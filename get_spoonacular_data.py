import sqlite3
import requests

# Spoonacular API key
spoonacular_key = "d87ae0d7f57e4098872d6785d197b3de"

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect("meals.db")

# Get recipe info from Spoonacular and store in the database
def get_spoonacular_data():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM Meals")
    meals = cur.fetchall()

    base_url = "https://api.spoonacular.com/recipes/complexSearch"
    count = 0

     # Loop through each meal in the database
    for meal_id, name in meals:
        try:
            print(f"spoonacular for: {name}") #debug

            params = {
                "query": name,
                "apiKey": spoonacular_key,
                "number": 1
            }
             # Making API request to get recipe info
            res = requests.get(base_url, params=params)
            data = res.json()

             # If recipe found, extract the info
            if "results" in data and data["results"]:
                recipe = data["results"][0]
                popularity = recipe.get("aggregateLikes", 0)
                dish_types = ", ".join(recipe.get("dishTypes", []))
                cuisines = ", ".join(recipe.get("cuisines", []))

            # Insert the recipe info into the Recipes table
                cur.execute("""
                    INSERT OR IGNORE INTO Recipes (meal_id, popularity, dish_type, cuisine)
                    VALUES (?, ?, ?, ?)
                """, (meal_id, popularity, dish_types, cuisines))

                print(f"recipe: {name} (popularity: {popularity})") #debugging
                count += 1
                if count >= 25:
                    break

        except Exception as e:
            print(f"Error fetching Spoonacular data for '{name}':", e)
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    get_spoonacular_data()