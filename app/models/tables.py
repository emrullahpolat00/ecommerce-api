from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """
    Resource olarak expose etmiyoruz. Order içindeki ürünleri tutan ara tablo.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    __table_args__ = (UniqueConstraint("order_id", "product_id", name="uq_order_product"),)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1..5
    comment = Column(Text, nullable=True)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product_review"),)