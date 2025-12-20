from fastapi import FastAPI
from app.routers.login import router as login_router
from app.routers.products import router as products_router
from app.routers.orders import router as orders_router
from app.routers.cart import router as cart_router
from app.routers.users import router as users_router

app = FastAPI()

app.include_router(login_router)
app.include_router(users_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(products_router)