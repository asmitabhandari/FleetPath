from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from services.distance import create_distance_matrix
from services.optimizer import optimize_route

app = FastAPI(title="Waste Route Optimizer API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Waste Route Optimizer API is running"}

@app.get("/optimize")
def optimize():
    """
    Optimize waste collection route based on pickup locations
    Returns optimized route with metrics
    """
    # Load pickup data
    df = pd.read_csv("data/pickups.csv")
    locations = df.to_dict(orient="records")
    
    # Create distance matrix
    matrix = create_distance_matrix(locations)
    
    # Get optimized route
    route_indices = optimize_route(matrix)
    
    # Calculate distances
    original_distance = calculate_sequential_distance(matrix)
    optimized_distance = calculate_route_distance(route_indices, matrix)
    savings = original_distance - optimized_distance
    
    # Order stops according to optimized route
    ordered_stops = [locations[i] for i in route_indices]
    
    return {
        "route": ordered_stops,
        "metrics": {
            "original_miles": round(original_distance, 2),
            "optimized_miles": round(optimized_distance, 2),
            "savings_miles": round(savings, 2),
            "savings_percentage": round((savings / original_distance * 100), 1),
            "estimated_fuel_savings_gallons": round(savings / 6, 2),  # Assuming 6 MPG for truck
            "total_stops": len(locations)
        }
    }

@app.get("/locations")
def get_locations():
    """Get all pickup locations"""
    df = pd.read_csv("data/pickups.csv")
    return df.to_dict(orient="records")

def calculate_sequential_distance(matrix):
    """Calculate distance for sequential (non-optimized) route"""
    total = 0
    for i in range(len(matrix) - 1):
        total += matrix[i][i + 1]
    # Return to start
    total += matrix[len(matrix) - 1][0]
    return total

def calculate_route_distance(route, matrix):
    """Calculate total distance for a given route"""
    total = 0
    for i in range(len(route) - 1):
        total += matrix[route[i]][route[i + 1]]
    return total    