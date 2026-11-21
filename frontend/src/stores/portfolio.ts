import {defineStore} from "pinia";
import {ref, computed} from "vue";
import type {Portfolio} from "../types/portfolio.ts";
import {getPortfolio} from "../scripts/portfolio.ts";
import {supabase} from "../lib/supabaseClient.ts";

export const usePortfolioStore = defineStore("portfolio", () => {
    const portfolio = ref<Portfolio | null>(null);
    const loading = ref(false);
    let inFlight: Promise<void> | null = null;

    const cashBalance = computed(() => portfolio.value?.cash_balance ?? 0);

    function load(force = false): Promise<void> {
        if (!force && portfolio.value) return Promise.resolve();
        if (inFlight) return inFlight;   // concurrent callers share one request

        inFlight = (async () => {
            loading.value = true;
            try {
                const {data: {user}} = await supabase.auth.getUser();
                if (!user) return;
                portfolio.value = await getPortfolio();
            } finally {
                loading.value = false;
                inFlight = null;
            }
        })();
        return inFlight;
    }

    return {portfolio, loading, cashBalance, load};
});