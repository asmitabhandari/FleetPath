# QUICK START GUIDE

## Installation (5 minutes)

### Step 1: Install Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Install Frontend
```bash
cd frontend
npm install
```

## Running the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```
Backend running at http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```
Frontend opens automatically at http://localhost:3000

## Using the App

1. View Locations - See all pickup points on the map
2. Click "Optimize Route" - Watch the route optimize
3. Review Metrics - See distance saved and fuel savings
4. Click "Reset" - Return to original view

## Adding Custom Locations

Edit backend/data/pickups.csv:
```csv
id,address,lat,lon
1,My Depot,42.4973,-83.3677
2,Customer A,42.4981,-83.3621
```

Get coordinates from Google Maps:
1. Right-click location -> "What's here?"
2. Copy latitude and longitude

## Troubleshooting

Map doesn't load?
- Check Mapbox token is set in App.js

Can't connect to backend?
- Make sure backend is running on port 8000
- Check http://localhost:8000/docs

Modules not found?
- Backend: pip install -r requirements.txt
- Frontend: npm install

## API Endpoints

- GET / - API status
- GET /locations - All pickup locations
- GET /optimize - Optimized route with metrics

## Tech Stack

- Frontend: React + Mapbox GL
- Backend: FastAPI (Python)
- Optimization: Google OR-Tools
- Maps: Mapbox

---

That's it! You're ready to optimize routes.

For detailed instructions, see Documentation/README.md
For demo presentation tips, see Documentation/DEMO_GUIDE.md
