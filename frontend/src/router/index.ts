import {createRouter, createWebHistory} from "vue-router";

//Page imports
import PortfolioPage from "../pages/PortfolioPage.vue";
import StocksDetailsPage from "../pages/StocksDetailsPage.vue";
import StocksOverviewPage from "../pages/StocksOverviewPage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import LeaderBoardPage from "../pages/LeaderBoardPage.vue";
import NotFound from "../pages/NotFound.vue";
import HomePage from "../pages/HomePage.vue";

const routes = [
    {path: "/", name: "2TheMoon | Home", component: HomePage, meta: {title: "Home"}},
    {path: "/portfolio", name: "2TheMoon | Portfolio", component: PortfolioPage, meta: {title: "Portfolio"}},
    {path: "/stocks", name: "2TheMoon | Stocks", component: StocksOverviewPage,meta: {title: "Stocks"}},
    {path: "/stocks/:symbol", name: "2TheMoon | Stock", component: StocksDetailsPage, props: true,meta: {title: "Stocks Details"}},
    {path: "/login", name: "2TheMoon | Login", component: LoginPage,meta: {title: "Login"}},
    {path: "/register", name: "2TheMoon | Register", component: RegisterPage,meta: {title: "Register"}},
    {path: "/Leaderboard", name: "2TheMoon | Leaderboard", component: LeaderBoardPage, meta: {title: "Leaderboard"}},
    {path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound,meta: {title: "404 Not Found"}},
]


const router = createRouter({
    history: createWebHistory(),
    routes
})
router.beforeEach((to, _from, next) => {
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