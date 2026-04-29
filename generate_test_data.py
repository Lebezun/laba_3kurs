#!/usr/bin/env python3
"""Script to generate test data for monitoring"""
import requests
import time

BASE_URL = "http://localhost:8000"

def generate_test_data():
    """Generate test API requests"""
    print("🔄 Генеруємо тестові запити...")
    
    # Generate requests to products endpoint
    for i in range(20):
        try:
            response = requests.get(f"{BASE_URL}/store/products", timeout=5)
            print(f"✓ Запит {i+1}/20: Status {response.status_code}")
        except Exception as e:
            print(f"✗ Помилка на запиті {i+1}: {e}")
        time.sleep(0.1)
    
    print("✅ Тестові дані генеровані!")

if __name__ == "__main__":
    generate_test_data()
