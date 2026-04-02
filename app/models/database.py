from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

# 1. Модель Юзера
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Зв'язки
    profile = relationship("Profile", back_populates="user", uselist=False) # One-to-One
    orders = relationship("Order", back_populates="user") # One-to-Many

# 2. Модель Профілю (One-to-One з Юзером)
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True) # unique=True робить зв'язок 1 до 1

    user = relationship("User", back_populates="profile")

# 3. Модель Категорії
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship("Product", back_populates="category") # One-to-Many

# 4. Модель Товару (Many-to-One з Категорією)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

# 5. Модель Замовлення (Many-to-One з Юзером)
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")