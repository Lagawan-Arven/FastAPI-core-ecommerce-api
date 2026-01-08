import logging
from fastapi import FastAPI,Request

from src.routers.login import router as login_router
from src.routers.user.products import router as products_router
from src.routers.user.orders import router as orders_router
from src.routers.user.cart import router as cart_router
from src.routers.user.users import router as users_router
from src.routers.admin.admin import router as admin_router

from src.core.lifespan import lifespan
from src.core.logging import setup_logging
from src.core.limiter import limiter

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

@app.get("/")
@limiter.limit("5/minute")
def app_started(request: Request):
    logger.info("App started")
    return {"message":"App Started"}

app.include_router(login_router,prefix="/api/v1/auth",tags=["Authentication"])
app.include_router(users_router,prefix="/api/v1",tags=["My Account"])
app.include_router(cart_router,prefix="/api/v1/my",tags=["My Cart"])
app.include_router(orders_router,prefix="/api/v1/my",tags=["My Orders"])
app.include_router(products_router,prefix="/api/v1",tags=["Products"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])