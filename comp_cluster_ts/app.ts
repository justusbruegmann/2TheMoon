import express from "express";
import {drizzle} from "drizzle-orm/postgres-js";
import postgres from "postgres";
import dotenv from "dotenv";
import {asset} from "./db/schema.js";
import cors from "cors";
import portfolioHistoryRouter from "./router/portfolioHistory.js";

dotenv.config();
const app = express();
app.use(cors());

app.use(express.json());
app.use("/portfolioHistory", portfolioHistoryRouter);

const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) {
    console.error("DATABASE_URL is not defined in the environment variables.");
    process.exit(1);
}

const client = postgres(DATABASE_URL, {ssl: "require"});
export const db = drizzle({client});

async function tryConnection() {
    try {
        await db.select().from(asset).limit(1)
        console.log("Database connection successful.");
    } catch (error) {
        console.error("Database connection failed:", error);
    }
}

import portfolioRouter from "./router/portfolioHistory.js"
app.use("/portfolioHistory", portfolioRouter);


app.get("/", (req, res) => {
    res.send("Hello World!");
})

app.listen(3000, () => {
    tryConnection().then(() => {
        console.log("Server is running on port 3000");
    })
})