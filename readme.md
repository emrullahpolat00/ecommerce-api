# Ecommerce API  
**FastAPI + SQLite | Software Quality Assurance & Testing Project**

This repository contains a RESTful E-commerce API developed as part of the **Software Quality Assurance and Testing (PhD level)** course.  
The project focuses on **API design, automated testing (Unit / Integration / E2E), coverage analysis, and CI pipelines**.

---

## 📌 Features
- REST API with **5 resources**:
  - `users`
  - `categories`
  - `products`
  - `orders`
  - `reviews`
- SQLite database with relational structure
- Full CRUD operations
- Swagger / OpenAPI documentation
- Automated testing:
  - Unit tests
  - Integration tests
  - End-to-End (System) tests
- Code coverage analysis
- Continuous Integration with **GitHub Actions**
- Windows-compatible setup

---

## 🛠️ Technologies
- **FastAPI**
- **SQLite**
- **SQLAlchemy**
- **Pytest**
- **pytest-cov**
- **GitHub Actions**

---

## ▶️ Run Locally

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt

2️⃣ Start the API server
uvicorn app.main:app --reload

3️⃣ Open in browser

Swagger UI: http://127.0.0.1:8000/docs
Health Check: http://127.0.0.1:8000/health

🧪 Run Tests
Run all tests
python -m pytest

Run tests with coverage
python -m pytest --cov=app --cov-report=term-missing
Current total coverage: ~88%

🧩 Test Types

Unit Tests
Location:
tests/unit

Integration Tests
Location:
tests/integration

End-to-End (System) Tests
Location:
    tests/e2e

🔄 Continuous Integration (CI)
    GitHub Actions pipeline automatically runs:
        Dependency installation
        All tests
        Coverage reporting
    CI is executed on Windows runner
    Pipeline status can be viewed under the Actions tab


👤 Author

Emrullah Polat
PhD Student – Computer Engineering - Erciyes University