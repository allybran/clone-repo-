import sqlite3

#connects to the database
def connect_db():
    conn = sqlite3.connect("meals.db")
    cur = conn.cursor()
    return conn, cur

# create meals and nutrition tables
def create_tables():
    conn, cur = connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            restaurant TEXT,
            rating REAL,
            UNIQUE(name, restaurant)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            calories INTEGER,
            fat_g REAL,
            sugar_g REAL,
            protein_g REAL,
            FOREIGN KEY(meal_id) REFERENCES Meals(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            popularity REAL,
            dish_type TEXT,
            cuisine TEXT,
            FOREIGN KEY(meal_id) REFERENCES Meals(id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
