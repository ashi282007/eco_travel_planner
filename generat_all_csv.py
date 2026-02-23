import pandas as pd
import random

# -----------------------------
# Destinations list
# -----------------------------
destinations = [
    "Goa", "Manali", "Jaipur", "Udaipur", "Shimla", "Delhi", "Mumbai", "Chennai",
    "Bangalore", "Hyderabad", "Pune", "Agra", "Varanasi", "Amritsar", "Rishikesh",
    "Dehradun", "Nainital", "Mussoorie", "Jaisalmer", "Jodhpur", "Bhopal", "Indore",
    "Kolkata", "Darjeeling", "Gangtok", "Shillong", "Guwahati", "Kochi",
    "Mysore", "Coimbatore", "Madurai", "Tirupati", "Ooty", "Kanyakumari",
    "Leh", "Ladakh", "Srinagar", "Jammu", "Katra", "Lucknow", "Patna", "Ranchi",
    "Raipur", "Bhubaneswar", "Cuttack", "Surat", "Vadodara", "Ahmedabad",
    "Nashik", "Aurangabad", "Nagpur", "Kanpur", "Allahabad", "Meerut",
    "Noida", "Gurgaon", "Faridabad", "Ghaziabad", "Haridwar", "Kullu",
    "Kasauli", "Dalhousie", "Mount Abu", "Hampi", "Pondicherry"
]

# -----------------------------
# Helpers
# -----------------------------
def clamp(value, min_val=0, max_val=100):
    return max(min_val, min(max_val, value))

def random_months():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    start = random.randint(0, 10)
    end = random.randint(start, min(start+2, 11))
    return f"{months[start]}-{months[end]}"

def tourist_footfall():
    return random.randint(50000, 2500000)

def crowd_risk_level(footfall):
    if footfall > 1500000:
        return "Very High"
    elif footfall > 900000:
        return "High"
    elif footfall > 400000:
        return "Medium"
    else:
        return "Low"

def pollution_risk(avg_aqi):
    if avg_aqi > 250:
        return "Very High"
    elif avg_aqi > 180:
        return "High"
    elif avg_aqi > 120:
        return "Medium"
    else:
        return "Low"

def water_risk_level(water_index):
    if water_index > 75:
        return "Severe"
    elif water_index > 50:
        return "High"
    elif water_index > 30:
        return "Moderate"
    else:
        return "Low"


# =====================================================
# 1) DESTINATIONS.CSV
# Columns:
# destination | waste_management_score | crowd_index | eco_hotels | avg_aqi | green_score | water_risk
# =====================================================
destination_rows = []

for _ in range(520):
    dest = random.choice(destinations)

    waste_management_score = random.randint(3, 10)
    crowd_index = random.randint(1, 10)
    eco_hotels = random.randint(10, 300)
    avg_aqi = random.randint(35, 420)

    # green_score calculation
    green_score = 100
    green_score -= (10 - waste_management_score) * 4
    green_score -= crowd_index * 4
    green_score -= (avg_aqi / 5)

    green_score += min(eco_hotels / 10, 20)

    green_score = round(clamp(green_score), 2)

    # water risk based on random water index
    water_index = random.randint(10, 90)
    water_risk = water_risk_level(water_index)

    destination_rows.append([
        dest,
        waste_management_score,
        crowd_index,
        eco_hotels,
        avg_aqi,
        green_score,
        water_risk
    ])

destinations_df = pd.DataFrame(destination_rows, columns=[
    "destination",
    "waste_management_score",
    "crowd_index",
    "eco_hotels",
    "avg_aqi",
    "green_score",
    "water_risk"
])

destinations_df.to_csv("destinations.csv", index=False)
print("✅ destinations.csv generated with", len(destinations_df), "rows")


# =====================================================
# 2) OVERTOURISM.CSV
# Columns:
# destination | peak_months | tourist_footfall | crowd_risk | pollution_risk
# =====================================================
overtourism_rows = []

for _ in range(520):
    dest = random.choice(destinations)

    peak_months = random_months()
    footfall = tourist_footfall()

    crowd_risk = crowd_risk_level(footfall)

    avg_aqi = random.randint(35, 420)
    pollution_level = pollution_risk(avg_aqi)

    overtourism_rows.append([
        dest,
        peak_months,
        footfall,
        crowd_risk,
        pollution_level
    ])

