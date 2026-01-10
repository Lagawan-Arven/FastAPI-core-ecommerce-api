from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import logging,os

from src.utilities import models
from src.configurations.database import engine,local_session,init_db
from src.utilities.auth import hash_password
from src.core.wait_for_db import wait_for_db
from src.configurations.config import limiter
from src.configurations.initialize_env import DB_URL,SECRET_KEY,ALGORITHM,REDIS_DB,REDIS_HOST,REDIS_PORT

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    #===============================
        #VALIDATE ENVIRONMENT
    #===============================
    required_env = [DB_URL,SECRET_KEY,ALGORITHM,REDIS_DB,REDIS_HOST,REDIS_PORT]

    for variable in required_env:
        if not variable:
            raise RuntimeError(f"Missing environment variable")
        
    #===============================
        #CONFIGURE REDIS
    #===============================
    app.state.redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        
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
        #CONFIGURE RATE LIMITER
    #===============================
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(status_code=429,content={"message":"Too many requests"})

    logger.info("Application startup complete")

    yield
    
    logger.info("Application shutdown")
    await app.state.redis.close()
    engine.dispose()