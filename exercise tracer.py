import os
import requests
from datetime import datetime

AGE = 20
GENDER = "male"
WEIGHT_KG = 58
HEIGHT_CM = 183

APP_ID = os.environ["YOUR_APP_ID"]
API_KEY = os.environ.get("YOUR_API_KEY")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ.get("YOUR_SHEET_ENDPOINT")

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}
parameters = {
    "query": exercise_text,
    "age": AGE,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM

}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(response.text)


# ################### Sheety part #################################################
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
bearer_headers = {
    "Authorization": f"Bearer {os.environ.get('YOUR_TOKEN')}"
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheety_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)
