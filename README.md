# DanceParty
EE250 Final Project 

## Team Member Names 
Emily London

## Demo Video Link
https://www.youtube.com/watch?v=aU3Hequax4g

## Installation Guide 

### On Node 1: Host Computer 

#### Activate virtual environment
``` 
python3 -m venv ./venv
source venv/bin/activate
```
#### Install Required Libraries to run ytSearch.py
##### Install Google Ai Python Client 
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
##### Install Paho-MQTT 
```
pip3 install paho-mqtt
```
#### Run code 
```
python3 ytSearch.py
```

### On Node 2: Raspberry Pi
#### Activate virtual environment 
``` 
python3 -m venv ./venv
source venv/bin/activate
```
#### Install yt-dl 
```
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
```
#### Install ffmpeg 
```
sudo apt-get install ffmpeg
```
#### Install requisite libraries
##### Install Paho-MQTT
```
pip3 install paho-mqtt
```
##### Install scipy 
```
pip3 install scipy
```
##### Install numpy
```
pip3 install numpy
```
##### Install pigpio
```
sudo apt-get install pigpio python-pigpio python3-pigpio
pip3 install pigpio
```
##### Install pigpio-encoder
```
pip install pigpio_encoder
```
#### Run code 
```
sudo pigpiod
python3 playLights.py
```

### All External Libraries Used 
paho-mqtt
youtube-dl 
numpy
scipy
pigpiod
pigpiod-encoder
Google API Python Client 
