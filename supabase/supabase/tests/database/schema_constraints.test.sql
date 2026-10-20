begin;

create extension if not exists pgtap with schema extensions;

select plan(22);

insert into auth.users (id, raw_user_meta_data) values
    ('00000000-0000-0000-0000-00000000000a', '{"display_name": "alice"}'),
    ('00000000-0000-0000-0000-00000000000b', '{}');

insert into public.season (id, name, status, starting_balance, starts_at) values
    ('10000000-0000-0000-0000-000000000001', 'Season 1', 'active', 10000, now()),
    ('10000000-0000-0000-0000-000000000002', 'Season 2', 'upcoming', 10000, now() + interval '30 days');

insert into public.asset (id, ticker, name, kind, creator_id) values
    ('20000000-0000-0000-0000-000000000001', 'AAPL', 'Apple', 'stock', null),
    ('20000000-0000-0000-0000-000000000002', 'MOON', 'Moon Coin', 'custom_crypto', '00000000-0000-0000-0000-00000000000a');

insert into public.portfolio (id, user_id, season_id, cash_balance) values
    ('30000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-00000000000a', '10000000-0000-0000-0000-000000000001', 10000),
    ('30000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-00000000000b', '10000000-0000-0000-0000-000000000001', 10000);

select is(
    (select display_name from public.profile where id = '00000000-0000-0000-0000-00000000000a'),
    'alice',
    'signup creates a profile with the display name from user metadata'
);

select is(
    (select display_name from public.profile where id = '00000000-0000-0000-0000-00000000000b'),
    'trader_00000000',
    'signup without a display name falls back to a generated one'
);

select throws_ok(
    $$ insert into auth.users (raw_user_meta_data) values ('{"display_name": "alice"}') $$,
    '23505', null,
    'display names are unique'
);

select throws_ok(
    $$ insert into public.season (name, status, starting_balance, starts_at) values ('Dup', 'active', 1, now()) $$,
    '23505', null,
    'only one season can be active'
);

select throws_ok(
    $$ insert into public.season (name, starting_balance, starts_at, ends_at) values ('Bad', 1, now(), now() - interval '1 day') $$,
    '23514', null,
    'season must end after it starts'
);

select throws_ok(
    $$ insert into public.season (name, starting_balance, starts_at) values ('Broke', 0, now()) $$,
    '23514', null,
    'season starting balance must be positive'
);

select throws_ok(
    $$ insert into public.asset (ticker, name, kind, creator_id) values ('MSFT', 'Microsoft', 'stock', '00000000-0000-0000-0000-00000000000a') $$,
    '23514', null,
    'non-custom assets cannot have a creator'
);

select throws_ok(
    $$ insert into public.asset (ticker, name, kind) values ('DOGE2', 'Doge Two', 'custom_crypto') $$,
    '23514', null,
    'custom crypto requires a creator'
);

select throws_ok(
    $$ insert into public.asset (ticker, name, kind) values ('aapl', 'Lowercase', 'stock') $$,
    '23514', null,
    'tickers must be uppercase symbols'
);

select throws_ok(
    $$ insert into public.asset (ticker, name, kind) values ('AAPL', 'Apple Again', 'stock') $$,
    '23505', null,
    'tickers are unique'
);

select throws_ok(
    $$ update public.portfolio set cash_balance = -1 where id = '30000000-0000-0000-0000-000000000001' $$,
    '23514', null,
    'cash balance cannot be negative'
);

select throws_ok(
    $$ insert into public.portfolio (user_id, season_id, cash_balance) values ('00000000-0000-0000-0000-00000000000a', '10000000-0000-0000-0000-000000000001', 1) $$,
    '23505', null,
    'a user has at most one portfolio per season'
);

select lives_ok(
    $$ insert into public.trade (portfolio_id, season_id, asset_id, operation, quantity, execution_price, fee)
       values ('30000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'buy', 1.5, 189.12345678, 0.5) $$,
    'a valid trade can be recorded'
);

select throws_ok(
    $$ insert into public.trade (portfolio_id, season_id, asset_id, operation, quantity, execution_price)
       values ('30000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000002', '20000000-0000-0000-0000-000000000001', 'buy', 1, 1) $$,
    '23503', null,
    'trade season must match the portfolio season'
);

select throws_ok(
    $$ insert into public.trade (portfolio_id, season_id, asset_id, operation, quantity, execution_price)
       values ('30000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 'sell', 0, 1) $$,
    '23514', null,
    'trade quantity must be positive'
);

select lives_ok(
    $$ insert into public.user_asset (portfolio_id, asset_id, quantity, average_buy_price)
       values ('30000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 1.5, 189.12345678) $$,
    'a holding can be recorded'
);

select throws_ok(
    $$ insert into public.user_asset (portfolio_id, asset_id, quantity)
       values ('30000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 2) $$,
    '23505', null,
    'a portfolio holds each asset at most once'
);

select lives_ok(
    $$ insert into public.portfolio_history (portfolio_id, recorded_at, cash_balance, user_assets_value) values
       ('30000000-0000-0000-0000-000000000001', now(), 10000, 0),
       ('30000000-0000-0000-0000-000000000001', now() + interval '1 minute', 9000, 1000) $$,
    'a portfolio can have multiple history snapshots'
);

select throws_ok(
    $$ insert into public.price_history (season_id, asset_id, price, recorded_at) values
       ('10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 1, '2026-01-01T00:00:00Z'),
       ('10000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001', 2, '2026-01-01T00:00:00Z') $$,
    '23505', null,
    'one price per asset, season and timestamp'
);

select throws_ok(
    $$ insert into public.market_event (season_id, label, description, starts_at, ends_at)
       values ('10000000-0000-0000-0000-000000000001', 'Crash', 'Markets fall', now(), now() - interval '1 hour') $$,
    '23514', null,
    'market event must end after it starts'
);

select throws_ok(
    $$ delete from auth.users where id = '00000000-0000-0000-0000-00000000000a' $$,
    '23503', null,
    'a custom crypto creator cannot be deleted while the token exists'
);

delete from auth.users where id = '00000000-0000-0000-0000-00000000000b';

select is(
    (select count(*)::int from public.portfolio where user_id = '00000000-0000-0000-0000-00000000000b'),
    0,
    'deleting a user cascades to profile and portfolios'
);

select * from finish();

rollback;
