import type {CandleChartData} from "../types/chart.ts";

export function calculateStockAnalyze(candleData: CandleChartData[]): { min: number, max: number } {
    if (candleData.length === 0) {
        return {min: 0, max: 0};
    }

    let min = candleData[0].low;
    let max = candleData[0].high;

    for (const candle of candleData) {
        if (candle.low < min) {
            min = candle.low;
        }
        if (candle.high > max) {
            max = candle.high;
        }
    }

    return {min, max};
}