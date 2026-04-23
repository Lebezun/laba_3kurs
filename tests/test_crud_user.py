import pytest
from httpx import AsyncClient
from app.schemas.user import UserCreate


class TestUserCRUDViaAPI:
    """Тести CRUD операцій для користувачів через API"""

    @pytest.mark.asyncio
    async def test_create_user_via_registration(self, client):
        """Тест створення користувача через реєстрацію"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = await client.post("/users/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] is not None
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_user_via_me(self, client):
        """Тест отримання користувача через /me endpoint"""
        # Реєстрація
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        await client.post("/users/register", json=user_data)
        
        # Логін
        login_data = {"username": "testuser", "password": "password123"}
        await client.post("/users/login", data=login_data)

        # Отримання користувача
        response = await client.get("/users/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_duplicate_email_error(self, client):
        """Тест помилки при реєстрації з дублюючим email"""
        user_data = {
            "username": "user1",
            "email": "test@example.com",
            "password": "password123"
        }
        await client.post("/users/register", json=user_data)
        
        # Спробуємо створити користувача з тим же email
        user_data2 = {
            "username": "user2",
            "email": "test@example.com",
            "password": "password456"
        }
        response = await client.post("/users/register", json=user_data2)
        
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, client):
        """Тест аутентифікації з неправильним паролем"""
        # Реєстрація
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        await client.post("/users/register", json=user_data)
        
        # Спробуємо логін з неправильним паролем
        login_data = {"username": "testuser", "password": "wrongpassword"}
        response = await client.post("/users/login", data=login_data)
        
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_multiple_users_registration(self, client):
        """Тест реєстрації декількох користувачів"""
        users = [
            {"username": "user1", "email": "user1@example.com", "password": "pass1"},
            {"username": "user2", "email": "user2@example.com", "password": "pass2"},
            {"username": "user3", "email": "user3@example.com", "password": "pass3"},
        ]
        
        for user in users:
            response = await client.post("/users/register", json=user)
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == user["username"]
            assert data["email"] == user["email"]

    @pytest.mark.asyncio
    async def test_unauthorized_access_to_me(self, client):
        """Тест доступу до /me без авторизації"""
        response = await client.get("/users/me")
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_invalid_username(self, client):
        """Тест логіну з неіснуючим користувачем"""
        login_data = {"username": "nonexistent", "password": "password123"}
        response = await client.post("/users/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

