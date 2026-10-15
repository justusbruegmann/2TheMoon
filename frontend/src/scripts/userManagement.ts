import {supabase} from "../lib/supabaseClient.ts";


export async function isLoggedIn() {
    const { data } = await supabase.auth.getSession()
    if (data && data?.session) {
        return true;
    } else {
        return false;
    }
}

//hi