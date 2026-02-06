# Demo Guide

## Goal
Show that the app can load pickup locations, optimize a route, and report savings.

## Setup
1. Start backend: `uvicorn main:app --reload` from `Backend/`
2. Start frontend: `npm start` from `Frontend/`
3. Open the app at http://localhost:3000

## Demo Flow (5-7 minutes)
1. Point out the map and list of pickup locations.
2. Click "Optimize Route" to trigger the API call.
3. Show the optimized path on the map.
4. Highlight metrics: total stops, original miles, optimized miles, savings.
5. Click "Reset" to return to the original view.

## Talking Points
- Route optimization reduces distance and fuel usage.
- The backend computes the distance matrix and optimized order.
- The frontend visualizes the path and metrics for quick decisions.

## Common Questions
- Q: Where does the data come from?
	A: `Backend/data/pickups.csv`.
- Q: Can we add more stops?
	A: Yes, add rows to the CSV and refresh.
- Q: What algorithm is used?
	A: Google OR-Tools solves a Traveling Salesman style problem.
