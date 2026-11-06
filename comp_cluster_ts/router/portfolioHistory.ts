import {Router} from "express";
import {portfolioHistory} from "../service/portfolioHistory.js";

const router = Router();

router.get("/", async (req, res) => {
    const portfolioId = req.query.portfolioId as string | undefined;
    const start = new Date((req.query.start as string) ?? 0);
    const end = req.query.end ? new Date(req.query.end as string) : new Date();

    if (!portfolioId || isNaN(start.getTime()) || isNaN(end.getTime())) {
        res.status(400).json({error: "portfolioId, start und end (ISO times) needed"});
        return;
    }

    try {
        res.json(await portfolioHistory(portfolioId, start, end));
    } catch (error) {
        console.error(error);
        res.status(500).json({error: "Could not calculate portfolio history"});
    }
});

export default router;
