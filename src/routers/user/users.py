from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from src.core.dependecies import get_current_user
from src.database import models
from src.core import schemas
from src.operations import operations

router = APIRouter()

#===============================
        #GET CURRENT USER
#===============================
@router.get("/users/me",response_model=schemas.Base_User_Out)
def get_user_info(current_user = Depends(get_current_user)):
    
    return current_user