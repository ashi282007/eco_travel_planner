import sqlite3

conn = sqlite3.connect("eco_data.db")
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# FEEDBACK
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# DESTINATIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS destinations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination TEXT UNIQUE NOT NULL,
    sustainability_score INTEGER NOT NULL,
    aqi_level TEXT NOT NULL,
    water_scarcity TEXT NOT NULL,
    over_tourism TEXT NOT NULL
)
""")

# TRANSPORT AVAILABILITY
cursor.execute("""
CREATE TABLE IF NOT EXISTS transport(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination TEXT UNIQUE NOT NULL,
    bicycle_available TEXT NOT NULL,
    ev_available TEXT NOT NULL,
    metro_available TEXT NOT NULL
)
""")

# ECO ROUTES
cursor.execute("""
CREATE TABLE IF NOT EXISTS eco_routes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    destination TEXT NOT NULL,
    best_route TEXT NOT NULL,
    distance_km REAL NOT NULL,
    fuel_saved REAL NOT NULL,
    co2_saved REAL NOT NULL
)
""")

# QUIZ QUESTIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

# ------------------ INSERT SAMPLE DATA ------------------

cursor.execute("""
INSERT OR IGNORE INTO destinations(destination, sustainability_score, aqi_level, water_scarcity, over_tourism)
VALUES
('Delhi', 60, 'High', 'High', 'High'),
('Mumbai', 65, 'High', 'Medium', 'High'),
('Chandigarh', 85, 'Low', 'Low', 'Low'),
('Shimla', 80, 'Medium', 'Medium', 'Medium'),
('Manali', 78, 'Low', 'Medium', 'High'),
('Goa', 70, 'Medium', 'High', 'High')
""")

cursor.execute("""
INSERT OR IGNORE INTO transport(destination, bicycle_available, ev_available, metro_available)
VALUES
('Delhi', 'Yes', 'Yes', 'Yes'),
('Mumbai', 'No', 'Yes', 'Yes'),
('Chandigarh', 'Yes', 'Yes', 'No'),
('Shimla', 'Yes', 'No', 'No'),
('Goa', 'Yes', 'Yes', 'No')
""")

cursor.execute("""
INSERT OR IGNORE INTO eco_routes(source, destination, best_route, distance_km, fuel_saved, co2_saved)
VALUES
('Delhi', 'Chandigarh', 'Train', 250, 5.2, 12.3),
('Delhi', 'Shimla', 'Bus', 350, 3.5, 9.1),
('Mumbai', 'Goa', 'Train', 590, 8.8, 20.0),
('Delhi', 'Manali', 'Bus', 540, 6.0, 16.5)
""")

cursor.execute("""
INSERT OR IGNORE INTO quiz(question, option1, option2, option3, option4, answer)
VALUES
('Which transport produces least CO₂?', 'Car', 'Bus', 'Train', 'Flight', 'Train'),
('What is the best eco habit?', 'Plastic bottles', 'Reuse water bottle', 'Throw waste', 'Burn garbage', 'Reuse water bottle'),
('Over-tourism means?', 'Too few tourists', 'Too many tourists', 'Eco travel', 'Clean city', 'Too many tourists')
""")

conn.commit()
conn.close()

print("✅ Database created and updated successfully.")
