import time, datetime
from datetime import datetime
import pytz

import pandas
import requests

from geopy.geocoders import Nominatim
import config
from iss_position import IssPosition
import telegram
from telegram.ext import *

iss_position = IssPosition()


class ChatMessage:
    def __init__(self):
        self.num_messages = None
        self.ExtBot = None
        self.message = None
        self.fetched_cor = None
        self.check_messages = None
        self.location = None
        self.requests = None
        self.time_in_secs = None
        self.geolocator = None
        self.TOKEN = config.TOKEN
        self.GOOGLE_API = config.GOOGLE_API
        self.GOOGLE_API2 = config.GOOGLE_API2
        self.UTC = pytz.utc
        self.chat_id = "522466354"

    def start(self):
        # time.sleep(5)
        self.check_messages = requests.get(f"https://api.telegram.org/bot{self.TOKEN}/getUpdates").json()["result"]
        self.num_messages = int(len(self.check_messages))
        message_time = self.check_messages[self.num_messages - 1]["message"]["date"]
        message_time_test = datetime.utcfromtimestamp(message_time)
        message_time_test = message_time_test.strftime("%Y-%m-%d %H:%M:%S")
        print(message_time_test)
        print(datetime.now(self.UTC).strftime("%Y-%m-%d %H:%M:%S"))
        time_stamp = int(message_time)
        time_in_secs = round(datetime.now(self.UTC).timestamp())
        time.sleep(5)
        if time_in_secs - 15 <= time_stamp <= time_in_secs + 15 and \
                self.check_messages[self.num_messages - 1]["message"]["text"] == "/check" or \
                self.check_messages[self.num_messages - 1]["message"]["text"] == "/initiate":
            requests.get(f"https://api.telegram.org/bot{self.TOKEN}/"
                         f"sendMessage?chat_id={self.chat_id}&text=What is the name of your city?")
            time.sleep(5)
            get_message = requests.get(f"https://api.telegram.org/bot{self.TOKEN}/getUpdates").json()["result"]
            fetched_city = get_message[int(len(get_message)) - 1]["message"]["text"]
            self.geolocator = Nominatim(user_agent="GOOGLE_API2")
            coordinates = self.geolocator.geocode(f"{fetched_city}")
            df = pandas.DataFrame(coordinates)
            self.fetched_cor = df.to_dict()[0][1]
            data_format = {"lat": self.fetched_cor[0],
                           "lng": self.fetched_cor[1],
                           }
            data_format = pandas.DataFrame(data_format, index=[0])
            print(data_format)
            df = pandas.read_csv("user_coordinates.csv")
            df.update(data_format)
            df.to_csv("user_coordinates.csv", index=False)
            # df1 = pandas.concat([df, data_format], ignore_index=True)
            # df1.to_csv("user_coordinates.csv", index=False)

    # def check(self):
    #     if self.get_updates(message="/check"):
    #         print("User clicked /check")
    #         return True

    def check_iss_and_send_messages(self):
        user_coordinates_data = pandas.read_csv("user_coordinates.csv")
        message1 = "Look up !! ISS is over your head."
        message2 = f"Not yet.\nYour current position: {user_coordinates_data['lat']}, {user_coordinates_data['lng']} " \
                   f"\n\nISS current position: {iss_position.iss_latitude}, {iss_position.iss_longitude}"
        message3 = f"Location: {self.location}"
        message4 = f"Location: None to display"

        if iss_position.get_position() and iss_position.is_night():
            requests.get(f"https://api.telegram.org/bot{self.TOKEN}/"
                         f"sendMessage?chat_id={self.chat_id}&text={message1}")
        else:
            requests.get(f"https://api.telegram.org/bot{self.TOKEN}/"
                         f"sendMessage?chat_id={self.chat_id}&text={message2}")

        if self.location == "None":
            requests.get(f"https://api.telegram.org/bot{self.TOKEN}/"
                         f"sendMessage?chat_id={self.chat_id}&text={message4}")
        else:
            requests.get(f"https://api.telegram.org/bot{self.TOKEN}/"
                         f"sendMessage?chat_id={self.chat_id}&text={message3}")
