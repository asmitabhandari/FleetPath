from geopy.distance import geodesic


def create_distance_matrix(locations):
    """
    Create a distance matrix from a list of locations

    Args:
        locations: List of dicts with 'lat' and 'lon' keys

    Returns:
        2D matrix where matrix[i][j] is distance in miles from location i to j
    """
    matrix = []

    for from_loc in locations:
        row = []
        for to_loc in locations:
            # Calculate geodesic distance in miles
            dist = geodesic(
                (from_loc["lat"], from_loc["lon"]),
                (to_loc["lat"], to_loc["lon"])
            ).miles
            row.append(dist)
        matrix.append(row)

    return matrix


def get_distance_between_points(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographic points

    Returns:
        Distance in miles
    """
    return geodesic((lat1, lon1), (lat2, lon2)).miles
from geopy.distance import geodesic

def create_distance_matrix(locations):
    """
    Create a distance matrix from a list of locations
    
    Args:
        locations: List of dicts with 'lat' and 'lon' keys
        
    Returns:
        2D matrix where matrix[i][j] is distance in miles from location i to j
    """
    matrix = []
    
    for from_loc in locations:
        row = []
        for to_loc in locations:
            # Calculate geodesic distance in miles
            dist = geodesic(
                (from_loc["lat"], from_loc["lon"]),
                (to_loc["lat"], to_loc["lon"])
            ).miles
            row.append(dist)
        matrix.append(row)
    
    return matrix

def get_distance_between_points(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographic points
    
    Returns:
        Distance in miles
    """
    return geodesic((lat1, lon1), (lat2, lon2)).miles