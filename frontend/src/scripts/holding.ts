import type {Holding} from "../types/holding.ts";
import {supabase} from "../lib/supabaseClient.ts";
import {notify} from "./notify.ts";
import type {ApiResponse} from "../types/api.ts";

const BASE_URL: string = import.meta.env.VITE_BACKEND_URL

export async function getHoldings(): Promise<Holding[]> {
    //here await because we need to ensure the user is authenticated before making the request
    const userId = (await supabase.auth.getSession()).data.session?.user.id;
    if (!userId) {
        notify.error("User not authenticated", "You must be logged in to fetch holdings.");
        throw new Error("User not authenticated");
    }
    const url = `${BASE_URL}/holdings/${userId}`;
    //here no await because we can first assemble the request and await it only when we need the result of the authToken Promise.
    const authToken = supabase.auth.getSession().then((session) => session.data.session?.access_token);
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${await authToken}`
        },
    });
    if (!response.ok) {
        notify.error("Failed to fetch holdings", "An error occurred while fetching holdings.");
        throw new Error("Failed to fetch holdings");
    }
    const data: ApiResponse<any> = await response.json();
    return data.data.map(h => ({
        assetId: h.asset_id,
        quantity: Number(h.quantity),
        avgBuyPrice: Number(h.average_buy_price),
    }));
}