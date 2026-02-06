try:
    from ortools.constraint_solver import pywrapcp, routing_enums_pb2
    ORTOOLS_AVAILABLE = True
except Exception:  # pragma: no cover - runtime import guard
    ORTOOLS_AVAILABLE = False

def optimize_route(distance_matrix):
    """
    Solve Vehicle Routing Problem (VRP) using Google OR-Tools
    
    Args:
        distance_matrix: 2D array of distances between locations
        
    Returns:
        List of location indices representing optimized route order
    """
    if ORTOOLS_AVAILABLE:
        # Create routing index manager
        # Parameters: number of locations, number of vehicles, depot index
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix),  # Number of locations
            1,                     # Number of vehicles (1 truck)
            0                      # Depot index (start/end point)
        )

        # Create routing model
        routing = pywrapcp.RoutingModel(manager)

        # Define distance callback
        def distance_callback(from_index, to_index):
            """Returns the distance between two nodes"""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            # Convert to integer (OR-Tools requirement) by multiplying by 1000
            return int(distance_matrix[from_node][to_node] * 1000)

        # Register distance callback
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Set cost of travel
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Set search parameters
        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        # Optional: Add time limit for optimization
        search_params.time_limit.seconds = 30

        # Solve the problem
        solution = routing.SolveWithParameters(search_params)

        if not solution:
            # If no solution found, return sequential route
            return list(range(len(distance_matrix)))

        # Extract route from solution
        route = []
        index = routing.Start(0)  # Start at depot

        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))

        # Add final node (return to depot)
        route.append(manager.IndexToNode(index))

        return route

    # Fallback: nearest-neighbor heuristic when OR-Tools is unavailable
    num_locations = len(distance_matrix)
    if num_locations == 0:
        return []
    unvisited = set(range(1, num_locations))
    route = [0]
    current = 0
    while unvisited:
        next_stop = min(unvisited, key=lambda idx: distance_matrix[current][idx])
        unvisited.remove(next_stop)
        route.append(next_stop)
        current = next_stop
    route.append(0)
    return route

def optimize_multi_vehicle_route(distance_matrix, num_vehicles=1, vehicle_capacities=None):
    """
    Advanced VRP with multiple vehicles and capacity constraints
    (For future expansion)
    
    Args:
        distance_matrix: 2D array of distances
        num_vehicles: Number of trucks available
        vehicle_capacities: List of max capacity per vehicle
        
    Returns:
        List of routes, one per vehicle
    """
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        num_vehicles,
        0  # All vehicles start from depot
    )
    
    routing = pywrapcp.RoutingModel(manager)
    
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node] * 1000)
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Add capacity constraints if provided
    if vehicle_capacities:
        # This would require demand data per location
        # Left as placeholder for expansion
        pass
    
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    
    solution = routing.SolveWithParameters(search_params)
    
    if not solution:
        return None
    
    # Extract routes for all vehicles
    routes = []
    for vehicle_id in range(num_vehicles):
        route = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)
    
    return routes