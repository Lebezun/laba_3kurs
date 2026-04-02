from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.database import Category, Product
# Якщо виніс в окремий файл, імпортуй схеми звідти:
from app.schemas.product import CategoryCreate, ProductCreate 

async def create_category(db: AsyncSession, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(title=product.title, price=product.price, category_id=product.category_id)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()