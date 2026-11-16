create index price_hisotry_asset_id_recorded_at_idx
    on public.price_history (asset_id, recorded_at desc);