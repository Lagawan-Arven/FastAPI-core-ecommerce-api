from fastapi import HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session

from app.database import models
from app.dependecies import get_session,get_current_user,admin_access
from app import schemas

router = APIRouter()

@router.get("/products",response_model=list[schemas.Base_Product_Out])
def get_all_products(current_user = Depends(get_current_user),
                     session: Session = Depends(get_session)):

    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_products = session.query(models.Product).all()
    if not db_products:
        raise HTTPException(status_code=400,detail="There is no products yet")
    
    return db_products

@router.get("/products/{product_id}",response_model=schemas.Base_Product_Out)
def get_product_by_id(product_id: int, current_user = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    return db_product

@router.post("/products",response_model=schemas.Base_Product_Out)
def add_prodcuct(product_input: schemas.Product_Create,
                 current_user = Depends(admin_access),
                 session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    new_product = models.Product(
        name = product_input.name,
        stock = product_input.stock,
        price = product_input.price,
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@router.put("/products/{product_id}",response_model=schemas.Base_Product_Out)
def update_product(product_id: int, product_updates: schemas.Product_Update,
                    current_user = Depends(admin_access),
                    session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    db_product.name = product_updates.name
    db_product.price = product_updates.price
    db_product.stock = product_updates.stock

    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int,
                    current_user = Depends(admin_access),
                    session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,current_user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_product = session.get(models.Product,product_id)
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    session.delete(db_product)
    session.commit()
    return{"message":"Product deleted successfully!"}