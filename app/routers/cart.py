from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.dependecies import get_session,get_current_user
from app.database import models
from app import schemas

router = APIRouter()

#===============================
    #GET ALL ITEMS FROM CART
#===============================
@router.get("/cart/products",response_model= schemas.Base_Cart_Out)
def get_all_items_from_cart(user = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")

    return db_user.cart

#===============================
        #ADD ITEM TO CART
#===============================
@router.post("/cart/products/{product_id}",response_model=schemas.Base_Cart_Out)
def add_item_to_cart(product_id: int, quantity: int,
                     user = Depends(get_current_user),
                     session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_item = session.get(models.Product,product_id)
    if not db_item:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    if quantity > db_item.stock:
        raise HTTPException(status_code=400,detail="Insufficient product stock!")

    db_link = (session.query(models.Cart_Product)
               .filter(models.Cart_Product.cart_id==db_user.id,
                       models.Cart_Product.product_id==db_item.id)
               .first())
    if not db_link:
        new_link = models.Cart_Product(
            cart_id = db_user.id,
            product_id = db_item.id,
            quantity = quantity
        )
        session.add(new_link)

    if db_link:
        db_link.quantity += quantity
    
    db_item.stock -= quantity

    session.commit()
    session.refresh(db_user.cart)
    return db_user.cart

#===============================
    #REMOVE ITEM FROM CART
#===============================
@router.put("/cart/products/{product_id}")
def remove_item_from_cart(product_id: int, 
                        user = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    db_user = session.get(models.User,user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    db_item = session.get(models.Product,product_id)
    if not db_item:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    db_link = (session.query(models.Cart_Product)
               .filter(models.Cart_Product.cart_id==user.id,
                       models.Cart_Product.product_id==db_item.id)
               .first())
    if not db_link:
        raise HTTPException(status_code=404,detail="Item is not in the cart!")
    
    session.delete(db_link)

    db_item.stock += db_link.quantity
    
    session.commit()
    session.refresh(db_user.cart)
    return {"message":f"{db_item.name} is removed from the cart successfully!"}

#===============================
    #CHECKOUT ITEMS FROM CART
#===============================
@router.post("/cart")
def checkout(product_id_list: list[int],
            order: schemas.Order_Create,
            user = Depends(get_current_user),
            session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    #GET ALL THE ITEMS FROM THE CURRENT USER'S CART
    cart_products = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==db_user.id).all()

    #MATCH THE SELECTED ITEMS TO CHECK OUT
    for product_id in product_id_list:
        for cart_product in cart_products:
            if product_id == cart_product.product_id:
                new_order = models.Order(
                    user_id = db_user.id,
                    payment_method = order.payment_method,
                    payment_status = order.payment_status,
                )
                new_order.order_products = [models.Order_Product(
                    product_id = cart_product.product_id,
                    quantity = cart_product.quantity
                )]
                cart_product_link = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==db_user.id,
                                                                              models.Cart_Product.product_id==product_id).first()
                session.delete(cart_product_link)
                session.add(new_order)
                session.flush()

    session.commit()
    return {"message":"Checkout successful!"}

#===============================
    #CHECKOUT ALL ITEMS FROM CART
#===============================
@router.post("/cart/{cart_id}")
def checkout_all_items(cart_id: int,
                order: schemas.Order_Create,
                user = Depends(get_current_user),
                session: Session = Depends(get_session)):
    
    db_user = session.get(models.User,user.id)
    if not db_user:
        raise HTTPException(status_code=404,detail="User not logged in!")
    
    #GET ALL THE ITEMS FROM THE CURRENT USER'S CART
    cart_products = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==db_user.id).all()

    for cart_product in cart_products:
        new_order = models.Order(
            user_id = db_user.id,
            payment_method = order.payment_method,
            payment_status = order.payment_status,
        )
        new_order.order_products = [models.Order_Product(
            product_id = cart_product.product_id,
            quantity = cart_product.quantity
        )]
        cart_product_link = session.query(models.Cart_Product).filter(models.Cart_Product.cart_id==db_user.id,
                                                                    models.Cart_Product.product_id==cart_product.product_id).first()
        session.delete(cart_product_link)
        session.add(new_order)
        session.flush()

    session.commit()
    return {"message":"Checkout successful!"}