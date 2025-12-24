from fastapi import FastAPI
from app.lifespan import lifespan

from app.routers.login import router as login_router
from app.routers.user.products import router as products_router
from app.routers.user.orders import router as orders_router
from app.routers.user.cart import router as cart_router
from app.routers.user.users import router as users_router
from app.routers.admin.admin import router as admin_router

from app.logging import setup_logging

setup_logging()

app = FastAPI(lifespan=lifespan)

app.include_router(login_router,prefix="/api/v1",tags=["Authentication"])
app.include_router(users_router,prefix="/api/v1",tags=["My Account"])
app.include_router(cart_router,prefix="/api/v1",tags=["My Cart"])
app.include_router(orders_router,prefix="/api/v1",tags=["My Orders"])
app.include_router(products_router,prefix="/api/v1",tags=["Products"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])