from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from redis import Redis
from contextlib import asynccontextmanager
import os,logging

from src.database import models
from src.database.database import engine,local_session
from src.core.auth import hash_password
from src.database.database import init_db
from src. database.wait_for_db import wait_for_db
from src.core.limiter import limiter

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    #===============================
        #VALIDATE ENVIRONMENT
    #===============================
    required_env = ["DB_URL","SECRET_KEY","ALGORITHM"]

    for variable in required_env:
        if not os.getenv(variable):
            raise RuntimeError(f"Missing environment variable: {variable}")
        
    #===============================
        #WAIT FOR DATABASE
    #===============================
    wait_for_db(engine, max_retries=10, delay_seconds=2)
   
   #===============================
        #INITIALIZE DATABASE
    #===============================
    if os.getenv("TESTING") == "1":
        logger.info("Running in TESTING mode")
    elif os.getenv("ENVIRONMENT") == "local" or "docker":
        init_db()

    #===============================
        #CREATE ADMIN USER
    #===============================
    session = local_session()
    try:
        admin = session.query(models.User).filter(models.User.role=="admin").first()
        if not admin:
            admin = models.User(
                username = "admin",
                email = "admin",
                password = hash_password("1234") ,
                role = "admin",
                fullname = "System Admin",
                age = 0,
                gender = "admin",
                occupation = "admin"
            )
            session.add(admin)
            session.commit()
    finally:
        session.close()

    #===============================
        #CONFIGURE REDIS
    #===============================
    redis = Redis(host="localhost",port=6379,decode_responses=True)

    #===============================
        #CONFIGURE RATE LIMITER
    #===============================
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(status_code=429,content={"message":"Too many requests"})

    logger.info("Application startup complete")

    yield
    
    logger.info("Application shutdown")
    redis.close()
    engine.dispose()