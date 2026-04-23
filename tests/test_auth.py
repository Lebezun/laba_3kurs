import pytest
from tests.conftest import client


class TestUserRegistration:
    """Тести реєстрації користувачів"""

    @pytest.mark.asyncio
    async def test_register_user_success(self, client):
        """Тест успішної реєстрації"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        response = await client.post("/users/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, client):
        """Тест реєстрації з дублюючим email"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        # Перший користувач
        await client.post("/users/register", json=user_data)
        
        # Другий з тим же email
        user_data2 = {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "password456"
        }
        response = await client.post("/users/register", json=user_data2)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_user_duplicate_username(self, client):
        """Тест реєстрації з дублюючим username"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        await client.post("/users/register", json=user_data)
        
        # Другий з тим же username
        user_data2 = {
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password456"
        }
        response = await client.post("/users/register", json=user_data2)
        # БД повинна повернути помилку через UniqueConstraint
        assert response.status_code != 200


class TestUserLogin:
    """Тести логіну та аутентифікації"""

    @pytest.mark.asyncio
    async def test_login_success(self, client):
        """Тест успішного логіну"""
        # Реєстрація
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        await client.post("/users/register", json=user_data)
        
        # Логін
        login_data = {"username": "testuser", "password": "password123"}
        response = await client.post("/users/login", data=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_username(self, client):
        """Тест логіну з неправильним іменем"""
        login_data = {"username": "nonexistent", "password": "password123"}
        response = await client.post("/users/login", data=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client):
        """Тест логіну з неправильним паролем"""
        # Реєстрація
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        await client.post("/users/register", json=user_data)
        
        # Логін з неправильним паролем
        login_data = {"username": "testuser", "password": "wrongpassword"}
        response = await client.post("/users/login", data=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]


class TestUserMe:
    """Тести отримання поточного користувача"""

    @pytest.mark.asyncio
    async def test_get_me_authenticated(self, client):
        """Тест отримання профілю авторизованого користувача"""
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

        # Отримання профілю
        response = await client.get("/users/me")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_me_unauthorized(self, client):
        """Тест отримання профілю без авторизації"""
        response = await client.get("/users/me")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestUserRegistrationAndLogin:
    """Інтеграційні тести повного цикла реєстрація-логін"""

    @pytest.mark.asyncio
    async def test_register_and_get_me(self, client):
        """Тест повного цикла: реєстрація -> логін -> профіль"""
        user_data = {
            "username": "testuser",
            "email": "test@mail.com",
            "password": "secretpassword"
        }
        reg_response = await client.post("/users/register", json=user_data)
        assert reg_response.status_code == 200
        
        # Тест логіну (отримання куки)
        login_data = {"username": "testuser", "password": "secretpassword"}
        login_response = await client.post("/users/login", data=login_data)
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

        # Тест ручки /me (Авторизація)
        me_response = await client.get("/users/me")
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "test@mail.com"
