from __future__ import unicode_literals
from youtube_dl import YoutubeDL
from apiclient.discovery import build
import os
import json

#API key for YouTube Search API
apikey = "AIzaSyBMfPWXD-sXoNLRZCUiYCknKrGApSicxwc"
youtube = build('youtube', 'v3', developerKey=apikey)

#Logger for conversion to mp3 
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

#Configuration for downloading the youtube video as an mp3 
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
}

while True: 
    searchTerm= input('Enter search query:  ')
    req = youtube.search().list(q=searchTerm, part='snippet', type = 'video', maxResults=5)
    res = req.execute()

    for i in range(5):
        print(str(i+1) + ": " + res['items'][i]['snippet']['title'])

    select = int(input('Enter number to select song: '))
    ytUrl="https://www.youtube.com/watch?v=" + res['items'][select-1]['id']['videoId']

    try:
        print('Youtube Downloader'.center(40, '_'))
        
        URL = ytUrl
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])
        os.rename(res['items'][select-1]['snippet']['title']+"-"+res['items'][select-1]['id']['videoId']+".mp3", "newSong.mp3")
        os.system("omxplayer " + "newSong.mp3")


    
    except Exception:
      
        print("Couldn\'t download the audio")
    
    finally:
      
        option = int(input('\n1.download again \n2.Exit\n\nOption here :'))
        
        if option!=1:
        
            break
