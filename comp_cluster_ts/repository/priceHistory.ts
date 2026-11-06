import {db} from  "../app.js"
import * as schema from "../db/schema.js"
import {and, eq, gte, lte, asc, inArray} from "drizzle-orm";

export async function getPriceHistoryOfAssets(assetIds: string[], start: Date, end: Date) {
    if (assetIds.length === 0) return [];
    return db.select().from(schema.priceHistory).where(and(
        inArray(schema.priceHistory.assetId, assetIds),
        gte(schema.priceHistory.recordedAt, start),
        lte(schema.priceHistory.recordedAt, end)
    )).orderBy(asc(schema.priceHistory.recordedAt));
}