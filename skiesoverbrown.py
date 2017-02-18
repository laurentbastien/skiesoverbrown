import pprint
import os
from tweepy import OAuthHandler, API
from markovbot import MarkovBot
from random import sample
from time import sleep
from math import radians, cos, sin, asin, sqrt
import re
import math
import requests

#Put your keys
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

#Aircraft API
url = requests.get('https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat=40.807496&lng=-73.963151&fDstL=0&fDstU=30')
pprinter = pprint.PrettyPrinter(indent=4)
data = url.json()

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)

#Calculate distance. 
R = 6373.0
40.807502, -73.963279
lat1 = radians(40.807502)
lon1 = radians(-73.963279)

#Function to calculate for distance
def myfunction(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

#Set up the Markovbot module. 
tweetbot = MarkovBot()
# Get the current directory's path
dirname = os.path.dirname(os.path.abspath('/Users/normandcorbeil/Desktop/computational_journalism/bot/'))
# Construct the path to the book
book = os.path.join(dirname,'/Users/normandcorbeil/Desktop/computational_journalism/bot/Webook.txt')
# Make your bot read the book!
tweetbot.read(book)

previous_airplane = ''
sentences = []
f = open('WeBook.txt') 

#I picked 5 km, but feel free to play with the distance a bit.
while True:
    for item in data["acList"]:
        if "FBI" in item.get('Op', "None") or "Police" in item.get('Op', "None") or "DEA" in item.get('Op', "None") or "Homeland" in item.get('Op', "None"):
            if myfunction(40.807487, -73.963265, item["Lat"], item["Long"]) < 5:
                my_first_text = tweetbot.generate_text(10)
                api.update_status(my_first_text)
                sleep(300)
            if myfunction(40.807487, -73.963265, item["Lat"], item["Long"]) > 5:
                for i in f:
                    sentences += re.findall(r".*?[\.\!\?]+", f.read()) 
                    selected = sample(sentences, 1)
                    api.update_status(selected[0])
                    sleep(300)
    






