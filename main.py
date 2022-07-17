import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env file
load_dotenv("C:\Python\env data.env")

# Input for user stating what exercise they did. e.g. walked 5 km and ran for 1h
exercise = input("Tell me which exercises you did: ")

gender = "male"
weight_kg = 70
height_cm = 180
age = 27

# Nutritionix API
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,

}
exercise_configs = {
    "query": exercise,
    "gender": gender,
    "weight_kg": weight_kg,
    "height_cm": height_cm,
    "age": age
}
# Posting data to Nutrionix API and configuring exercise dictionary
response = requests.post(url=NUTRITIONIX_ENDPOINT, headers=headers, json=exercise_configs)
exercise_data = response.json()

# Sheety API
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
sheety_header = {
    "Authorization": os.getenv("Authorization"),
}
today = datetime.now()
exercise_date = today.strftime(f"%d/%m/%Y")
exercise_time = today.strftime(f"%H:%M:%S")

# Loop through every exercise and add a row to my workout sheet.
for exercise in exercise_data["exercises"]:
    sheety_config = {
        "workout": {
            "date": exercise_date,
            "time": exercise_time,
            "exercise": exercise["user_input"].title(),
            "duration": round(exercise["duration_min"]),
            "calories": round(exercise["nf_calories"]),
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_config, headers=sheety_header)

