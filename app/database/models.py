from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Integer,Column,ForeignKey,Float,UniqueConstraint,DateTime,JSON,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from app.database.database import engine

Base = declarative_base()

#============================================
                # USER
#============================================
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer,primary_key=True,nullable=False,unique=True,index=True,autoincrement=True)
    role = Column(String,default="user")
    username = Column(String)
    email = Column(String)
    password = Column(String)

    fullname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    occupation = Column(String)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    cart = relationship("Cart",back_populates="user",uselist=False,cascade="all, delete-orphan")
    orders = relationship("Order",back_populates="user",cascade="all, delete-orphan")

#============================================
                # CART
#============================================
class Cart(Base):
    __tablename__ = "Carts"

    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),primary_key=True,unique=True,nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User",back_populates="cart",uselist=False)
    cart_products = relationship("Cart_Product",back_populates="cart")

#============================================
        # LINK BETWEEN CART AND PRODUCT
        # FOR MANY TO MANY RELATIONSHIP
#============================================
class Cart_Product(Base):
    __tablename__ = "Cart_Products"
    __table_args__ = (UniqueConstraint("cart_id","product_id",name="uq_cart_product"),)

    id = Column(Integer,primary_key=True,nullable=False,unique=True,index=True,autoincrement=True)
    cart_id = Column(Integer,ForeignKey("Carts.user_id",ondelete="CASCADE"),unique=False,nullable=False)
    product_id = Column(Integer,ForeignKey("Products.id",ondelete="CASCADE"),unique=False,nullable=False)
    quantity = Column(Integer)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    cart = relationship("Cart",back_populates="cart_products")
    product = relationship("Product",back_populates="product_carts")

#============================================
                # ORDER
#============================================
class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer,primary_key=True,nullable=False,unique=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),unique=False,nullable=False)
    status = Column(String,default="pending")
    payment_method = Column(String,default=None)
    payment_status = Column(String,default=None)

    ordered_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User",back_populates="orders",uselist=False)
    order_products = relationship("Order_Product",back_populates="order")

#============================================
        # LINK BETWEEN ORDER AND PRODUCT
        # FOR MANY TO MANY RELATIONSHIP
#============================================
class Order_Product(Base):
    __tablename__ = "Order_Products"
    __table_args__ = (UniqueConstraint("order_id","product_id",name="uq_order_product"),)

    id = Column(Integer,primary_key=True,nullable=False,unique=True,index=True,autoincrement=True)
    order_id = Column(Integer,ForeignKey("Orders.id",ondelete="CASCADE"),unique=True,nullable=False)
    product_id = Column(Integer,ForeignKey("Products.id",ondelete="CASCADE"),unique=False,nullable=False)
    quantity = Column(Integer)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    order = relationship("Order",back_populates="order_products")
    product = relationship("Product",back_populates="product_orders")

#============================================
                # PRODUCT
#============================================
class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer,primary_key=True,nullable=False,unique=True,index=True,autoincrement=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product_carts = relationship("Cart_Product",back_populates="product")
    product_orders = relationship("Order_Product",back_populates="product")

Base.metadata.create_all(bind=engine)