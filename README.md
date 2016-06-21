# kerktelefoon

This script allows you to listen to an audio stream. It was meant to be run from a raspberry pi. It will turn on your TV (if it supports HDMI-CEC) and will shutdown the raspberry pi when the TV is turned off.

## To use
1. download or git clone this repo on your pi
3. install dependencies
  * feh to display the image (on raspbian: ```sudo apt-get install feh```)
  * omxplayer to play the audio stream (installed by default on raspbian)
  * cec-client from cec-utils (the one available in the raspbian repos does not work, you'll have to compile from scratch)
2. ```ln -s <path_to_repo>/kerktelefoon.desktop ~/.config/autostart/``` to autostart the script at boot.
