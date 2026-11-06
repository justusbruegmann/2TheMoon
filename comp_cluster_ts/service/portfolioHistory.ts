import type { PriceData } from "../types/priceData.js";
import type { Candle } from "../types/candle.js";

import { getLastTradesOfUser } from "../repository/lastTrades.js";
import { getCurrentHoldingsOfPortfolio } from "../repository/holdings.js";
import { getPriceHistoryOfAssets } from "../repository/priceHistory.js";

export async function portfolioHistory(portfolioId: string, start: Date, end: Date): Promise<Candle[]> {
    //load all holdings in intervall
    const [holdings, trades] = await Promise.all([
        getCurrentHoldingsOfPortfolio(portfolioId),
        getLastTradesOfUser(portfolioId, start, new Date()),
    ]);

    //Set so no dups
    const assetIds = [...new Set([
        ...holdings.map((h) => h.assetId),
        ...trades.map((t) => t.assetId),
    ])];

    //get price data for each asset
    const rows = await getPriceHistoryOfAssets(assetIds, start, end);

    const candlesByAsset = new Map<string, Candle[]>(assetIds.map((id) => [id, []]));
    for (const row of rows) {
        candlesByAsset.get(row.assetId)!.push({
            timestamp: row.recordedAt,
            open: Number(row.open),
            high: Number(row.high),
            low: Number(row.low),
            close: Number(row.close),
        });
    }

    const priceData: PriceData[] = [...candlesByAsset].map(([assetId, candles]) => ({ assetId, candles }));

    //sort cancles my timestamp without dups
    const timestamps = [...new Set(
        priceData.flatMap((p) => p.candles.map((c) => c.timestamp.getTime()))
    )]

    //calculate quantity of each asset per timestamp
    const parsedTrades = trades
        .map((t) => ({
            assetId: t.assetId,
            time: t.executedAt.getTime(),
            delta: t.operation === "buy" ? -Number(t.quantity) : Number(t.quantity),
        }))
        .filter((t) => !isNaN(t.delta));

    const currentQuantity = new Map(holdings.map((h) => [h.assetId, Number(h.quantity)]));
    const quantityAt = (assetId: string, time: number): number => {
        let quantity = currentQuantity.get(assetId) ?? 0;
        for (const trade of parsedTrades) {
            if (trade.assetId !== assetId || trade.time <= time) continue;
            quantity += trade.delta;
        }
        return quantity;
    };

    const lastIndex = new Map<string, number>(assetIds.map((id) => [id, -1]));
    //build output
    const result: Candle[] = [];
    for (const time of timestamps) {
        const sum: Candle = { timestamp: new Date(time), open: 0, high: 0, low: 0, close: 0 };
        for (const { assetId, candles } of priceData) {
            let i = lastIndex.get(assetId)!;
            while (i + 1 < candles.length && candles[i + 1]!.timestamp.getTime() <= time) i++;
            lastIndex.set(assetId, i);
            if (i < 0) continue;

            const quantity = quantityAt(assetId, time);
            const candle = candles[i]!;
            if (isNaN(quantity)) continue;
            if (isNaN(candle.open) || isNaN(candle.high) || isNaN(candle.low) || isNaN(candle.close)) continue;
            const isCurrent = candle.timestamp.getTime() === time;
            sum.open += quantity * (isCurrent ? candle.open : candle.close);
            sum.high += quantity * (isCurrent ? candle.high : candle.close);
            sum.low += quantity * (isCurrent ? candle.low : candle.close);
            sum.close += quantity * candle.close;
        }
        result.push(sum);
    }

    return result;
}
