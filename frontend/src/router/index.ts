import {createRouter, createWebHistory} from "vue-router";
import {notify} from "../scripts/notify.ts";

//Page imports
import PortfolioPage from "../pages/PortfolioPage.vue";
import StocksDetailsPage from "../pages/StocksDetailsPage.vue";
import StocksOverviewPage from "../pages/StocksOverviewPage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import LeaderBoardPage from "../pages/LeaderBoardPage.vue";
import NotFound from "../pages/NotFound.vue";
import HomePage from "../pages/HomePage.vue";
import {isLoggedIn} from "../scripts/userManagement.ts";

const routes = [
    {path: "/", name: "2TheMoon | Home", component: HomePage, meta: {title: "Home"}},
    {path: "/portfolio", name: "2TheMoon | Portfolio", component: PortfolioPage, meta: {title: "Portfolio", requiresAuth: true}},
    {path: "/stocks", name: "2TheMoon | Stocks", component: StocksOverviewPage,meta: {title: "Stocks", requiresAuth: true}},
    {path: "/stocks/:symbol", name: "2TheMoon | Stock", component: StocksDetailsPage, props: true,meta: {title: "Stocks Details", requiresAuth: true}},
    {path: "/login", name: "2TheMoon | Login", component: LoginPage,meta: {title: "Login"}},
    {path: "/register", name: "2TheMoon | Register", component: RegisterPage,meta: {title: "Register"}},
    {path: "/Leaderboard", name: "2TheMoon | Leaderboard", component: LeaderBoardPage, meta: {title: "Leaderboard", requiresAuth: true}},
    {path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound,meta: {title: "404 Not Found"}},
]


const router = createRouter({
    history: createWebHistory(),
    routes
})
router.beforeEach(async (to, _from, next) => {
    if (to.meta.requiresAuth && !(await isLoggedIn())) {
        notify.error("Authentication Required", "You must be logged in to access this page.");
        next("/login")
        return
    }

    let dynamicTitle: string | {}

    if (to.meta.title) {
        dynamicTitle = to.meta.title
    } else {
        dynamicTitle = "2TheMoon"
    }

    document.title = `2TheMoon | ${dynamicTitle}`

    next()
})


export default router