overtourism_df = pd.DataFrame(overtourism_rows, columns=[
    "destination",
    "peak_months",
    "tourist_footfall",
    "crowd_risk",
    "pollution_risk"
])

overtourism_df.to_csv("overtourism.csv", index=False)
print("✅ overtourism.csv generated with", len(overtourism_df), "rows")


# =====================================================
# 3) TRANSPORT_EMISSIONS.CSV
# Columns:
# vehicle_type | fuel_type | co2_per_km | pm2_5 | nox | avg_cost_per_km
# =====================================================
vehicles = [
    ("Car", "Petrol"),
    ("Car", "Diesel"),
    ("Car", "EV"),
    ("Bike", "Petrol"),
    ("Bike", "Electric"),
    ("Bus", "Diesel"),
    ("Bus", "CNG"),
    ("Train", "Electric"),
    ("Train", "Diesel"),
    ("Flight", "Domestic"),
    ("Flight", "International"),
]

transport_rows = []

for vtype, fuel in vehicles:
    for _ in range(50):  # total 500+ rows approx
        if vtype == "Car" and fuel == "Petrol":
            co2 = round(random.uniform(0.16, 0.25), 3)
        elif vtype == "Car" and fuel == "Diesel":
            co2 = round(random.uniform(0.18, 0.30), 3)
        elif vtype == "Car" and fuel == "EV":
            co2 = round(random.uniform(0.03, 0.09), 3)
        elif vtype == "Bike" and fuel == "Petrol":
            co2 = round(random.uniform(0.07, 0.12), 3)
        elif vtype == "Bike" and fuel == "Electric":
            co2 = round(random.uniform(0.01, 0.05), 3)
        elif vtype == "Bus":
            co2 = round(random.uniform(0.04, 0.09), 3)
        elif vtype == "Train":
            co2 = round(random.uniform(0.02, 0.06), 3)
        else:  # Flight
            co2 = round(random.uniform(0.18, 0.35), 3)

        pm2_5 = round(random.uniform(5, 90), 2)
        nox = round(random.uniform(10, 250), 2)

        if vtype == "Flight":
            cost = round(random.uniform(6, 20), 2)
        elif vtype == "Train":
            cost = round(random.uniform(0.8, 3), 2)
        elif vtype == "Bus":
            cost = round(random.uniform(1, 4), 2)
        elif vtype == "Bike":
            cost = round(random.uniform(0.5, 2), 2)
        else:
            cost = round(random.uniform(3, 10), 2)

        transport_rows.append([vtype, fuel, co2, pm2_5, nox, cost])

transport_df = pd.DataFrame(transport_rows, columns=[
    "vehicle_type",
    "fuel_type",
    "co2_per_km",
    "pm2_5",
    "nox",
    "avg_cost_per_km"
])

transport_df.to_csv("transport_emissions.csv", index=False)
print("✅ transport_emissions.csv generated with", len(transport_df), "rows")


# =====================================================
# 4) WATER_SCARCITY.CSV
# Columns:
# destination | water_index | drought_risk | water_alert_message
# =====================================================
water_rows = []

for _ in range(520):
    dest = random.choice(destinations)

    water_index = random.randint(10, 95)

    drought = water_risk_level(water_index)

    if drought == "Severe":
        msg = "Severe water scarcity. Avoid unnecessary water usage and prefer eco-hotels."
    elif drought == "High":
        msg = "High drought risk. Use water responsibly and avoid wastage."
    elif drought == "Moderate":
        msg = "Moderate water risk. Be mindful while travelling."
    else:
        msg = "Low water scarcity risk. Still avoid pollution of local water bodies."

    water_rows.append([dest, water_index, drought, msg])

water_df = pd.DataFrame(water_rows, columns=[
    "destination",
    "water_index",
    "drought_risk",
    "water_alert_message"
])

water_df.to_csv("water_scarcity.csv", index=False)
print("✅ water_scarcity.csv generated with", len(water_df), "rows")

print("\n🔥 ALL FILES GENERATED SUCCESSFULLY!")
