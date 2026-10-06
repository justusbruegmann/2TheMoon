from fastapi import Depends, FastAPI
from .dependencies import check_header_token
from .routers import test_router


####################################################
# App
####################################################
app = FastAPI()


####################################################
# Routers
####################################################
app.include_router(
    test_router.router,
    prefix="/test_prefix",
    tags=["test-tag"],
    dependencies=[Depends(check_header_token)],
    responses={418: {"description": "I'm a teapot"}},
)


####################################################
# Health Check
####################################################
@app.get("/")
async def root():
    return {"health": "ok"}
