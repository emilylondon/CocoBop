from __future__ import unicode_literals
import paho.mqtt.client as mqtt 
from apiclient.discovery import build

#API key for YouTube Search API
apikey = "AIzaSyBMfPWXD-sXoNLRZCUiYCknKrGApSicxwc"
youtube = build('youtube', 'v3', developerKey=apikey)

def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    
    #Youtube Search code 
    while True: 
        searchTerm= input('Enter search query:  ')
        req = youtube.search().list(q=searchTerm, part='snippet', type = 'video', maxResults=5) #parameteres for youtube search list api 
        res = req.execute()

        #Displays search results 
        for i in range(5):
            print(str(i+1) + ": " + res['items'][i]['snippet']['title'])

        select = int(input('Enter number to select song: '))
        ytUrl="https://www.youtube.com/watch?v=" + res['items'][select-1]['id']['videoId']
        client.publish("emilylondon/yturl", ytUrl)