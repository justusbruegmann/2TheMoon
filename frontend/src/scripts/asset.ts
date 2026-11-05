import type {Asset} from "../types/asset.ts";
import type {ApiResponse} from "../types/api.ts";
import {notify} from "./notify.ts";
import {supabase} from "../lib/supabaseClient.ts";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export async function getAssets(): Promise<Asset[]> {
    const url = `${BACKEND_URL}/assets/`;
    const authToken = supabase.auth.getSession().then((session) => session.data.session?.access_token);
    const response = await fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${await authToken}`
        },
    });
    if (response.ok) {
        const data: ApiResponse<Asset> = await response.json() as ApiResponse<Asset>;
        return data.data;
    } else {
        const data: ApiResponse<Asset> = await response.json() as ApiResponse<Asset>;
      notify.error("Failed to fetch assets",`Failed to fetch assets: ${response.status} ${data.message}`);
      return [];
    }
}
