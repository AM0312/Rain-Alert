import requests
from twilio.rest import Client

OWM_API_KEY = ""
LAT = 28.613939
LNG = 77.209023

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

parameters = {
    "appid": OWM_API_KEY,
    "lat": LAT,
    "lon": LNG,
    "exclude": "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall",
                        params=parameters)

response.raise_for_status()

weather_data = response.json()
hourly_data = weather_data["hourly"]
weather_slice = hourly_data[:12]

raining = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    raining = raining or (int(condition_code) < 700)

if raining:
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain. Bring an umbrella.",
        to="Your verified Number",
        from_="Twilio Trial Number")
    print(message.status)
