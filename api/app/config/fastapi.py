from fastapi import FastAPI, Depends

from app.config.dependencies import get_user_db
from app.routers import asset_router, price_history_router, portfolio_router, holding_router, trade_router



#########################################
# API Endpoint Base URLs
#########################################
ASSETS = "/assets"
PRICE_HISTORY = "/price_history"
PORTFOLIOS = "/portfolios"
HOLDINGS = "/holdings"
TRADES = "/trades"


def register_routers(app: FastAPI):
    app.include_router(
        asset_router.router,
        prefix=ASSETS,
        tags=["Asset"],
        dependencies=[Depends(get_user_db)],
    )

    app.include_router(
        price_history_router.router,
        prefix=PRICE_HISTORY,
        tags=["Price History"],
        dependencies=[Depends(get_user_db)],
    )

    app.include_router(
        portfolio_router.router,
        prefix=PORTFOLIOS,
        tags=["Portfolio"],
        dependencies=[Depends(get_user_db)],
    )

    app.include_router(
        holding_router.router,
        prefix=HOLDINGS,
        tags=["Holding"],
        dependencies=[Depends(get_user_db)],
    )

    app.include_router(
        trade_router.router,
        prefix=TRADES,
        tags=["Trade"],
        dependencies=[Depends(get_user_db)],
    )
