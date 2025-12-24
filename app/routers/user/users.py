from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependecies import get_current_user
from app.database import models
from app import schemas
from app.operations import operations

router = APIRouter()

#===============================
        #GET CURRENT USER
#===============================
@router.get("/user",response_model=schemas.Base_User_Out)
def get_user_info(current_user = Depends(get_current_user)):
    
    return current_user