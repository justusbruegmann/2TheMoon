// Shape returned by GET /price_history (numeric fields arrive as decimal strings)
export type PriceHistory = {
    season_id: string;
    asset_id: string;
    recorded_at: string;
    open: string;
    high: string;
    low: string;
    close: string;
}
