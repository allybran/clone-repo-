# this will be where we visualize the data 

import sqlite3
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

def connect_db():
    return sqlite3.connect("meals.db") #connect to meals database



def load_data_for_visualization(): #grab the data we are going to use
    conn = connect_db()
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT Meals.name, Meals.rating, Recipes.popularity, Recipes.cuisine,
               Nutrition.calories, Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
        JOIN Recipes ON Meals.id = Recipes.meal_id
    """, conn)
    conn.close()
    return df

def make_visuals(): #creating graphs

    df = load_data_for_visualization()

    print(df.head()) #debug check
    print(df.shape)

    #trying to convert columns to numbers 
    numeric_columns = ["calories", "fat_g", "sugar_g", "protein_g", "rating"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["name"] = df["name"].astype(str)
    df = df.dropna(subset=["rating", "name"]) # Drop any rows with missing ratings or names

     
    top10 = df.sort_values("rating", ascending=False).head(10)

    
    #bar chart of 10 most popular recipes
    df.set_index("name")[["rating"]].head(10).plot(kind="bar", stacked=False)
    plt.xticks(rotation=45, ha='right')
    plt.title("Top 10 Meals by Yelp Rating")
    plt.ylabel("Rating")
    plt.ylim(0, 5)
    plt.tight_layout()
    plt.show()

    # Scatterplot - calories vs popularity
    sns.scatterplot(data=df, x="calories", y="rating")
    plt.title("Calories vs Yelp Rating")
    plt.xlabel("Calories")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.show()

    # stacked bar chart - 10 meals with macronutrients 
    df.set_index("name")[["fat_g", "sugar_g", "protein_g"]].head(10).plot(kind="bar", stacked=True)
    plt.title("Macronutrient Breakdown (Top 10 Meals)")
    plt.ylabel("Grams")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Boxplot of calories by cuisine type
    sns.boxplot(data=df, x="cuisine", y="calories")
    plt.title("Calories by Cuisine Type")
    plt.xlabel("Cuisine")
    plt.ylabel("Calories")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    make_visuals()