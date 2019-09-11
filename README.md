# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/smile.svg' card_color='#22a7f0' width='50' height='50' style='vertical-align:bottom'/> Chsmartbulb for Mycroft
Mycroft skill to control a Chsmartbulb via voice commands.
Chsmartbulb is a bluetooth smart lamp that you can buy at https://www.amazon.it/Lunvon-Lampadina-Altoparlante-Intelligente-Multicolore/dp/B07D7THZS5/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=chsmartbulb&qid=1568228030&s=gateway&sr=8-1 (12 Euros).
The skill allows to turn the light on and off, change color and get its status (color, turned on?).

## About 
Mycroft skill to control a Chsmartbulb via voice commands.
Chsmartbulb is a bluetooth smart lamp.
The skill allows to turn the light on and off, change color and get its status (color, turned on?).

## Examples 
* "Turn the light on"
* "Turn the light off"
* "Red light"
* "Lamp status"

## Installation
Turn Mycroft on. Pair the smartbulb with Mycroft/Linux with

	hcitool scan  # to get the MAC address of your device
	bluetoothctl
	agent on
	scan on  # wait for your device's address to show up here
	scan off
	trust MAC_ADDRESS
	pair MAC_ADDRRESS
	connect MAC_ADDRESS 


Then, install the required packages and the skill

	sudo apt-get install bluetooth libbluetooth-dev bluez-tools
	sudo pip install pybluez
	mycroft-msm install https://github.com/HerrAugust/skill-smart-lamp.git/
	mycroft-cli-test

Of course, you need to register a Mycroft account.
Tested in Picroft Stable 2019-07-20 (https://github.com/MycroftAI/enclosure-picroft/) on Raspberry Pi 3B+ (September 2019), connected to microphone via external sound card and speaker via jack 3.5mm.

## Credits 
HerrAugust @ github.com

Credits to https://github.com/pfalcon/Chsmartbulb-led-bulb-speaker
for showing how to use a bluetooth log from Android app in order to
prepare a script and find out in a simple way the strings to be sent
to the smart lamp to make it work.

## Category
**IoT**

## Tags
#iot
#smartbulb
#chsmartbulb
#mycroft