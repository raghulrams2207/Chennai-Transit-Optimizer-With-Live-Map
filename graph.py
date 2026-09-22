from database import get_connection


def build_graph():

    graph = {}

    connection = get_connection()

    if not connection:
        return graph

    cursor = connection.cursor(dictionary=True)

    # =====================================================
    # GET ALL STATIONS
    # =====================================================

    cursor.execute("""
        SELECT
            station_id,
            name,
            mode
        FROM stations
        WHERE status = TRUE
    """)

    stations = cursor.fetchall()

    # Create empty adjacency list
    for station in stations:

        graph[station["station_id"]] = []

    # =====================================================
    # GET ALL CONNECTIONS
    # =====================================================

    cursor.execute("""
        SELECT
            c.source_id,
            c.destination_id,
            c.route_id,
            c.travel_time,
            c.distance,
            r.mode,
            r.route_name
        FROM connections c

        JOIN routes r
            ON c.route_id = r.route_id

        WHERE c.status = TRUE
    """)

    connections = cursor.fetchall()

    # =====================================================
    # BUILD ADJACENCY LIST
    # =====================================================

    for connection_data in connections:

        source = connection_data["source_id"]

        destination = connection_data["destination_id"]

        travel_time = float(
            connection_data["travel_time"]
        )

        distance = float(
            connection_data["distance"]
            or 0
        )

        mode = connection_data["mode"]

        route_name = connection_data["route_name"]

        # -------------------------------------------------
        # SIMPLE FARE CALCULATION
        # -------------------------------------------------
        #
        # This is a representative fare model for the
        # semester project.
        #
        # Metro / Rail / Bus have different base fares.
        #

        if mode == "Metro":

            base_fare = 10

        elif mode == "Rail":

            base_fare = 10

        elif mode == "Bus":

            base_fare = 8

        else:

            base_fare = 10

        # Additional distance-based component

        distance_fare = distance * 0.50

        cost = base_fare + distance_fare

        # -------------------------------------------------
        # ADD EDGE
        # -------------------------------------------------

        graph[source].append({

            "station": destination,

            "route": route_name,

            "route_id": connection_data["route_id"],

            "mode": mode,

            "travel_time": travel_time,

            "distance": distance,

            "cost": round(
                cost,
                2
            )

        })

    cursor.close()

    connection.close()

    return graph