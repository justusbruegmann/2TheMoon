import {db} from "../app.js"
import * as schema from "../db/schema.js"
import {and, eq, gte, lte, desc} from "drizzle-orm";

export async function getLastTradesOfUser(portfolioId: string, start: Date, end: Date) {
    const result = await db.select().from(schema.trade).where(and(
        eq(schema.trade.portfolioId, portfolioId),
        gte(schema.trade.executedAt, start),
        lte(schema.trade.executedAt, end)
    )).orderBy(desc(schema.trade.executedAt));
    return result;
}
