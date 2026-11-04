alter table public.user_asset rename to holding;
alter index public.user_asset_asset_id_idx rename to holding_asset_id_idx;

drop table public.portfolio_history;