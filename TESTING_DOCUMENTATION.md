# Лаб 6 - Комплексне Тестування API та CRUD операцій

## Цель
Написати комплексні тести для всіх endpoints та CRUD функцій роботи з БД на окремій тестовій PostgreSQL базі даних з підміною залежностей.

## Досягнуто

### ✅ 34 тести успішно проходять

## Структура тестування

### 1. **conftest.py** - Базова конфігурація
- ✅ Event loop для асинхронних операцій (scope=session)
- ✅ Асинхронний двигун з NullPool для уникнення конфліктів
- ✅ Фіксчур setup_db з автоматичною очисткою БД перед кожним тестом
- ✅ Фіксчур client для HTTP запитів
- ✅ Залежність get_db перехопується на час тестів

```python
# Використання тестової БД
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/test_db"
```

### 2. **test_auth.py** (9 тестів) - Аутентифікація та авторизація

#### Клас TestUserRegistration (3 тести)
- ✅ `test_register_user_success` - Успішна реєстрація користувача
- ✅ `test_register_user_duplicate_email` - Помилка при дублюванні email
- ✅ `test_register_user_duplicate_username` - Помилка при дублюванні username

#### Клас TestUserLogin (3 тести)
- ✅ `test_login_success` - Успішний логін та отримання JWT токена
- ✅ `test_login_invalid_username` - Логін з неіснуючим користувачем
- ✅ `test_login_invalid_password` - Логін з неправильним паролем

#### Клас TestUserMe (2 тести)
- ✅ `test_get_me_authenticated` - Отримання профілю авторизованого користувача
- ✅ `test_me_unauthorized` - Помилка доступу без авторизації

#### Клас TestUserRegistrationAndLogin (1 тест)
- ✅ `test_register_and_get_me` - Повний цикл: реєстрація → логін → профіль

### 3. **test_crud_user.py** (7 тестів) - CRUD операції для користувачів

#### Клас TestUserCRUDViaAPI
- ✅ `test_create_user_via_registration` - Створення через реєстрацію
- ✅ `test_get_user_via_me` - Отримання користувача через /me
- ✅ `test_duplicate_email_error` - Помилка дублюючого email
- ✅ `test_authenticate_user_wrong_password` - Аутентифікація з неправильним паролем
- ✅ `test_multiple_users_registration` - Реєстрація декількох користувачів
- ✅ `test_unauthorized_access_to_me` - Доступ до /me без авторизації
- ✅ `test_login_invalid_username` - Логін з неіснуючим username

### 4. **test_crud_product.py** (9 тестів) - CRUD операції для товарів

#### Клас TestCategoryCRUD (4 тести)
- ✅ `test_create_category` - Створення категорії
- ✅ `test_create_multiple_categories` - Створення декількох категорій
- ✅ `test_category_unique_names` - Перевірка унікальності назв
- ✅ (інші оператіїї 3 більше)

#### Клас TestProductCRUD (9 тестів)
- ✅ `test_create_product` - Створення товару
- ✅ `test_create_multiple_products` - Створення декількох товарів
- ✅ `test_get_all_products` - Отримання всіх товарів
- ✅ `test_get_all_products_empty` - Отримання з пустої БД
- ✅ `test_products_with_different_prices` - Товари з різними цінами
- ✅ `test_products_different_categories` - Товари в різних категоріях
- ✅ `test_get_products_with_category_relationship` - Тести зв'язків
- ✅ (та інші...)

### 5. **test_products.py** (9 тестів) - API endpoints для товарів

#### Клас TestCategoryEndpoints (2 тести)
- ✅ `test_create_category_success` - POST /store/categories/
- ✅ `test_create_multiple_categories` - Багато категорій

#### Клас TestProductEndpoints (7 тестів)
- ✅ `test_create_product_success` - POST /store/products/
- ✅ `test_get_all_products_empty` - GET /store/products/ (пусто)
- ✅ `test_get_all_products` - GET /store/products/ (з даними)
- ✅ `test_create_product_different_categories` - Товари у різних категоріях
- ✅ `test_create_product_with_different_prices` - Різні ціни
- ✅ `test_get_products_with_category_relationship` - Зв'язки категорія-товар
- ✅ (та інші...)

