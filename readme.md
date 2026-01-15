# E-Ticaret REST API  
**FastAPI + SQLite | Yazılım Kalite Güvencesi ve Testi Dersi Projesi**

Bu depo, **Yazılım Kalite Güvencesi ve Testi** doktora dersi kapsamında geliştirilmiş bir **REST tabanlı E-Ticaret API** projesini içermektedir.  
Projenin temel amacı; **API geliştirme, otomatik test süreçleri, test türleri (Unit / Integration / System), kapsama (coverage) analizi ve CI (Continuous Integration)** kavramlarını uygulamalı olarak göstermektir.

---

## 📌 Proje Özellikleri
- **5 adet REST kaynağı (resource):**
  - `users`
  - `categories`
  - `products`
  - `orders`
  - `reviews`
- SQLite veritabanı
- Kaynaklar arası ilişkiler (Category–Product, User–Order, User/Product–Review)
- Tüm kaynaklar için CRUD işlemleri
- Swagger / OpenAPI dokümantasyonu
- Otomatik test altyapısı:
  - Unit Testler
  - Integration Testler
  - Sistem / Uçtan Uca (E2E) Testler
- Kod kapsama (coverage) analizi
- GitHub Actions ile CI (Sürekli Entegrasyon)
- Windows işletim sistemi ile uyumlu yapı

---

## 🛠️ Kullanılan Teknolojiler
- **FastAPI**
- **SQLite**
- **SQLAlchemy**
- **Pytest**
- **pytest-cov**
- **GitHub Actions**

---

## ▶️ Projeyi Çalıştırma

### 1️⃣ Gerekli paketleri yükleyin
```bash
pip install -r requirements.txt

2️⃣ API sunucusunu başlatın
uvicorn app.main:app --reload

3️⃣ Tarayıcıdan erişim
  Swagger Arayüzü: http://127.0.0.1:8000/docs
  Sağlık Kontrolü: http://127.0.0.1:8000/health

🧪 Testleri Çalıştırma

Tüm testleri çalıştırma
  python -m pytest

Testleri kapsama analizi ile çalıştırma
  python -m pytest --cov=app --cov-report=term-missing
  Mevcut toplam kod kapsama oranı: ~%88

🧩 Test Türleri

Unit Testler
  İş mantığı ve yardımcı fonksiyonların test edilmesi
  tests/unit

Integration Testler
  API uç noktalarının veritabanı ile birlikte test edilmesi
  tests/integration

Sistem / Uçtan Uca (E2E) Testler
  Gerçek kullanıcı senaryolarının uçtan uca test edilmesi
  tests/e2e

🔄 Sürekli Entegrasyon (CI)
Projede GitHub Actions kullanılarak CI hattı oluşturulmuştur.
Her push ve pull request işleminde:
  Bağımlılıklar yüklenir
  Tüm testler otomatik olarak çalıştırılır
  Kapsama (coverage) raporu üretilir
CI işlemleri Windows runner üzerinde gerçekleştirilmektedir.

👤 Yazar

Emrullah Polat
Bilgisayar Mühendisliği – Doktora Öğrencisi - Erciyes Üniversitesi