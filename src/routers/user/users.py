import json
from fastapi import APIRouter,Depends,HTTPException
from redis.asyncio import Redis

from src.utilities.dependecies import get_current_user,get_redis
from src.utilities import models,schemas

router = APIRouter()

#===============================
        #GET CURRENT USER
#===============================
@router.get("/users/me")
async def get_user_info(current_user = Depends(get_current_user)):
    return current_user