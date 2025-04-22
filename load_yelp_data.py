import sqlite3
import json

def connect_db():
    return sqlite3.connect("meals.db")

def load_meals():
    conn = connect_db()
    cur = conn.cursor()

    with open("yelp_data.json", "r") as f:
        data = json.load(f)

    count = 0
    for item in data:
        name = item["Popular_dish"]
        restaurant = item["restaurant name"]
        rating = item["rating"]

        try:
            cur.execute("""
                INSERT OR IGNORE INTO Meals (name, restaurant, rating)
                VALUES (?, ?, ?)
            """, (name, restaurant, rating))
            count += 1
            if count >= 25:  # idk if this is right but loading all 100 of yelps data 
                break
        except Exception as e:
            print(f"Error inserting {name}: {e}")
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_meals()