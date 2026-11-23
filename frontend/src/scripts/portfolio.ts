import type {Portfolio} from "../types/portfolio.ts";
import {notify} from "./notify.ts";
import {supabase} from "../lib/supabaseClient.ts";



const BASE_URL : string = import.meta.env.VITE_BACKEND_URL

export async function postPortfolio(): Promise<Portfolio> {
    const userId = (await supabase.auth.getSession()).data.session?.user.id;
    if (!userId) {
        notify.error("User not authenticated", "You must be logged in to create a portfolio.");
        throw new Error("User not authenticated");
    }
    const url = `${BASE_URL}/portfolios/`;
    const authToken = supabase.auth.getSession().then((session) => session.data.session?.access_token);
    const body = JSON.stringify({user_id: userId});
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${await authToken}`
        },
        body: body
    });
    if (!response.ok) {
        notify.error("Failed to create portfolio", "An error occurred while creating the portfolio.");
        throw new Error("Failed to create portfolio");
    }
    const data: Portfolio = await response.json();
    return data;
}


export async function getPortfolio(): Promise<Portfolio> {
    //here await because we need to ensure the user is authenticated before making the request
    const userId = (await supabase.auth.getSession()).data.session?.user.id;
    if (!userId) {
        notify.error("User not authenticated", "You must be logged in to fetch holdings.");
        throw new Error("User not authenticated");
    }
    const url = `${BASE_URL}/portfolios/?user_id=${userId}`;
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
        notify.error("Failed to fetch portfolio", "An error occurred while fetching the portfolio.");
        throw new Error("Failed to fetch portfolio");
    }
    const data: any  = await response.json();
    return data.data;
}