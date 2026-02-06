# File Structure

```
FleetPath/
├── Backend/
│   ├── main.py               # FastAPI entrypoint
│   ├── services/
│   │   ├── distance.py       # Distance matrix helpers
│   │   └── optimizer.py      # OR-Tools route solver
│   ├── data/
│   │   └── pickups.csv       # Sample locations
│   └── requirements.txt
├── Frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js            # Main UI and map
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── Documentation/
	├── README.md             # Full project documentation
	├── Quickstart.md         # Short setup guide
	├── DEMO_GUIDE.md         # Demo script
	├── FILE_STRUCTURE.md     # This file
	└── FOLDER_SETUP.md       # Folder prep and run tips
```
