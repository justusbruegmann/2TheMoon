import type {PriceHistory} from "../types/priceHistory.ts";
import type {CandleChartData} from "../types/chart.ts";
import type {ApiResponse} from "../types/api.ts";
import {notify} from "./notify.ts";
import {supabase} from "../lib/supabaseClient.ts";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export async function getPriceHistory(ticker: string): Promise<CandleChartData[]> {
    const url = `${BACKEND_URL}/price_history?ticker=${ticker}`;
    const authToken = supabase.auth.getSession().then((session) => session.data.session?.access_token);
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${await authToken}`
        },
    });
    if (response.ok) {
        const data: ApiResponse<PriceHistory> = await response.json() as ApiResponse<PriceHistory>;
        return data.data.map((item) => ({
            timestamp: new Date(item.recorded_at).getTime(),
            low: Number(item.low),
            high: Number(item.high),
            open: Number(item.open),
            close: Number(item.close)
        })).sort((a, b) => a.timestamp - b.timestamp);

    } else {
        const data: ApiResponse<PriceHistory> = await response.json() as ApiResponse<PriceHistory>;
        notify.error("Failed to fetch price history", `Failed to fetch price history: ${response.status} ${data.message}`);
        return [];
    }
}