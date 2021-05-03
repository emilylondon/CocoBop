from __future__ import unicode_literals
import paho.mqtt.client as mqtt 
from youtube_dl import YoutubeDL
import os 
import time

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
    'outtmpl': 'newSong.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
}

#Default connection function, subscribes to the yturl topic
def on_connect(client, userdata, flags, rc):
    print("Connected to server with result code " + str(rc))

    client.subscribe("emilylondon/yturl")
    client.message_callback_add("emilylondon/yturl", download_audio)

#Audio Download Function
def download_audio(client, userdata, msg):
    try:
        ytLink= str(msg.payload).encode("utf-8")
        print(ytLink)
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([ytLink])
    except Exception:
        print("Error downloading")
#main
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    while True:
        time.sleep(1)
