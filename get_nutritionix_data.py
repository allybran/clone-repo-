import sqlite3
import requests

app_id = "7b857982"
app_key = "147987eb843d733fd4bd746545c15e0d"

#connects to the database
def connect_db():
    return sqlite3.connect("meals.db")


def get_nutrition_facts(): 
    conn, cur = connect_db()

    cur.execute("SELECT id, name FROM meals") #SQL SELECT query
    meals = cur.fetchall()
    
    #inputting my personalized api keys
    headers = {
        "x-app-id": app_id,
        "x-app-key": app_key,
        "Content-Type": "application/json",
    }
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients" 
    count = 0 #keeping track of how many foods i put into the api 
    
    for meal_id, food_item in meals: #loop through each meal in the database
        try: 
            response =requests.post(url, headers=headers, json={"query":food_item})

            #debug checking
            print(f"Querying Nutritionix for: {food_item}")
            print(response.status_code)
            print(response.text)

            food = response.json()["foods"][0] #this is going to accept the first match of the search
            #inserting nutrition info with SQL parameters
            cur.execute(""" 
                INSERT OR IGNORE INTO Nutrition (meal_id, calories, fat_g, sugar_g, protein_g)
                VALUES (?, ?, ?, ?, ?)
            """,(meal_id, food["nf_calories"], food["nf_total_fat"], food["nf_sugars"], food["nf_protein"]))
            print(food_item)
            count += 1 
            if count >= 25: 
                break
        except: 
            continue
    conn.commit()
    conn.close()

if __name__ == "__main__":
    get_nutrition_facts()