Bridging the Yield Gap: Satellite and Weather-Driven Crop Monitoring for
Climate-Vulnerable Smallholder Farmers in Rwanda

**BSc in Software Engineering**\
**Student:** Ganza Owen Yhaan\
**Supervisor:** Tunde Isiaq Gbadamosi\
**Institution:** African Leadership University (ALU)\
**Date:** 25th January 2026

## Project Description

This capstone project develops a low-cost, accessible precision
agriculture system for smallholder farmers in Rwanda. It uses free
satellite NDVI data (from Google Earth Engine - MODIS), historical and
forecast weather data (from Open-Meteo), and a trained Random Forest
machine learning model to predict maize crop yield. The system provides
actionable insights and color-coded alerts via a web interface
(Streamlit) and API (FastAPI with Swagger UI).

**Core Features:** - Real-time yield prediction based on location,
planting date, and crop type - District-specific predictions using
Rwanda-wide data - User-friendly web dashboard with login, prediction
form, and history - API endpoint for integration (tested with
Swagger/Postman) - Simulated database (session state) for storing
prediction history

The MVP focuses on maize in pilot areas (e.g., Gasabo district) and aims
for ≥70% prediction accuracy and farmer usability.

## GitHub Repository Link

https://github.com/gyhaan/capstone-backend

## How to Set Up the Environment and Project

### Prerequisites

-   Python 3.10+
-   Git
-   Virtual environment (venv)

### Step 1: Clone the Repository

``` bash
git clone https://github.com/gyhaan/capstone-backend.git
cd capstone-backend
```

------------------------------------------------------------------------

### Step 2: Set Up Virtual Environment

``` bash
# Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

------------------------------------------------------------------------

### Step 3: Install Dependencies

``` bash
pip install -r requirements.txt
```

(If separate backend/frontend requirements, install both.)

------------------------------------------------------------------------

### Step 4: Run the Backend (FastAPI)

``` bash
cd backend
uvicorn main:app --reload
```

API available at:\
http://127.0.0.1:8000

Swagger UI (interactive testing):\
http://127.0.0.1:8000/docs

------------------------------------------------------------------------

### Step 5: Run the Frontend (Streamlit)

Open a second terminal and navigate to the frontend folder:

``` bash
cd ../frontend
streamlit run streamlit_app.py
```

Web app opens at:\
http://localhost:8501

Login credentials:\
- **Username:** farmer\
- **Password:** password123

------------------------------------------------------------------------

### Step 6: Test the MVP

-   Start backend → test `/predict` in Swagger\
-   Start Streamlit → login → select district/crop/date → predict → view
    in **History**

------------------------------------------------------------------------

## Designs & Screenshots

### Figma Mockups

Full design file (login, dashboard, prediction form, history):\
https://www.figma.com/design/tNPIMk36QzCHUGe15BzOK3/Capstone?node-id=0-1&t=13xY3oH5sZ8qCyfy-1

### Screenshots (add after testing)

-   Login screen\
-   Prediction form with district dropdown\
-   Successful prediction result\
-   History page with saved predictions\
-   Swagger UI showing `/predict` endpoint

(Add actual screenshots here in README after running the app)

------------------------------------------------------------------------

## Deployment Plan

### Local Development

-   **Backend:** `uvicorn main:app --reload`\
-   **Frontend:** `streamlit run streamlit_app.py`

------------------------------------------------------------------------

### Production Deployment (Free Options)

#### Backend (FastAPI)

**Platform:** Render.com (free tier)

**Steps:** 1. Create account → New → Web Service → connect GitHub repo\
2. Runtime: Python\
3. Build command: `bash    pip install -r requirements.txt` 4. Start
command: `bash    uvicorn main:app --host 0.0.0.0 --port $PORT`

After deploy:\
Get URL (e.g., `https://your-backend.onrender.com`)

------------------------------------------------------------------------

#### Frontend (Streamlit)

**Platform:** Streamlit Community Cloud (free)

**Steps:** 1. Go to https://share.streamlit.io\
2. Connect GitHub → select `frontend/streamlit_app.py`\
3. Deploy → gets public URL

Update `API_URL` in `streamlit_app.py` to your deployed backend URL.

------------------------------------------------------------------------

### Full Flow

1.  Deploy backend → get URL\
2.  Update Streamlit code with new API URL\
3.  Deploy Streamlit → share public link

