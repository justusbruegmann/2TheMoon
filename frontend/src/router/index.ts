import {createRouter, createWebHistory} from "vue-router";

//Page imports
import PortfolioPage from "../pages/PortfolioPage.vue";
import StocksDetailsPage from "../pages/StocksDetailsPage.vue";
import StocksOverviewPage from "../pages/StocksOverviewPage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import LeaderBoardPage from "../pages/LeaderBoardPage.vue";

const routes = [
    { path: "/", redirect: "/portfolio" },
    {path: "/portfolio", name: "2TheMoon | Portfolio", component: PortfolioPage},
    {path: "/stocks", name: "2TheMoon | Stocks", component: StocksOverviewPage},
    {path: "/stocks/:symbol", name: "2TheMoon | Stock", component: StocksDetailsPage, props: true},
    {path: "/login", name: "2TheMoon | Login", component: LoginPage},
    {path: "/register", name: "2TheMoon | Register", component: RegisterPage},
    {path: "/Leaderboard", name: "2TheMoon | Leaderboard", component: LeaderBoardPage},

]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router