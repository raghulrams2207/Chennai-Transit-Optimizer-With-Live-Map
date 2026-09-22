from flask import Flask, render_template, request
from database import get_connection
from graph import build_graph
from dijkstra import dijkstra
import requests
import time

app = Flask(__name__)


# =========================================================
# GEOCODE CHENNAI STATION
# =========================================================

def get_coordinates(place_name):

    try:
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": f"{place_name}, Chennai, Tamil Nadu, India",
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "ChennaiTransitOptimizer/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5
        )

        data = response.json()

        if data:
            return [
                float(data[0]["lat"]),
                float(data[0]["lon"])
            ]

    except Exception as e:
        print("Map geocoding error:", e)

    return None


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    connection = get_connection()

    if not connection:
        return "Database connection failed."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            station_id,
            name,
            mode
        FROM stations
        WHERE status = TRUE
        ORDER BY name
    """)

    stations = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        stations=stations
    )


# =========================================================
# FIND ROUTE
# =========================================================

@app.route("/find-route", methods=["POST"])
def find_route():

    source = int(request.form["source"])
    destination = int(request.form["destination"])

    mode = request.form.get(
        "mode",
        "fastest"
    )

    # -----------------------------------------------------
    # SAME STATION
    # -----------------------------------------------------

    if source == destination:

        return """
        <h2>⚠️ Invalid Journey</h2>

        <p>
        Starting and destination stations cannot be the same.
        </p>

        <a href="/">
        ← Go Back
        </a>
        """

    # -----------------------------------------------------
    # BUILD GRAPH
    # -----------------------------------------------------

    graph = build_graph()

    # -----------------------------------------------------
    # DIJKSTRA
    # -----------------------------------------------------

    result = dijkstra(
        graph,
        source,
        destination,
        mode
    )

    # -----------------------------------------------------
    # NO ROUTE
    # -----------------------------------------------------

    if not result:

        return render_template(
            "result.html",
            result=None,
            mode=mode,
            source=source,
            destination=destination,
            map_points=[]
        )

    # -----------------------------------------------------
    # GET STATION DATA
    # -----------------------------------------------------

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            station_id,
            name,
            mode
        FROM stations
    """)

    stations = cursor.fetchall()

    cursor.close()
    connection.close()

    # -----------------------------------------------------
    # STATION NAME DICTIONARY
    # -----------------------------------------------------

    station_names = {
        station["station_id"]:
        station["name"]
        for station in stations
    }

    station_modes = {
        station["station_id"]:
        station["mode"]
        for station in stations
    }

    # -----------------------------------------------------
    # ADD STATION NAMES
    # -----------------------------------------------------

    for item in result["path"]:

        station_id = item["station"]

        item["station_name"] = station_names.get(
            station_id,
            f"Station {station_id}"
        )

        item["mode"] = station_modes.get(
            station_id,
            "Transit"
        )

    # -----------------------------------------------------
    # CREATE MAP POINTS
    # -----------------------------------------------------

    map_points = []

    print("\n================ MAP ROUTE ================")

    for item in result["path"]:

        station_name = item["station_name"]

        print(
            "Finding coordinates for:",
            station_name
        )

        coordinates = get_coordinates(
            station_name
        )

        if coordinates:

            map_points.append({

                "name": station_name,

                "lat": coordinates[0],

                "lng": coordinates[1]

            })

            print(
                "Found:",
                coordinates
            )

        else:

            print(
                "Could not find:",
                station_name
            )

        # Small delay for geocoding service
        time.sleep(0.2)

    print(
        "Total map points:",
        len(map_points)
    )

    print(
        "==========================================\n"
    )

    # -----------------------------------------------------
    # RESULT PAGE
    # -----------------------------------------------------

    return render_template(

        "result.html",

        result=result,

        mode=mode,

        source=source,

        destination=destination,

        map_points=map_points

    )


# =========================================================
# BOOK JOURNEY
# =========================================================

@app.route("/book", methods=["POST"])
def book_journey():

    user_name = request.form[
        "user_name"
    ].strip()

    source = int(
        request.form["source"]
    )

    destination = int(
        request.form["destination"]
    )

    travel_time = int(
        float(
            request.form[
                "travel_time"
            ]
        )
    )

    final_cost = float(
        request.form[
            "final_cost"
        ]
    )

    if not user_name:

        return """
        <h2>❌ Booking Failed</h2>

        <p>
        Please enter passenger name.
        </p>

        <a href="/">
        ← Go Back
        </a>
        """

    connection = get_connection()

    if not connection:

        return "Database connection failed."

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""

            INSERT INTO bookings
            (
                user_name,
                source_id,
                destination_id,
                travel_time,
                final_cost
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """, (

            user_name,

            source,

            destination,

            travel_time,

            final_cost

        ))

        connection.commit()

        booking_id = cursor.lastrowid

        cursor.execute("""

            SELECT
                station_id,
                name

            FROM stations

            WHERE station_id IN (%s, %s)

        """, (

            source,
            destination

        ))

        station_rows = cursor.fetchall()

        names = {

            row["station_id"]:
            row["name"]

            for row in station_rows

        }

        source_name = names.get(
            source,
            f"Station {source}"
        )

        destination_name = names.get(
            destination,
            f"Station {destination}"
        )

        return render_template(

            "booking_success.html",

            booking_id=booking_id,

            user_name=user_name,

            source_name=source_name,

            destination_name=destination_name,

            travel_time=travel_time,

            final_cost=final_cost

        )

    except Exception as e:

        connection.rollback()

        return f"""

        <h2>❌ Booking Failed</h2>

        <p>{e}</p>

        <a href="/">
        ← Go Back
        </a>

        """

    finally:

        cursor.close()
        connection.close()


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )