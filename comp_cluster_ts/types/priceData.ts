import type { Candle } from "./candle.js";
export type PriceData = {
    assetId: string,
    candles: Candle[]
}