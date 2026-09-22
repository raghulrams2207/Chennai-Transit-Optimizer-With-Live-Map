import heapq


def dijkstra(graph, start, destination, mode="fastest"):
    """
    Dijkstra's Shortest Path Algorithm

    Parameters:
        graph       : adjacency-list graph
        start       : starting station ID
        destination : destination station ID
        mode        : "fastest" or "cheapest"

    Returns:
        {
            "path": [...],
            "total_time": ...,
            "total_cost": ...
        }

    The complete path is returned here.
    The UI can later reduce the number of stations displayed.
    """

    # ---------------------------------------------------------
    # CHECK STATIONS
    # ---------------------------------------------------------

    if start not in graph:
        return None

    if destination not in graph:
        return None

    # ---------------------------------------------------------
    # PRIORITY QUEUE
    # ---------------------------------------------------------

    priority_queue = []

    # (current_distance, station_id)
    heapq.heappush(
        priority_queue,
        (0, start)
    )

    # ---------------------------------------------------------
    # SHORTEST DISTANCE
    # ---------------------------------------------------------

    distances = {

        station: float("inf")

        for station in graph

    }

    distances[start] = 0

    # ---------------------------------------------------------
    # PREVIOUS STATION
    # ---------------------------------------------------------

    previous = {}

    # ---------------------------------------------------------
    # STORE EDGE INFORMATION
    # ---------------------------------------------------------

    previous_edge = {}

    # ---------------------------------------------------------
    # DIJKSTRA
    # ---------------------------------------------------------

    while priority_queue:

        current_distance, current_station = heapq.heappop(
            priority_queue
        )

        # Ignore outdated queue entries
        if current_distance > distances[current_station]:
            continue

        # Destination reached
        if current_station == destination:
            break

        # -----------------------------------------------------
        # CHECK ALL NEIGHBOURS
        # -----------------------------------------------------

        for edge in graph[current_station]:

            # -------------------------------------------------
            # SUPPORT DICTIONARY EDGE
            # -------------------------------------------------

            next_station = edge["station"]

            travel_time = float(
                edge.get("travel_time", 0)
            )

            travel_cost = float(
                edge.get("cost", 0)
            )

            # -------------------------------------------------
            # DETERMINE WEIGHT
            # -------------------------------------------------

            if mode == "cheapest":

                weight = travel_cost

            else:

                # Default = fastest route
                weight = travel_time

            # -------------------------------------------------
            # NEW DISTANCE
            # -------------------------------------------------

            new_distance = (
                current_distance + weight
            )

            # -------------------------------------------------
            # BETTER ROUTE FOUND
            # -------------------------------------------------

            if new_distance < distances[next_station]:

                distances[next_station] = new_distance

                previous[next_station] = current_station

                previous_edge[next_station] = edge

                heapq.heappush(
                    priority_queue,
                    (
                        new_distance,
                        next_station
                    )
                )

    # ---------------------------------------------------------
    # NO ROUTE
    # ---------------------------------------------------------

    if destination not in previous and start != destination:

        return None

    # ---------------------------------------------------------
    # RECONSTRUCT PATH
    # ---------------------------------------------------------

    station_path = []

    current = destination

    while current != start:

        station_path.append(current)

        if current not in previous:
            return None

        current = previous[current]

    station_path.append(start)

    # Reverse path
    station_path.reverse()

    # ---------------------------------------------------------
    # CREATE DETAILED PATH
    # ---------------------------------------------------------

    detailed_path = []

    # ---------------------------------------------------------
    # START STATION
    # ---------------------------------------------------------

    detailed_path.append({

        "station": start,

        "route": None,

        "mode": None,

        "travel_time": 0,

        "cost": 0

    })

    # ---------------------------------------------------------
    # ADD EACH CONNECTION
    # ---------------------------------------------------------

    total_time = 0

    total_cost = 0

    for station in station_path[1:]:

        edge = previous_edge[station]

        travel_time = float(
            edge.get("travel_time", 0)
        )

        travel_cost = float(
            edge.get("cost", 0)
        )

        total_time += travel_time

        total_cost += travel_cost

        detailed_path.append({

            "station": station,

            "route": edge.get(
                "route",
                None
            ),

            "mode": edge.get(
                "mode",
                None
            ),

            "travel_time": travel_time,

            "cost": travel_cost

        })

    # ---------------------------------------------------------
    # RETURN RESULT
    # ---------------------------------------------------------

    return {

        "path": detailed_path,

        "total_time": round(
            total_time,
            2
        ),

        "total_cost": round(
            total_cost,
            2
        )

    }