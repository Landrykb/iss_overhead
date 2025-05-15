import time, datetime
from datetime import datetime
import pytz

import pandas
import requests

from geopy.geocoders import Nominatim

import config

MY_LAT = 35.689487
MY_LONG = 139.691711
TOKEN = config.TOKEN
GOOGLE_API = config.GOOGLE_API
GOOGLE_API2 = config.GOOGLE_API2

UTC = pytz.utc


position_checking = True
while position_checking:
    time.sleep(2)
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    geolocator = Nominatim(user_agent="GOOGLE_API2")
    location = geolocator.reverse(f"{iss_latitude},{iss_longitude}")
    print(location)


    def is_iss_overheard():
        # Your position is within +5 or -5 degrees of the ISS position.
        if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
            return True


    def is_night():
        parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }

        response_sat = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response_sat.raise_for_status()
        data2 = response.json()
        sunrise = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data2["results"]["sunset"].split("T")[1].split(":")[0])

        time_now = datetime.now().hour

        if time_now >= sunset or time_now <= sunrise:
            return True


    chat_id = "522466354"
    response_tel = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
    check_messages = response_tel.json()["result"]
    # print(check_messages[0]["message"]["text"])
    num_messages = int(len(check_messages))

    message_time = check_messages[num_messages - 1]["message"]["date"]
    # message_time = datetime.utcfromtimestamp(message_time)
    # message_time = message_time.strftime("%Y-%m-%d %H:%M:%S")
    time_stamp = int(message_time)
    print(time_stamp)
    time_in_secs = round(datetime.now(UTC).timestamp())
    # if check_messages[num_messages - 1]["message"]["text"] == "/check" and time_stamp == datetime.now(UTC).strftime(
    #         "%Y-%m-%d %H:%M:%S"):

    if check_messages[num_messages - 1]["message"]["text"] == "/check" \
            and time_in_secs - 15 <= time_stamp <= time_in_secs + 15:
        # response2 = requests.get(f"https://api.telegram.org/bot{TOKEN}/"
        #                          f"sendMessage?chat_id={chat_id}&text=What is the name of your city?")
        # fetched_city = check_messages[num_messages - 1]["message"]["text"]
        # coordinates = geolocator.geocode(f"{fetched_city}")
        # df = pandas.DataFrame(coordinates)
        message1 = "Look up !! ISS is over your head."
        message2 = f"Not yet.\nYour current position: {MY_LAT}, {MY_LONG} " \
                   f"\n\nISS current position: {iss_latitude}, {iss_longitude}"
        message3 = f"Location: {location}"
        message4 = f"Location: None to display"

        if is_iss_overheard() and is_night():
            response2 = requests.get(f"https://api.telegram.org/bot{TOKEN}/"
                                     f"sendMessage?chat_id={chat_id}&text={message1}")
        else:
            response2 = requests.get(f"https://api.telegram.org/bot{TOKEN}/"
                                     f"sendMessage?chat_id={chat_id}&text={message2}")

        if location == "None":
            response2 = requests.get(f"https://api.telegram.org/bot{TOKEN}/"
                                     f"sendMessage?chat_id={chat_id}&text={message4}")
        else:
            response2 = requests.get(f"https://api.telegram.org/bot{TOKEN}/"
                                     f"sendMessage?chat_id={chat_id}&text={message3}")


