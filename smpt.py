import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 35.689487  # Your latitude
MY_LONG = 139.691711  # Your longitude


def is_iss_overheard():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])




    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overheard() and is_night():
        connection = smtplib.SMTP("smtp.telegmail.com")
        connection.starttls()
        connection.login("gjmibz@telegmail.com",)
        connection.sendmail(
            from_addr="gjmibz@telegmail.com",
            to_addrs="gjmibz@telegmail.com",
            msg="Subject:Look up\n\nThe ISS is above you in the sky"
        )