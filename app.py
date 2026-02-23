from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "eco_data.db")


#---------------------------
#secret key for sessions
#---------------------------
app.secret_key = "eco_secret_key"

@app.route("/save_score", methods=["POST"])
def save_score():
    data = request.get_json()
    session["eco_score"] = data["score"]
    return {"message": "Saved"}

@app.route("/download_report")
def download_report():
    score = session.get("eco_score", 0)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("EcoRoute Travel Readiness Report", styles["Heading1"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Your Eco Readiness Score: {score}%", styles["Normal"]))
    elements.append(Spacer(1, 10))

    if score >= 85:
        level = "Eco Champion"
    elif score >= 60:
        level = "Eco Explorer"
    elif score >= 35:
        level = "Eco Beginner"
    else:
        level = "Needs Improvement"

    elements.append(Paragraph(f"Level: {level}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="Eco_Readiness_Report.pdf",
                     mimetype="application/pdf")


# ---------------------------
# DB CONNECTION
# ---------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def trees_equivalent(co2_kg):
    return round(co2_kg / 21, 2)


# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")

#-----------------------------
#feedback
#-----------------------------

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        return render_template("feedback.html", success="Feedback submitted!")
    return render_template("feedback.html")




# ---------------------------
# ABOUT PAGE
# ---------------------------
@app.route("/about")
def about():
    return render_template("about.html")

#---------------------------
#profile page
#---------------------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("profile.html", user_name=session["user_name"])



# ---------------------------
# FAQ PAGE
# ---------------------------
@app.route("/faq")
def faq():
    return render_template("faq.html")


# ---------------------------
# DASHBOARD PAGE
# ---------------------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------------------
# ECO ROUTE PAGE
# ---------------------------
@app.route("/eco_route_page")
def eco_route_page():
    return render_template("eco_route.html")


@app.route("/eco_route", methods=["GET", "POST"])
def eco_route():

    if request.method == "POST":
        source = request.form.get("source", "").strip()
        destination = request.form.get("destination", "").strip()
        fuel_type = request.form.get("fuel_type", "").strip()

        if not source or not destination or not fuel_type:
            return render_template("result.html", error="Please fill all fields.")

        conn = get_db_connection()

        popular = conn.execute("""
            SELECT * FROM routes
            WHERE lower(source)=lower(?)
            AND lower(destination)=lower(?)
            AND lower(route_type)='popular'
            LIMIT 1
        """, (source, destination)).fetchone()

        eco = conn.execute("""
            SELECT * FROM routes
            WHERE lower(source)=lower(?)
            AND lower(destination)=lower(?)
            AND lower(route_type)='eco'
            LIMIT 1
        """, (source, destination)).fetchone()

        conn.close()

        if not popular or not eco:
            return render_template("result.html", error="Route not found in database.")

        pop_fuel = round(popular["distance_km"] / popular["fuel_efficiency_kmpl"], 2)
        eco_fuel = round(eco["distance_km"] / eco["fuel_efficiency_kmpl"], 2)

        co2_per_litre = {
            "Petrol": 2.31,
            "Diesel": 2.68,
            "Electric": 0.50
        }

        rate = co2_per_litre.get(fuel_type, 2.31)

        pop_co2 = round(pop_fuel * rate, 2)
        eco_co2 = round(eco_fuel * rate, 2)

        result = {
            "source": source,
            "destination": destination,
            "popular_distance": popular["distance_km"],
            "eco_distance": eco["distance_km"],
            "fuel_saved": round(pop_fuel - eco_fuel, 2),
            "co2_saved": round(pop_co2 - eco_co2, 2),
            "traffic_popular": popular["traffic_level"],
            "traffic_eco": eco["traffic_level"]
        }

        return render_template("result.html", result=result)

    return render_template("eco_route.html")

# ---------------------------
# CARBON PAGE
# ---------------------------
@app.route("/carbon_page")
def carbon_page():
    return render_template("carbon.html")

# ---------------------------
# ECO CHECKLIST PAGE
# ---------------------------
@app.route("/checklist")
def checklist():
    return render_template("checklist.html")

# ---------------------------
# QUIZ PAGE
# ---------------------------
@app.route("/quiz")
def quiz():
    return render_template("quiz.html")



# ---------------------------
# CARBON CALCULATOR
# ---------------------------
@app.route("/carbon", methods=["GET","POST"])
def carbon():
    distance = float(request.form.get("distance", 0))
    vehicle_type = request.form.get("vehicle_type", "").strip()
    passengers = int(request.form.get("passengers", 1))

    if passengers <= 0:
        passengers = 1

    conn = get_db_connection()

    row = conn.execute("""
        SELECT co2_per_km, pm2_5, nox, avg_cost_per_km
        FROM transport_emissions
        WHERE lower(vehicle_type)=lower(?)
        LIMIT 1
    """, (vehicle_type,)).fetchone()

    conn.close()

    if not row:
        return render_template("result.html", error="Vehicle type not found.")

    total_co2 = round(distance * row["co2_per_km"], 2)
    per_person = round(total_co2 / passengers, 2)
    trees_eq = trees_equivalent(total_co2)

    return render_template(
        "result.html",
        carbon_result={
            "distance": distance,
            "vehicle_type": vehicle_type,
            "passengers": passengers,
            "total_co2": total_co2,
            "per_person": per_person,
            "trees_eq": trees_eq
        }
    )


# ---------------------------
# CHART PAGE
# ---------------------------
@app.route("/chart", methods=["GET", "POST"])
def chart():
    vehicle = "Car"

    if request.method == "POST":
        vehicle = request.form.get("vehicle", "Car")

    conn = get_db_connection()
    row = conn.execute("""
        SELECT co2_per_km, pm2_5, nox, avg_cost_per_km
        FROM transport_emissions
        WHERE lower(vehicle_type)=lower(?)
        LIMIT 1
    """, (vehicle,)).fetchone()
    conn.close()

    chart_data = [0, 0, 0, 0]
    if row:
        chart_data = [row["co2_per_km"], row["pm2_5"], row["nox"], row["avg_cost_per_km"]]

    return render_template("chart.html", chart_data=chart_data, vehicle=vehicle)


# ---------------------------
# TRANSPORT FINDER PAGE
# ---------------------------
@app.route("/transport_finder")
def transport_finder():
    return render_template("transport_finder.html")


@app.route("/get_city_transport", methods=["POST"])
def get_city_transport():
    city = request.form.get("city", "").strip()

    conn = get_db_connection()
    row = conn.execute("""
        SELECT * FROM city_transport
        WHERE lower(city)=lower(?)
        LIMIT 1
    """, (city,)).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "City not found"})

    return jsonify(dict(row))


# ---------------------------
# DESTINATION SCORE PAGE
# ---------------------------
@app.route("/destination_page")
def destination_page():
    return render_template("destination_score.html")


@app.route("/get_destination_score", methods=["POST"])
def get_destination_score():
    destination = request.form.get("destination", "").strip()

    conn = get_db_connection()
    row = conn.execute("""
        SELECT * FROM destinations
        WHERE lower(destination)=lower(?)
        LIMIT 1
    """, (destination,)).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Destination not found"})

    return jsonify(dict(row))


# ---------------------------
# ALERTS PAGE
# ---------------------------
@app.route("/alerts_page")
def alerts_page():
    return render_template("alerts.html")


@app.route("/get_alerts", methods=["POST"])
def get_alerts():
    destination = request.form.get("destination", "").strip()

    conn = get_db_connection()

    overt = conn.execute("""
        SELECT * FROM overtourism
        WHERE lower(destination)=lower(?)
        LIMIT 1
    """, (destination,)).fetchone()

    water = conn.execute("""
        SELECT * FROM water_scarcity
        WHERE lower(destination)=lower(?)
        LIMIT 1
    """, (destination,)).fetchone()

    conn.close()

    return jsonify({
        "overtourism": dict(overt) if overt else None,
        "water": dict(water) if water else None
    })


# ---------------------------
# AUTOCOMPLETE SEARCH API
# ---------------------------
@app.route("/search_city")
def search_city():
    q = request.args.get("q", "").lower()

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT DISTINCT source AS city FROM routes
        UNION
        SELECT DISTINCT destination AS city FROM routes
    """).fetchall()
    conn.close()

    all_cities = [r["city"] for r in rows if r["city"]]
    suggestions = [c for c in all_cities if c.lower().startswith(q)]

    return jsonify(suggestions[:10])


# ---------------------------
# SIGNUP PAGE
# ---------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)

        try:
            conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                         (name, email, hashed_password))
            conn.commit()
        except:
            conn.close()
            return render_template("signup.html", error="Email already exists!")

        conn.close()
        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------------------
# LOGIN PAGE
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid email or password!")

    return render_template("login.html")

#---------------------------
# ECO GUIDE PAGE
#---------------------------

@app.route("/eco-guide")
def eco_guide():
    return render_template("eco_guide.html")

# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
