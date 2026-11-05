import { sql } from "drizzle-orm";
import {
    numeric,
    pgEnum,
    pgPolicy,
    pgTable,
    primaryKey,
    text,
    timestamp,
    uuid,
} from "drizzle-orm/pg-core";
import { authenticatedRole, authUsers } from "drizzle-orm/supabase";


export const assetKind = pgEnum("asset_kind", ["stock", "crypto", "custom_crypto"]);
export const tradeOperation = pgEnum("trade_operation", ["buy", "sell"]);
export const seasonStatus = pgEnum("season_status", ["upcoming", "active", "ended"]);

// TODO: Die Werte von `industry` fehlen in der Doku. Bitte durch die echten ersetzen.
export const industry = pgEnum("industry", ["TODO_REPLACE_ME"]);


export const profile = pgTable(
    "profile",
    {
        id: uuid("id")
            .primaryKey()
            .references(() => authUsers.id),
        displayName: text("display_name").notNull().unique(),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Authenticated users can read profiles", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`true`,
        }),
    ],
);

export const season = pgTable(
    "season",
    {
        id: uuid("id").primaryKey().defaultRandom(),
        name: text("name").notNull(),
        status: seasonStatus("status").notNull(),
        startingBalance: numeric("starting_balance").notNull(),
        startsAt: timestamp("starts_at", { withTimezone: true }).notNull(),
        endsAt: timestamp("ends_at", { withTimezone: true }),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Authenticated users can read seasons", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`true`,
        }),
    ],
);

export const asset = pgTable(
    "asset",
    {
        id: uuid("id").primaryKey().defaultRandom(),
        ticker: text("ticker").notNull().unique(),
        name: text("name").notNull(),
        kind: assetKind("kind").notNull(),
        industry: industry("industry").array().notNull(),
        creatorId: uuid("creator_id").references(() => profile.id),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Authenticated users can read assets", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`true`,
        }),
    ],
);

export const portfolio = pgTable(
    "portfolio",
    {
        id: uuid("id").primaryKey().defaultRandom(),
        userId: uuid("user_id")
            .notNull()
            .references(() => profile.id),
        seasonId: uuid("season_id")
            .notNull()
            .references(() => season.id),
        cashBalance: numeric("cash_balance").notNull(),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Users can read their own portfolios", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`user_id = (SELECT auth.uid())`,
        }),
    ],
);

export const trade = pgTable(
    "trade",
    {
        id: uuid("id").primaryKey().defaultRandom(),
        portfolioId: uuid("portfolio_id")
            .notNull()
            .references(() => portfolio.id),
        seasonId: uuid("season_id")
            .notNull()
            .references(() => season.id),
        assetId: uuid("asset_id")
            .notNull()
            .references(() => asset.id),
        operation: tradeOperation("operation").notNull(),
        quantity: numeric("quantity").notNull(),
        executionPrice: numeric("execution_price").notNull(),
        fee: numeric("fee").notNull(),
        executedAt: timestamp("executed_at", { withTimezone: true }).notNull(),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Users can read their own trades", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`EXISTS (
        SELECT 1 FROM portfolio p
        WHERE p.id = trade.portfolio_id AND p.user_id = (SELECT auth.uid())
      )`,
        }),
    ],
);

export const holding = pgTable(
    "holding",
    {
        portfolioId: uuid("portfolio_id")
            .notNull()
            .references(() => portfolio.id),
        assetId: uuid("asset_id")
            .notNull()
            .references(() => asset.id),
        quantity: numeric("quantity").notNull(),
        averageBuyPrice: numeric("average_buy_price"),
    },
    (t) => [
        primaryKey({ columns: [t.portfolioId, t.assetId] }),
        pgPolicy("Users can read their own holdings", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`EXISTS (
        SELECT 1 FROM portfolio p
        WHERE p.id = holding.portfolio_id AND p.user_id = (SELECT auth.uid())
      )`,
        }),
    ],
);

export const priceHistory = pgTable(
    "price_history",
    {
        seasonId: uuid("season_id")
            .notNull()
            .references(() => season.id),
        assetId: uuid("asset_id")
            .notNull()
            .references(() => asset.id),
        open: numeric("open").notNull(),
        close: numeric("close").notNull(),
        high: numeric("high").notNull(),
        low: numeric("low").notNull(),
        recordedAt: timestamp("recorded_at", { withTimezone: true }).notNull(),
    },
    (t) => [
        primaryKey({ columns: [t.seasonId, t.assetId, t.recordedAt] }),
        pgPolicy("Authenticated users can read price history", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`true`,
        }),
    ],
);

export const marketEvent = pgTable(
    "market_event",
    {
        id: uuid("id").primaryKey().defaultRandom(),
        seasonId: uuid("season_id")
            .notNull()
            .references(() => season.id),
        label: text("label").notNull(),
        description: text("description").notNull(),
        affectedIndustries: industry("affected_industries").array().notNull(),
        startsAt: timestamp("starts_at", { withTimezone: true }).notNull(),
        endsAt: timestamp("ends_at", { withTimezone: true }).notNull(),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Authenticated users can read started market events", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`starts_at <= now()`,
        }),
    ],
);

export const chatMessage = pgTable(
    "chat_message",
    {
        id: uuid("id").primaryKey().defaultRandom(),
        senderId: uuid("sender_id")
            .notNull()
            .references(() => profile.id),
        message: text("message").notNull(),
        createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    },
    () => [
        pgPolicy("Authenticated users can read chat messages", {
            as: "permissive",
            for: "select",
            to: authenticatedRole,
            using: sql`true`,
        }),
    ],
);