import pytest
from tests.conftest import client



class TestCategoryEndpoints:
    """Тести endpoints для категорій"""

    @pytest.mark.asyncio
    async def test_create_category_success(self, client):
        """Тест створення категорії"""
        category_data = {"name": "Electronics"}
        response = await client.post("/store/categories/", json=category_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Electronics"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_multiple_categories(self, client):
        """Тест створення декількох категорій"""
        cat1 = {"name": "Electronics"}
        cat2 = {"name": "Books"}
        cat3 = {"name": "Clothing"}
        
        resp1 = await client.post("/store/categories/", json=cat1)
        resp2 = await client.post("/store/categories/", json=cat2)
        resp3 = await client.post("/store/categories/", json=cat3)
        
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        assert resp3.status_code == 200
        
        assert resp1.json()["name"] == "Electronics"
        assert resp2.json()["name"] == "Books"
        assert resp3.json()["name"] == "Clothing"


class TestProductEndpoints:
    """Тести endpoints для товарів"""

    @pytest.mark.asyncio
    async def test_create_product_success(self, client):
        """Тест створення товару"""
        # Спочатку створюємо категорію
        category_data = {"name": "Electronics"}
        cat_response = await client.post("/store/categories/", json=category_data)
        category_id = cat_response.json()["id"]
        
        # Потім створюємо товар
        product_data = {
            "title": "Laptop",
            "price": 999.99,
            "category_id": category_id
        }
        response = await client.post("/store/products/", json=product_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Laptop"
        assert data["price"] == 999.99
        assert data["category_id"] == category_id
        assert "id" in data

    @pytest.mark.asyncio
    async def test_get_all_products_empty(self, client):
        """Тест отримання всіх товарів з пустої БД"""
        response = await client.get("/store/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.asyncio
    async def test_get_all_products(self, client):
        """Тест отримання всіх товарів"""
        # Створюємо категорію
        category_data = {"name": "Electronics"}
        cat_response = await client.post("/store/categories/", json=category_data)
        category_id = cat_response.json()["id"]
        
        # Створюємо товари
        prod1 = {
            "title": "Laptop",
            "price": 999.99,
            "category_id": category_id
        }
        prod2 = {
            "title": "Phone",
            "price": 499.99,
            "category_id": category_id
        }
        prod3 = {
            "title": "Tablet",
            "price": 299.99,
            "category_id": category_id
        }
        
        await client.post("/store/products/", json=prod1)
        await client.post("/store/products/", json=prod2)
        await client.post("/store/products/", json=prod3)
        
        # Отримуємо всі
        response = await client.get("/store/products/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        titles = [p["title"] for p in data]
        assert "Laptop" in titles
        assert "Phone" in titles
        assert "Tablet" in titles

    @pytest.mark.asyncio
    async def test_create_product_different_categories(self, client):
        """Тест створення товарів у різних категоріях"""
        # Створюємо категорії
        cat_elec = {"name": "Electronics"}
        cat_books = {"name": "Books"}
        
        resp_elec = await client.post("/store/categories/", json=cat_elec)
        resp_books = await client.post("/store/categories/", json=cat_books)
        
        elec_id = resp_elec.json()["id"]
        books_id = resp_books.json()["id"]
        
        # Створюємо товари в різних категоріях
        prod_elec = {
            "title": "Laptop",
            "price": 999.99,
            "category_id": elec_id
        }
        prod_book = {
            "title": "Python Programming",
            "price": 49.99,
            "category_id": books_id
        }
        
        resp1 = await client.post("/store/products/", json=prod_elec)
        resp2 = await client.post("/store/products/", json=prod_book)
        
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        
        assert resp1.json()["category_id"] == elec_id
        assert resp2.json()["category_id"] == books_id

    @pytest.mark.asyncio
    async def test_create_product_with_different_prices(self, client):
        """Тест створення товарів з різними цінами"""
        # Створюємо категорію
        category_data = {"name": "Store"}
        cat_response = await client.post("/store/categories/", json=category_data)
        category_id = cat_response.json()["id"]
        
        # Створюємо товари з різними цінами
        prices = [0.99, 10.00, 100.50, 1000.00]
        
        for i, price in enumerate(prices):
            product_data = {
                "title": f"Product {i+1}",
                "price": price,
                "category_id": category_id
            }
            response = await client.post("/store/products/", json=product_data)
            assert response.status_code == 200
            assert response.json()["price"] == price

    @pytest.mark.asyncio
    async def test_get_products_with_category_relationship(self, client):
        """Тест отримання товарів з їх категоріями"""
        # Створюємо категорію
        category_data = {"name": "Electronics"}
        cat_response = await client.post("/store/categories/", json=category_data)
        category_id = cat_response.json()["id"]
        
        # Створюємо товар
        product_data = {
            "title": "Laptop",
            "price": 999.99,
            "category_id": category_id
        }
        await client.post("/store/products/", json=product_data)
        
        # Отримуємо всі товари
        response = await client.get("/store/products/")
        assert response.status_code == 200
        
        products = response.json()
        assert len(products) == 1
        assert products[0]["category_id"] == category_id

