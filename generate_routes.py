import pandas as pd
import random

cities = [
    "Delhi","Agra","Jaipur","Udaipur","Mumbai","Pune","Nagpur","Bhopal","Indore",
    "Chandigarh","Shimla","Manali","Amritsar","Ludhiana","Jalandhar","Patiala",
    "Lucknow","Kanpur","Varanasi","Prayagraj","Patna","Ranchi","Kolkata",
    "Bhubaneswar","Cuttack","Hyderabad","Bengaluru","Chennai","Coimbatore",
    "Madurai","Kochi","Trivandrum","Goa","Surat","Ahmedabad","Vadodara",
    "Rajkot","Jodhpur","Ajmer","Dehradun","Haridwar","Rishikesh","Nainital",
    "Guwahati","Shillong","Gangtok","Srinagar","Leh","Jammu","Darjeeling"
]

road_types = ["Highway", "City", "Rural", "Hill Road", "Expressway"]
traffic_levels = ["Low", "Medium", "High"]
road_conditions = ["Good", "Moderate", "Bad"]
weather_risks = ["Low", "Medium", "High"]

data = []

for _ in range(500):
    source = random.choice(cities)
    destination = random.choice(cities)

    while destination == source:
        destination = random.choice(cities)

    base_distance = random.randint(50, 2000)

    # Popular Route
    traffic = random.choice(["Medium", "High"])
    avg_speed = random.randint(25, 55)
    fuel_eff = random.randint(10, 18)

    road_type = random.choice(road_types)
    toll_cost = random.randint(0, 1200)
    road_condition = random.choice(road_conditions)
    elevation_gain = random.randint(0, 3000)
    weather_risk = random.choice(weather_risks)

    data.append([source, destination, "Popular", base_distance, traffic, avg_speed, fuel_eff,
                 road_type, toll_cost, road_condition, elevation_gain, weather_risk])

    # Eco Route (slightly longer but better efficiency)
    eco_distance = base_distance + random.randint(10, 150)
    eco_traffic = random.choice(["Low", "Medium"])
    eco_speed = random.randint(45, 80)
    eco_fuel_eff = fuel_eff + random.randint(1, 5)

    eco_road_type = random.choice(road_types)
    eco_toll_cost = max(0, toll_cost - random.randint(0, 400))
    eco_road_condition = random.choice(["Good", "Moderate"])
    eco_elevation_gain = max(0, elevation_gain - random.randint(0, 800))
    eco_weather_risk = random.choice(["Low", "Medium"])

    data.append([source, destination, "Eco", eco_distance, eco_traffic, eco_speed, eco_fuel_eff,
                 eco_road_type, eco_toll_cost, eco_road_condition, eco_elevation_gain, eco_weather_risk])


df = pd.DataFrame(data, columns=[
    "source","destination","route_type","distance_km","traffic_level","avg_speed",
    "fuel_efficiency_kmpl","road_type","toll_cost","road_condition","elevation_gain","weather_risk"
])

df.to_csv("routes.csv", index=False)
print("✅ routes.csv generated successfully with", len(df), "rows")
