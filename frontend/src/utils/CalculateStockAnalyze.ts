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

export function calculateSummedUpCandleData(candleData: CandleChartData[], timeFrame: string): CandleChartData[] {
    if (candleData.length === 0) {
        return [];
    }
    const result : CandleChartData[] = [];
    if(timeFrame === "1W") {

        for (let i = 0; i < candleData.length; i += 6) {
            const chunk = candleData.slice(i, i + 6);
            result.push({
                timestamp: chunk[0].timestamp,
                open: chunk[0].open,
                close: chunk[chunk.length - 1].close,
                high: Math.max(...chunk.map(c => c.high)),
                low: Math.min(...chunk.map(c => c.low)),
            });
        }
    }
    return result;
}