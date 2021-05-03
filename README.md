# DanceParty
EE250 Final Project 

Install yt-dl 
```
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
```

Open venv
run:
``` 
python3 -m venv ./venv
source venv/bin/activate
pip3 install youtube_dl
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip
deactivate
```

Install ffmpeg
```
sudo apt-get install ffmpeg
```
and macOS use the command:
```
brew install ffmpeg
```
Install Certificate Command: 
run: 
```
/Applications/Python\ 3.7/Install\ Certificates.command
```
Install Paho-Mqtt
```
pip3 install paho-mqtt
```
Install Librosa, Numpy, and PyGame
```
pip3 install librosa
pip3 install numpy 
pip3 install pygame
pip3 install scipy
sudo apt-get install libatlas-base-dev
sudo apt-get install libsdl-ttf2.0-0

```

Install pigpio for LED strip and start the daemon

```
pip3 install pigpio
sudo pigpiod 

```

Install GrovePi stuff 

```
curl -kL dexterindustries.com/update_grovepi | bash
```