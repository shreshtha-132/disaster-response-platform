# 📘 Disaster Response Platform (FastAPI Backend)

## 🎯 Objective

Build a backend-heavy FastAPI project to manage disaster data, extract locations using AI (Gemini), get coordinates, store in Supabase with geospatial features, cache responses, and support real-time communication.

---

## ✅ Step-by-Step Plan

### 🧱 Step 1: Project Setup

```bash
mkdir disaster-platform && cd disaster-platform
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn python-dotenv "httpx[http2]>=0.24,<0.28" "websockets>=11,<13" beautifulsoup4 supabase geojson
```

### 🗂️ Step 2: Create Project Structure

```
disaster-platform/
├── main.py
├── api/
│   ├── __init__.py
│   ├── disaster.py
│   ├── geocode.py
│   ├── social_media.py
│   ├── verify_image.py
│   └── updates.py
├── db/
│   ├── __init__.py
│   └── database.py
├── models/
│   ├── __init__.py
│   └── schemas.py
├── services/
│   ├── __init__.py
│   ├── cache.py
│   ├── gemini.py
│   ├── geocoding.py
│   └── scraper.py
├── static/
│   └── index.html (optional minimal frontend)
```

---

## 🔧 Step 3: Supabase Setup

* Create project at [https://supabase.com](https://supabase.com)
* Set up tables: `disasters`, `resources`, `reports`, `cache`
* Enable PostGIS (geospatial extension)
* Add geospatial indexes:

```sql
CREATE INDEX disasters_location_idx ON disasters USING GIST (location);
```

---

## 🧠 Step 4: Build APIs (in `api/` folder)

### 1. Disaster CRUD (`disaster.py`)

* POST `/disasters` → calls Gemini to extract location + maps API for lat/lng
* GET `/disasters?tag=flood`
* PUT/DELETE `/disasters/:id`

### 2. Geocoding (`geocode.py`)

* POST `/geocode` → extract + convert location

### 3. Social Media (`social_media.py`)

* GET `/disasters/:id/social-media` → mock social data + caching

### 4. Image Verification (`verify_image.py`)

* POST `/disasters/:id/verify-image` → Gemini image verification API

### 5. Official Updates (`updates.py`)

* GET `/disasters/:id/official-updates` → scrape Red Cross/FEMA with BeautifulSoup

---

## 🛠️ Step 5: Services Logic (`services/` folder)

### gemini.py

* `extract_location_with_gemini(text)`
* `verify_image_with_gemini(image_url)`

### geocoding.py

* `get_coordinates(location_name)` → uses Mapbox/Google Maps API

### cache.py

* `get_cached_data(key)`
* `set_cache_data(key, value)` with TTL check

### scraper.py

* `fetch_official_updates(url)`

---

## 🧾 Step 6: Models (`models/schemas.py`)

Use Pydantic to define:

* DisasterSchema, ReportSchema, ResourceSchema
* CacheSchema, VerificationSchema

---

## 🔌 Step 7: DB Connection (`db/database.py`)

Use Supabase Python SDK to:

* Connect to DB
* Run `insert`, `select`, and `update` functions

---

## 🌐 Step 8: Main App (`main.py`)

* Include all routers from `api/`
* Load `.env` and connect DB
* Setup WebSocket events:

  * `disaster_updated`, `resources_updated`, `social_media_updated`

---

## 🔄 Step 9: Real-Time WebSocket

Use `websockets` or `fastapi-socketio`

* Emit on disaster/resource changes
* Broadcast to connected clients

---

## 🔐 Step 10: Mock Authentication

* Hardcode users:

```python
users = {
  "netrunnerX": {"role": "admin"},
  "reliefAdmin": {"role": "contributor"}
}
```

* Use request header `X-User: netrunnerX`

---

## 🧪 Step 11: Testing

* Use Postman or `static/index.html`
* Test all endpoints manually

---

## 🚀 Step 12: Deployment

* Backend → Render (use Gunicorn/Uvicorn)
* Frontend (if made) → Vercel

---

## 📝 Summary

| Feature                      | Status     |
| ---------------------------- | ---------- |
| Disaster CRUD                | ✅          |
| Location Extraction (Gemini) | ✅          |
| Geocoding                    | ✅          |
| Caching Layer                | ✅          |
| Social Media Monitoring      | ✅ (mocked) |
| Image Verification           | ✅          |
| Browse Page Scraping         | ✅          |
| Real-time Updates            | ✅          |
| Auth + Roles                 | ✅          |
| Minimal Frontend             | Optional   |

---

## 🔑 ENV Example

```
SUPABASE_URL=your_url
SUPABASE_KEY=your_anon_key
GEMINI_API_KEY=your_key
MAPBOX_API_KEY=your_key
```

---

# 📘 Disaster Response Platform (FastAPI Backend)

## 🎯 Project Overview

A backend-heavy platform that helps manage and respond to disasters. The system leverages:
- 🌍 AI (Gemini) for extracting location data from text/image
- 📍 Geocoding (OpenStreetMap)
- 🗂️ Supabase for structured and geospatial storage
- ⚡ Caching layer for efficiency
- 📡 WebSockets for real-time updates
- 🧪 Testing, 🐳 Docker, and 🚀 CI/CD for production-readiness

---

## ✅ What's Done (as of now)

### Core Features
- [x] `disaster.py`: Full CRUD for disasters with Gemini location extraction
- [x] `resource.py`: Add and fetch resources linked to disasters
- [x] `geocode.py`: Geocoding using OpenStreetMap
- [x] `gemini.py`: Location and image verification with caching
- [x] `cache.py`: Redis-compatible cache layer using Supabase
- [x] Supabase DB connected and functional
- [x] Project structure finalized
- [x] Project runs with Uvicorn
- [x] Initial local testing working

---

### 📦 1. Push to GitHub (Version Control)
- [ ] Initialize Git repo (if not done)
- [ ] Push working code to GitHub
- [ ] Add `.gitignore`, `README.md`, and `requirements.txt`

### 🧪 2. Testing
- [ ] Add unit tests using `pytest` for:
  - [ ] `disaster.py`
  - [ ] `resource.py`
  - [ ] `services/geocode.py`, `gemini.py`
- [ ] Use `pytest-asyncio` for async endpoints
- [ ] Mock external API calls (Gemini, HTTPX)

### 🔁 3. CI/CD (via GitHub Actions)
- [ ] Create `.github/workflows/test.yml`
  - Run lint (`flake8`)
  - Run tests (`pytest`)
- [ ] Auto-deploy to Render from GitHub

### 🌐 5. Deployment
- [ ] Deploy Backend on **Render**
  - Add Supabase + Gemini keys
  - Add Render build & start commands

## 🧭 What’s Pending (Work Plan)



---

### 🐳 4. Dockerization
- [ ] Create `Dockerfile`
- [ ] Add `.dockerignore`
- [ ] Test locally (`docker build`, `docker run`)
- [ ] Optional: Add `docker-compose.yml` for multi-container setup

---

### 🌐 5. Deployment
- [ ] Deploy Frontend (if created) on **Vercel**
- [ ] Test deployed APIs via Postman

---

### 📡 6. WebSocket Integration (Real-Time)
- [ ] Add a WebSocket route to broadcast updates
  - e.g., `ws://.../ws/disaster-updates`
- [ ] Emit updates on disaster/resource insert/update
- [ ] Add frontend listener for live updates (optional)

---

### 🔐 7. Basic Auth (Optional)
- [ ] Use header-based mock authentication
- [ ] Role-based access control for certain routes

---

### 🌈 8. Frontend (Optional but Recommended)
- [ ] Minimal UI using React/Vite or HTML
- [ ] Show disaster locations, social feeds, and image status
- [ ] Connect via REST + WebSocket to backend

---

## 🗂️ Folder Structure



