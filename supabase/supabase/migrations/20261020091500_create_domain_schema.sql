create type public.asset_kind as enum ('stock', 'crypto', 'custom_crypto');
create type public.trade_operation as enum ('buy', 'sell');
create type public.season_status as enum ('upcoming', 'active', 'ended');
-- Values are defined in a follow-up migration via `alter type public.industry add value '...'`.
create type public.industry as enum ();

create table public.profile (
    id uuid primary key references auth.users (id) on delete cascade,
    display_name text not null unique check (char_length(display_name) between 3 and 32),
    created_at timestamptz not null default now()
);

create table public.season (
    id uuid primary key default gen_random_uuid(),
    name text not null check (char_length(name) between 1 and 64),
    status public.season_status not null default 'upcoming',
    starting_balance numeric(24, 8) not null check (starting_balance > 0),
    starts_at timestamptz not null,
    ends_at timestamptz,
    created_at timestamptz not null default now(),
    check (ends_at is null or ends_at > starts_at)
);

create unique index season_single_active_idx on public.season (status) where status = 'active';

create table public.asset (
    id uuid primary key default gen_random_uuid(),
    ticker text not null unique check (ticker ~ '^[A-Z0-9][A-Z0-9.\-]{0,14}$'),
    name text not null check (char_length(name) between 1 and 128),
    kind public.asset_kind not null,
    industry public.industry[] not null default '{}',
    -- Restrict: deleting a creator must not silently wipe other players' trades and holdings in that token.
    creator_id uuid references public.profile (id) on delete restrict,
    created_at timestamptz not null default now(),
    check ((kind = 'custom_crypto') = (creator_id is not null))
);

create index asset_creator_id_idx on public.asset (creator_id) where creator_id is not null;

create table public.portfolio (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profile (id) on delete cascade,
    season_id uuid not null references public.season (id) on delete cascade,
    cash_balance numeric(24, 8) not null check (cash_balance >= 0),
    created_at timestamptz not null default now(),
    unique (user_id, season_id),
    -- Target of trade's composite FK, guarantees trade.season_id matches its portfolio's season.
    unique (id, season_id)
);

create index portfolio_season_id_idx on public.portfolio (season_id);

create table public.trade (
    id uuid primary key default gen_random_uuid(),
    portfolio_id uuid not null,
    season_id uuid not null,
    asset_id uuid not null references public.asset (id) on delete restrict,
    operation public.trade_operation not null,
    quantity numeric(24, 8) not null check (quantity > 0),
    execution_price numeric(24, 8) not null check (execution_price > 0),
    fee numeric(24, 8) not null default 0 check (fee >= 0),
    executed_at timestamptz not null default now(),
    created_at timestamptz not null default now(),
    foreign key (portfolio_id, season_id) references public.portfolio (id, season_id) on delete cascade
);

create index trade_portfolio_executed_at_idx on public.trade (portfolio_id, executed_at desc);
create index trade_asset_id_idx on public.trade (asset_id);

create table public.user_asset (
    portfolio_id uuid not null references public.portfolio (id) on delete cascade,
    asset_id uuid not null references public.asset (id) on delete restrict,
    quantity numeric(24, 8) not null check (quantity > 0),
    average_buy_price numeric(24, 8) check (average_buy_price > 0),
    primary key (portfolio_id, asset_id)
);

create index user_asset_asset_id_idx on public.user_asset (asset_id);

create table public.portfolio_history (
    portfolio_id uuid not null references public.portfolio (id) on delete cascade,
    recorded_at timestamptz not null default now(),
    cash_balance numeric(24, 8) not null check (cash_balance >= 0),
    user_assets_value numeric(24, 8) not null check (user_assets_value >= 0),
    primary key (portfolio_id, recorded_at)
);

create table public.price_history (
    season_id uuid not null references public.season (id) on delete cascade,
    asset_id uuid not null references public.asset (id) on delete cascade,
    price numeric(24, 8) not null check (price > 0),
    recorded_at timestamptz not null default now(),
    primary key (season_id, asset_id, recorded_at)
);

create table public.market_event (
    id uuid primary key default gen_random_uuid(),
    season_id uuid not null references public.season (id) on delete cascade,
    label text not null check (char_length(label) between 1 and 64),
    description text not null,
    affected_industries public.industry[] not null default '{}',
    starts_at timestamptz not null,
    ends_at timestamptz not null,
    created_at timestamptz not null default now(),
    check (ends_at > starts_at)
);

create index market_event_season_starts_at_idx on public.market_event (season_id, starts_at);

create function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
    insert into public.profile (id, display_name)
    values (
        new.id,
        coalesce(
            nullif(btrim(new.raw_user_meta_data ->> 'display_name'), ''),
            'trader_' || left(new.id::text, 8)
        )
    );
    return new;
end;
$$;

revoke all on function public.handle_new_user() from public, anon, authenticated;

create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_user();

do $$
declare
    table_name text;
begin
    foreach table_name in array array[
        'profile', 'season', 'asset', 'portfolio', 'trade',
        'user_asset', 'portfolio_history', 'price_history', 'market_event'
    ]
    loop
        execute format('alter table public.%I enable row level security', table_name);
        execute format('revoke all on table public.%I from anon, authenticated', table_name);
        execute format('grant select on table public.%I to authenticated', table_name);
        execute format('grant all on table public.%I to service_role', table_name);
    end loop;
end;
$$;

create policy "Authenticated users can read profiles"
    on public.profile for select to authenticated
    using (true);

create policy "Authenticated users can read seasons"
    on public.season for select to authenticated
    using (true);

create policy "Authenticated users can read assets"
    on public.asset for select to authenticated
    using (true);

create policy "Authenticated users can read price history"
    on public.price_history for select to authenticated
    using (true);

create policy "Authenticated users can read started market events"
    on public.market_event for select to authenticated
    using (starts_at <= now());

create policy "Users can read their own portfolios"
    on public.portfolio for select to authenticated
    using (user_id = (select auth.uid()));

create policy "Users can read their own trades"
    on public.trade for select to authenticated
    using (exists (
        select 1 from public.portfolio p
        where p.id = trade.portfolio_id and p.user_id = (select auth.uid())
    ));

create policy "Users can read their own holdings"
    on public.user_asset for select to authenticated
    using (exists (
        select 1 from public.portfolio p
        where p.id = user_asset.portfolio_id and p.user_id = (select auth.uid())
    ));

create policy "Users can read their own portfolio history"
    on public.portfolio_history for select to authenticated
    using (exists (
        select 1 from public.portfolio p
        where p.id = portfolio_history.portfolio_id and p.user_id = (select auth.uid())
    ));
