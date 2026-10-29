begin;

create extension if not exists pgtap with schema extensions;

select plan(15);

insert into auth.users (id, raw_user_meta_data) values
    ('00000000-0000-0000-0000-00000000000a', '{"display_name": "alice"}'),
    ('00000000-0000-0000-0000-00000000000b', '{"display_name": "bob"}');

insert into public.season (id, name, status, starting_balance, starts_at) values
    ('10000000-0000-0000-0000-000000000001', 'Season 1', 'active', 10000, now());

insert into public.asset (id, ticker, name, kind) values
    ('20000000-0000-0000-0000-000000000001', 'AAPL', 'Apple', 'stock');

insert into public.portfolio (id, user_id, season_id, cash_balance) values
    ('30000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-00000000000a', '10000000-0000-0000-0000-000000000001', 10000),
    ('30000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-00000000000b', '10000000-0000-0000-0000-000000000001', 10000);

insert into public.trade (portfolio_id, season_id, asset_id, operation, quantity, execution_price) values
    ('30000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'buy', 1, 100),
    ('30000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'buy', 2, 100);

insert into public.user_asset (portfolio_id, asset_id, quantity) values
    ('30000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 1),
    ('30000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001', 2);

insert into public.portfolio_history (portfolio_id, cash_balance, user_assets_value) values
    ('30000000-0000-0000-0000-000000000001', 9900, 100),
    ('30000000-0000-0000-0000-000000000002', 9800, 200);

insert into public.price_history (season_id, asset_id, open, close, high, low) values
    ('10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 100, 105, 110, 95);

insert into public.chat_message (sender_id, message) values
    ('00000000-0000-0000-0000-00000000000b', 'to the moon');

insert into public.market_event (season_id, label, description, starts_at, ends_at) values
    ('10000000-0000-0000-0000-000000000001', 'Rally', 'Tech rally', now() - interval '1 hour', now() + interval '1 hour'),
    ('10000000-0000-0000-0000-000000000001', 'Crash', 'Future crash', now() + interval '1 day', now() + interval '2 days');

set local role authenticated;
set local request.jwt.claims to '{"sub": "00000000-0000-0000-0000-00000000000a", "role": "authenticated"}';

select is((select count(*)::int from public.profile), 2, 'authenticated users can read all profiles');
select is((select count(*)::int from public.season), 1, 'authenticated users can read seasons');
select is((select count(*)::int from public.asset), 1, 'authenticated users can read assets');
select is((select count(*)::int from public.price_history), 1, 'authenticated users can read price history');
select is((select count(*)::int from public.chat_message), 1, 'authenticated users can read chat messages');
select is((select count(*)::int from public.market_event), 1, 'future market events are hidden from players');

select is(
    (select array_agg(id) from public.portfolio),
    array['30000000-0000-0000-0000-000000000001'::uuid],
    'users only see their own portfolio'
);
select is((select count(*)::int from public.trade), 1, 'users only see their own trades');
select is((select count(*)::int from public.user_asset), 1, 'users only see their own holdings');
select is((select count(*)::int from public.portfolio_history), 1, 'users only see their own portfolio history');

select throws_ok(
    $$ insert into public.trade (portfolio_id, season_id, asset_id, operation, quantity, execution_price)
       values ('30000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'buy', 1, 1) $$,
    '42501', null,
    'players cannot record trades directly'
);

select throws_ok(
    $$ update public.portfolio set cash_balance = 1000000 where id = '30000000-0000-0000-0000-000000000001' $$,
    '42501', null,
    'players cannot change their cash balance'
);

select throws_ok(
    $$ update public.profile set display_name = 'mallory' where id = '00000000-0000-0000-0000-00000000000a' $$,
    '42501', null,
    'profiles are only written by the backend'
);

reset role;
set local role anon;

select throws_ok(
    $$ select count(*) from public.profile $$,
    '42501', null,
    'anonymous clients cannot read any table'
);

reset role;
set local role service_role;

select is((select count(*)::int from public.portfolio), 2, 'the service role bypasses row level security');

select * from finish();

rollback;