import pandas as pd
import random

# -------------------------------
# Cities list (India + extra)
# -------------------------------
cities = [
    "Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Hyderabad", "Pune", "Ahmedabad",
    "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Patna", "Ranchi",
    "Raipur", "Bhubaneswar", "Guwahati", "Chandigarh", "Shimla", "Manali", "Agra",
    "Varanasi", "Amritsar", "Jodhpur", "Udaipur", "Surat", "Vadodara", "Nashik",
    "Aurangabad", "Noida", "Gurgaon", "Faridabad", "Ghaziabad", "Meerut", "Dehradun",
    "Haridwar", "Jammu", "Srinagar", "Leh", "Gangtok", "Shillong", "Imphal",
    "Itanagar", "Kochi", "Thiruvananthapuram", "Mysore", "Coimbatore", "Madurai",
    "Vijayawada", "Visakhapatnam", "Tirupati", "Mangalore", "Goa", "Panaji",
    "Ludhiana", "Jalandhar", "Bathinda", "Hisar", "Rohtak", "Ambala", "Karnal",
    "Gwalior", "Jabalpur", "Bilaspur", "Durg", "Siliguri", "Darjeeling", "Dhanbad",
    "Jamshedpur", "Allahabad", "Bareilly", "Moradabad", "Aligarh", "Mathura",
    "Gaya", "Muzaffarpur", "Sambalpur", "Cuttack", "Rourkela", "Kharagpur",
    "Haldia", "Asansol", "Nainital", "Mussoorie", "Rishikesh", "Katra", "Kullu"
]

# -------------------------------
# Helper functions
# -------------------------------
def random_yes_no(prob_yes=0.6):
    return "Yes" if random.random() < prob_yes else "No"

def random_bus_frequency():
    return random.choice(["Low", "Medium", "High", "Very High"])

def random_aqi():
    return random.randint(35, 450)

def calculate_green_score(aqi, metro, ev, bicycle, bus):
    score = 100

    # AQI impact
    if aqi > 300:
        score -= 50
    elif aqi > 200:
        score -= 35
    elif aqi > 150:
        score -= 25
    elif aqi > 100:
        score -= 15
    else:
        score -= 5

    # Metro impact
    if metro == "Yes":
        score += 15

    # EV stations impact
    score += min(ev // 20, 20)

    # Bicycle rentals impact
    if bicycle == "Yes":
        score += 10

    # Bus frequency impact
    if bus == "Very High":
        score += 15
    elif bus == "High":
        score += 10
    elif bus == "Medium":
        score += 5
    else:
        score += 0

    # clamp score between 0 and 100
    return max(0, min(100, score))


# -------------------------------
# Generate 500+ rows
# -------------------------------
rows = []
for _ in range(520):  # you can increase this if you want 1000 rows
    city = random.choice(cities)

    metro_available = random_yes_no(0.4)  # metro less common
    bicycle_rentals = random_yes_no(0.55)

    # EV stations depends on metro presence (more stations if metro exists)
    if metro_available == "Yes":
        ev_stations = random.randint(30, 300)
    else:
        ev_stations = random.randint(0, 80)

    bus_frequency = random_bus_frequency()
    avg_aqi = random_aqi()

    green_score = calculate_green_score(
        avg_aqi, metro_available, ev_stations, bicycle_rentals, bus_frequency
    )

    rows.append([
        city,
        metro_available,
        ev_stations,
        bicycle_rentals,
        bus_frequency,
        avg_aqi,
        green_score
    ])


# -------------------------------
# Save to CSV
# -------------------------------
df = pd.DataFrame(rows, columns=[
    "city",
    "metro_available",
    "ev_stations",
    "bicycle_rentals",
    "bus_frequency",
    "avg_aqi",
    "green_score"
])

df.to_csv("city_transport.csv", index=False)

print("✅ city_transport.csv generated successfully with", len(df), "rows!")
