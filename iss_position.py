import time, datetime
from datetime import datetime
import pytz

import pandas
import requests

from geopy.geocoders import Nominatim


class IssPosition:
    def __init__(self):
        self.geolocator = None
        self.parameters = None
        self.iss_longitude = None
        self.iss_latitude = None
        self.response = None
        self.requests = None
        self.MY_LAT = 35.689487
        self.MY_LONG = 139.691711

    def get_position(self):
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        self.iss_latitude = float(data["iss_position"]["latitude"])
        self.iss_longitude = float(data["iss_position"]["longitude"])
        self.geolocator = Nominatim(user_agent="GOOGLE_API2")
        location = self.geolocator.reverse(f"{self.iss_latitude},{self.iss_longitude}")
        print(location)

        if self.MY_LAT - 5 <= self.iss_latitude <= self.MY_LAT + 5 and \
                self.MY_LONG - 5 <= self.iss_longitude <= self.MY_LONG + 5:
            return True

    def is_night(self):
        self.parameters = {
            "lat": self.MY_LAT,
            "lng": self.MY_LONG,
            "formatted": 0,
        }

        response_sat = requests.get("https://api.sunrise-sunset.org/json", params=self.parameters)
        response_sat.raise_for_status()
        data2 = self.response.json()
        sunrise = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data2["results"]["sunset"].split("T")[1].split(":")[0])

        time_now = datetime.now().hour

        if time_now >= sunset or time_now <= sunrise:
            return True