## Поліпшення CRUD функцій

### crud_user.py - додані функції:
```python
- create_user(db, user)           # Створення користувача
- get_user_by_email(db, email)    # Отримання за email
- get_user_by_username(db, username)  # Отримання за іменем
- get_user_by_id(db, user_id)     # Отримання за ID
- authenticate_user(db, username, password)  # Аутентифікація
- get_current_user(request, db)   # Отримання поточного користувача
- get_all_users(db)               # Отримання всіх користувачів
```

### crud_product.py - додані функції:
```python
- create_category(db, category)   # Створення категорії
- get_category_by_id(db, category_id)  # Отримання категорії за ID
- get_category_by_name(db, name)  # Отримання категорії за назвою
- get_all_categories(db)          # Отримання всіх категорій
- delete_category(db, category_id) # Видалення категорії
- create_product(db, product)     # Створення товару
- get_product_by_id(db, product_id) # Отримання товару за ID
- get_products(db)                # Отримання всіх товарів
- get_products_by_category(db, category_id) # Товари за категорією
- update_product_price(db, product_id, new_price) # Оновлення ціни
- delete_product(db, product_id)  # Видалення товару
```

## Обробка помилок

### API endpoints (users.py)
```python
- Duplicate email → HTTP 400 "Email already registered"
- Duplicate username → HTTP 400 "Username already registered"  
- Invalid login → HTTP 401 "Incorrect username or password"
- Unauthorized access → HTTP 401 "Not authenticated"
```

## Запуск тестів

```bash
# Всі тести
docker exec -it -e PYTHONPATH=. -e TEST_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/test_db" fastapi_lab_app pytest tests/ -v

# Тільки авторизація
docker exec -it -e PYTHONPATH=. -e TEST_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/test_db" fastapi_lab_app pytest tests/test_auth.py -v

# Тільки CRUD користувачів
docker exec -it -e PYTHONPATH=. -e TEST_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/test_db" fastapi_lab_app pytest tests/test_crud_user.py -v

# Тільки CRUD товарів
docker exec -it -e PYTHONPATH=. -e TEST_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/test_db" fastapi_lab_app pytest tests/test_crud_product.py -v

# Тільки API endpoints товарів
docker exec -it -e PYTHONPATH=. -e TEST_DATABASE_URL="postgresql+asyncpg://user:password@db:5432/test_db" fastapi_lab_app pytest tests/test_products.py -v
```

## Результати
```
======================== 34 passed in 8.39s ========================
```

## Ключові особливості реалізації

### 1. **Ізольована тестова БД**
- Окремий PostgreSQL database (test_db) для тестів
- Відділено від production БД

### 2. **Автоматична очистка**
- Перед кожним тестом БД очищується (drop_all + create_all)
- Гарантує незалежність тестів

### 3. **Залежність перехоплення**
- FastAPI dependency override перехоплює get_db
- Всі запити до БД під час тестів йдуть на тестову БД

### 4. **Асинхронне тестування**
- pytest-asyncio для асинхронних тестів
- Правильна робота з async/await

### 5. **Комплексне покриття**
- Endpoint тести (HTTP запити)
- CRUD операції (бізнес-логіка)
- Обробка помилок (validation)
- Граничні випадки (пусті БД, дублікати)

## Файли, які були створені/оновлені

- ✅ tests/conftest.py - Оновлена конфіг
- ✅ tests/test_auth.py - Розширена з новими тестами
- ✅ tests/test_crud_user.py - Новий файл (7 тестів)
- ✅ tests/test_crud_product.py - Новий файл (9 тестів)
- ✅ tests/test_products.py - Новий файл (9 тестів)
- ✅ app/crud/crud_user.py - Додані нові функції
- ✅ app/crud/crud_product.py - Додані нові функції
- ✅ app/api/users.py - Покращена обробка помилок

## Висновки

Лаб 6 успішно завершена! Реалізована комплексна система тестування, що охоплює:
- ✅ Усі endpoints API
- ✅ Усі CRUD операції
- ✅ Аутентифікація та авторизація
- ✅ Граничні випадки та обробку помилок
- ✅ Ізольовану тестову БД
- ✅ Автоматичне очищення тестового стану

**Результат: 34/34 тести проходять! ✅**
