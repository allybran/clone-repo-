import sqlite3

def connect_db():
    return sqlite3.connect("meals.db")

def check_data():
    conn = connect_db()
    cur = conn.cursor()

    tables = ["Meals", "Nutrition", "Recipes"]

    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"{table} has {count} rows")
        except Exception as e:
            print(f"Error checking {table}: {e}")

    #Check if the join between all 3 tables would return results
    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM Meals
            JOIN Nutrition ON Meals.id = Nutrition.meal_id
            JOIN Recipes ON Meals.id = Recipes.meal_id
        """)
        join_count = cur.fetchone()[0]
        print(f"Rows with complete data (joined): {join_count}")
    except Exception as e:
        print("Error checking join:", e)

    conn.close()

if __name__ == "__main__":
    check_data()