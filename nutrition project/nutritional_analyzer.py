# nutrition.py
import requests

APP_ID = "06d03dbf"
APP_KEY = "954acedac20250952b6265158bfa3477"
NUTRITIONIX_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "Content-Type": "application/json"
}

def get_nutrition_data(query):
    data = {"query": query}
    response = requests.post(NUTRITIONIX_URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def parse_food_nutrients(data):
    result = {}
    for food in data["foods"]:
        name = food["food_name"].title()
        nutrients = {
            "Protein (g)": round(food.get("nf_protein", 0), 2),
            "Carbs (g)": round(food.get("nf_total_carbohydrate", 0), 2),
            "Fiber (g)": round(food.get("nf_dietary_fiber", 0), 2),
            "Fats (g)": round(food.get("nf_total_fat", 0), 2),
            "Sat. Fat (g)": round(food.get("nf_saturated_fat", 0), 2),
            "Potassium (mg)": round(food.get("nf_potassium", 0), 2),
            "Phosphorus (mg)": round(food.get("nf_p", 0), 2),
            "Calories (kcal)": round(food.get("nf_calories", 0), 2),
        }

        full_nutrients = {item["attr_id"]: item["value"] for item in food.get("full_nutrients", [])}
        nutrients["Calcium (mg)"] = round(full_nutrients.get(301, 0), 2)
        nutrients["Iron (mg)"] = round(full_nutrients.get(303, 0), 2)

        result[name] = nutrients
    return result