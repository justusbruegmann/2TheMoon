import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { Asset } from "../types/asset.ts";
import { getAssets } from "../scripts/asset.ts";

export const useAssetStore = defineStore("assets", () => {

    const assets = ref<Asset[]>([]);
    const loading = ref(false);

    const byId = computed(() => new Map(assets.value.map(a => [a.id, a])));

    async function load(force = false) {
        if (!force && assets.value.length) return;
        loading.value = true;
        try {
            assets.value = await getAssets();
        } finally {
            loading.value = false;
        }
    }

    return { assets, loading, byId, load };
});