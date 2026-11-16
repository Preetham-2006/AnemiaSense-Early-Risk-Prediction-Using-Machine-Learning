# AnemiaSense — LightGBM Healthcare Screening App

## 1. Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Backend: http://127.0.0.1:5000
Health check: http://127.0.0.1:5000/api/health

## 2. Frontend (new terminal)
```powershell
cd frontend
npm install
npm run dev
```
Open the URL Vite prints, normally http://localhost:5173.

## 3. Important
The LightGBM model expects these exact features:
`WardNum, ERY, HK, LEUKO, HB, PLT, MCV, MCHC, MCH, RDW`.
The Analyze page therefore contains all 10 fields and the backend maps the user-friendly names to the trained feature names.
