import time
import config
import requests
import pandas
from chat_message import ChatMessage
from iss_position import IssPosition

default_coordinates = {
    "lat": 0,
    "lng": 0,
}

# while True:
time.sleep(2)
user_coordinates = pandas.DataFrame(default_coordinates, index=[0])
user_coordinates.to_csv("user_coordinates.csv", index=False)

chat_message = ChatMessage()
iss_position = IssPosition()

r = requests.get(f"https://api.telegram.org/bot{config.TOKEN}/getUpdates").json()["result"]
print(r)
num_messages = int(len(r))
chat_message.start()



# chat_message.check_iss_and_send_messages()
