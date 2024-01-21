import requests
from twilio.rest import Client
import os

MY_LATITUDE = 51.759050  # Your latitude
MY_LONGITUDE = 19.458600  # Your longitude

# Get your own API Key by creating a free account on https://home.openweathermap.org/
OMW_api_key = os.environ.get("OWM_API_KEY")

TWILIO_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
your_phone_number = os.environ.get("MY_PHONE_NUMBER")
TWILIO_phone_number = "+18147525328"  # This is a random phone number that TWILIO will generate for you

OMW_EndPoint = "https://api.openweathermap.org/data/2.5/forecast"
parameters = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": OMW_api_key,
    "cnt": 4
}
# Get only the 4 hours interval of 3-hour forecast data
response = requests.get(url=OMW_EndPoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
condition_codes = [hour_data["weather"][0]["id"] for hour_data in weather_data["list"]]

# If any weather code within the next 12 hours is less than 700, than it's a snowy/rainy day
target_codes_list = [code for code in condition_codes if code < 700]

if len(target_codes_list) >= 1:
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    client = Client(TWILIO_account_sid, TWILIO_auth_token)

    # If any code starts with 6XX, then send the message with snowing info, any other case send rain info
    if len([snow_code for snow_code in target_codes_list if str(snow_code).startswith("6")]) >= 1:
        body_msg = "It's going to snow today ❄. Remember to bring a thick coat 🧥🧣🥶!"
    else:
        body_msg = "It's going to rain today. Remember to bring an ☔!"

    message = client.messages.create(body=body_msg, from_=TWILIO_phone_number, to=your_phone_number)

    print(message.status)
