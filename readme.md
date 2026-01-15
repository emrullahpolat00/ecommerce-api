# E-Ticaret REST API
![CI](https://github.com/emrullahpolat00/ecommerce-api/actions/workflows/ci.yml/badge.svg)

FastAPI + SQLite  
Yazılım Kalite Güvencesi ve Testi (Doktora) Dersi Projesi

Bu proje, Yazılım Kalite Güvencesi ve Testi doktora dersi kapsamında geliştirilmiş bir REST tabanlı E-Ticaret API uygulamasıdır. Projenin amacı; REST API geliştirme sürecinde test türlerinin (Unit, Integration, Sistem/Uçtan Uca), kod kapsama analizinin ve CI/CD süreçlerinin uygulamalı olarak gösterilmesidir.

---

## 1. Proje Açıklaması ve Kullanılan Teknolojiler

Proje, bir e-ticaret sisteminin temel işlevlerini sağlayan REST servislerinden oluşmaktadır. Kullanıcılar, ürünler, kategoriler, siparişler ve değerlendirmeler için CRUD (Create, Read, Update, Delete) işlemleri sunulmaktadır.

Kullanılan teknolojiler:
- FastAPI
- SQLite
- SQLAlchemy
- Pytest
- pytest-cov
- GitHub Actions

---

## 2. Kurulum Talimatları 

### 2.1 Gerekli Yazılımlar
- Python 3.11 veya üzeri
- Git

### 2.2 Projenin İndirilmesi

    git clone https://github.com/emrullahpolat00/ecommerce-api.git
    cd ecommerce-api

### 2.3 Gerekli Paketlerin Kurulması

    pip install -r requirements.txt

### 2.4 API Sunucusunun Çalıştırılması

    uvicorn app.main:app --reload

Uygulama varsayılan olarak aşağıdaki adreste çalışır:

    http://127.0.0.1:8000

---

## 3. API Endpoint Listesi ve Kullanım Örnekleri

### 3.1 Users
- GET /users
- GET /users/{id}
- POST /users
- PUT /users/{id}
- DELETE /users/{id}

Örnek POST isteği:

    {
      "email": "user@example.com",
      "full_name": "Test User"
    }

---

### 3.2 Categories
- GET /categories
- GET /categories/{id}
- POST /categories
- PUT /categories/{id}
- DELETE /categories/{id}

Örnek POST isteği:

    {
      "name": "Electronics"
    }

---

### 3.3 Products
- GET /products
- GET /products/{id}
- POST /products
- PUT /products/{id}
- DELETE /products/{id}

Örnek POST isteği:

    {
      "name": "Laptop",
      "price": 25000,
      "category_id": 1
    }

---

### 3.4 Orders
- GET /orders
- GET /orders/{id}
- POST /orders
- DELETE /orders/{id}

Örnek POST isteği:

    {
      "user_id": 1,
      "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
      ]
    }

---

### 3.5 Reviews
- GET /reviews
- GET /reviews/{id}
- POST /reviews
- PUT /reviews/{id}
- DELETE /reviews/{id}

Örnek POST isteği:

    {
      "user_id": 1,
      "product_id": 1,
      "rating": 5,
      "comment": "Ürün çok iyi"
    }

---

## 4. Swagger / OpenAPI Dokümantasyonu

FastAPI tarafından otomatik olarak üretilen Swagger / OpenAPI dokümantasyonuna aşağıdaki URL üzerinden erişilebilir:

    http://127.0.0.1:8000/docs

---

## 5. Testlerin Çalıştırılması

Tüm testleri çalıştırmak için:

    python -m pytest

Kapsama (coverage) analizi ile testleri çalıştırmak için:

    python -m pytest --cov=app --cov-report=term-missing

Projedeki mevcut toplam kod kapsama oranı yaklaşık %88’dir.

---

## 6. Test Türleri

- Unit Testler: tests/unit
- Integration Testler: tests/integration
- Sistem / Uçtan Uca (E2E) Testler: tests/e2e

---

## 7. CI/CD Süreci

Projede GitHub Actions kullanılarak bir CI (Continuous Integration) hattı oluşturulmuştur. Her push ve pull request işleminde testler otomatik olarak çalıştırılmakta ve kapsama raporu üretilmektedir.

---

## Yazar

Emrullah Polat  
Bilgisayar Mühendisliği – Doktora Öğrencisi - Erciyes Üniversitesi
