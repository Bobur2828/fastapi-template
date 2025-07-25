# 🚀 FastAPI Ilovasi

Bu loyiha `FastAPI` asosida ishlab chiqilgan zamonaviy, modulli backend ilova bo‘lib, PostgreSQL yoki SQLite bilan ishlash, JWT himoya, asinxron ishlov, va modulli arxitektura bilan jihozlangan.

---

## 📁 Loyiha tuzilmasi


```
app/
├── app.py # Ilovaning ishga tushish nuqtasi
├── core/ # Yadro konfiguratsiyasi
│ ├── settings.py # Muhit sozlamalari (pydantic)
│ ├── db.py # Ma'lumotlar bazasi konfiguratsiyasi
│ ├── logger.py # Loglash konfiguratsiyasi
│ └── dependencies.py # Umumiy bog‘liqliklar
├── middleware/ # Middleware komponentlar
│ ├── error_handler.py # Xatolarni ushlash
│ ├── logging.py # So‘rov loglash
│ └── cors.py # CORS sozlamalari
├── shared/ # Umumiy sxemalar va modellar
│ ├── schemas/ # Bazaviy Pydantic sxemalar
│ └── models/ # Bazaviy SQLAlchemy modellar
├── modules/ # Biznes modullar
│ └── echo/ # Misol modul
├── utils/ # Yordamchi funksiyalar
└── logs/ # Log fayllar
```

## Установка и запуск

## ⚙️ O‘rnatish va ishga tushirish

### 🖥️ Lokal usulda

```bash
# Virtual muhit yaratish
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# Bog‘liqliklarni o‘rnatish
pip install -r requirements.txt

# .env faylini yaratish
cp .env.example .env
# .env faylini tahrir qiling

# Ilovani ishga tushirish
uvicorn app:app --reload

# Docker Compose orqali Baza bilan
docker-compose up -d

# Faqat ilovani ishga tushirish
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app


### API hujjatlari

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


```bash
# Ochiq endpoint
curl -X POST http://localhost:8000/api/echo/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Salom Dunyo"}'

# Himoyalangan endpoint (Bearer token talab qilinadi)
curl -X POST http://localhost:8000/api/echo/protected \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sizning-tokeningiz" \
     -d '{"message": "Himoyalangan salom"}'
```

## Dasturlash

### Yangi modul yaratish

1. modules/ papkasida yangi papka yarating
2. Quyidagi fayllarni yarating: router.py, schemas.py, services.py, models.py
3. app.py faylida yangi router'ni ulang

### Ma'lumotlar bazasi bilan ishlash

```bash
# Yangi migratsiya yaratish
make db-revision MSG="O‘zgarishlar tavsifi"

# Migratsiyalarni qo‘llash
make db-upgrade

# Migratsiyani bekor qilish
make db-downgrade
```

## Sozlamalar

Barcha sozlamalar .env faylida saqlanadi:

- `APP_DATABASE_URL` - Ma'lumotlar bazasiga ulanish satri
- `APP_BEARER_TOKEN` - Himoyalangan endpointlar uchun token
- `APP_DEBUG` - Debug rejimi
- `APP_ALLOWED_ORIGINS` - CORS uchun ruxsat etilgan manbalar

##  Loglash

Loglar quyidagi joylarga yoziladi:
- Konsolga (dasturlashda)
- `logs/app.log` barcha loglar
- `logs/app_errors.log` faqat xatoliklar

## Xususiyatlar

### Modulli arxitektura

Har bir modul quyidagilarni o‘z ichiga oladi:
- `router.py` - API endpointlar
- `schemas.py` - Pydantic sxemalari
- `services.py` - Biznes mantiq
- `models.py` - ORM modellar
- `funcs.py` - Yordamchi funksiyalar (ixtiyoriy)



### Bazaviy modellar

Barcha ma'lumotlar bazasi modellar  `BaseModel` dan meros oladi va quyidagi ustunlarni o‘z ichiga oladi:
- `id` (UUID)
- `created_at` 
- `updated_at`
- `deleted_at`  (yumshoq o‘chirish uchun)

### Middleware

- Xatolarni avtomatik qayta ishlash
- Har bir so‘rovni loglash
- CORS siyosatini qo‘llash
- Javob sarlavhalarini avtomatik qo‘shish

## Xavfsizlik

- Himoyalangan endpointlar uchun Bearer token autentifikatsiyasi
- Kiruvchi ma'lumotlarni to‘liq validatsiyalash
- CORS orqali xavfsiz manbalarni cheklash
- Shubhali faoliyatni loglash

## Ishlash samaradorligi

- Barcha funksiyalar async/await orqali asinxron ishlaydi
- Ma'lumotlar bazasi uchun ulanishlar pooling asosida
- So‘rovlar paginatsiya orqali optimallashtirilgan
- Kesh tizimi (zaruratga qarab)

## Мониторинг

- Health check endpoint
- Keng qamrovli loglar
- МHar bir so‘rovning ishlash vaqtini o‘lchash
- Xatoliklarni kuzatish tizimi bilan integratsiya
