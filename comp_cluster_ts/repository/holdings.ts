import {db} from "../app.js"
import * as schema from "../db/schema.js"
import { eq} from "drizzle-orm";

export async function getCurrentHoldingsOfPortfolio(portfolioId: string) {
    const result = await db.select().from(schema.holding).where(eq(schema.holding.portfolioId, portfolioId))
    return result;
}