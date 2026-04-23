from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.database import Category, Product
from app.schemas.product import CategoryCreate, ProductCreate 


async def create_category(db: AsyncSession, category: CategoryCreate):
    """Створює нову категорію"""
    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_category_by_id(db: AsyncSession, category_id: int):
    """Отримує категорію за ID"""
    result = await db.execute(select(Category).filter(Category.id == category_id))
    return result.scalars().first()


async def get_category_by_name(db: AsyncSession, name: str):
    """Отримує категорію за назвою"""
    result = await db.execute(select(Category).filter(Category.name == name))
    return result.scalars().first()


async def get_all_categories(db: AsyncSession):
    """Отримує всі категорії"""
    result = await db.execute(select(Category))
    return result.scalars().all()


async def create_product(db: AsyncSession, product: ProductCreate):
    """Створює новий товар"""
    db_product = Product(
        title=product.title, 
        price=product.price, 
        category_id=product.category_id
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_product_by_id(db: AsyncSession, product_id: int):
    """Отримує товар за ID"""
    result = await db.execute(select(Product).filter(Product.id == product_id))
    return result.scalars().first()


async def get_products(db: AsyncSession):
    """Отримує всі товари"""
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_products_by_category(db: AsyncSession, category_id: int):
    """Отримує товари за категорією"""
    result = await db.execute(select(Product).filter(Product.category_id == category_id))
    return result.scalars().all()


async def update_product_price(db: AsyncSession, product_id: int, new_price: float):
    """Оновлює ціну товару"""
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product:
        product.price = new_price
        await db.commit()
        await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: int):
    """Видаляє товар"""
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product:
        await db.delete(product)
        await db.commit()
    return product


async def delete_category(db: AsyncSession, category_id: int):
    """Видаляє категорію"""
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalars().first()
    if category:
        await db.delete(category)
        await db.commit()
    return category
