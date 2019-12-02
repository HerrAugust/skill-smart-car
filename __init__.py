# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.



# Credits to https://github.com/pfalcon/Chsmartbulb-led-bulb-speaker
# for showing how to use a bluetooth log from Android app in order to
# prepare a script and find out in a simple way the strings to be sent
# to the smart lamp to make it work


import sys

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'HerrAugust'

LOGGER = getLogger(__name__)


class HerrAugustSmartCarSkill(MycroftSkill):
	def __init__(self):
		super(HerrAugustSmartCarSkill, self).__init__(name="HerrAugustSmartCarSkill")

	def initialize(self):
		turn_left_intent = IntentBuilder("TurnLeftIntent"). \
			require("TurnLeftLampKeyword").build()
		self.register_intent(turn_left_intent, self.handle_turn_left_intent)

		turn_right_intent = IntentBuilder("TurnRightIntent"). \
			require("TurnRightKeyword").build()
		self.register_intent(turn_right_intent, self.handle_turn_left_intent)

		go_ahead_intent = IntentBuilder("GoAheadIntent"). \
			require("GoAheadKeyword").build()
		self.register_intent(go_ahead_intent, self.handle_go_ahead_intent)

		go_back_intent = IntentBuilder("GoBackIntent"). \
			require("GoBackKeyword").build()
		self.register_intent(go_back_intent, self.handle_go_back_intent)


		self.open_connection_with_car()

	def open_connection_with_car(self):
		# Bluetooth SPP, which the HC-06 (or simular) Arduino bluetooth module uses
		uuid = "00001101-0000-1000-8000-00805F9B34FB"
		service_matches = bluetooth.find_service(uuid=uuid, address=self.serverMACAddress)

		if len(service_matches) == 0:
			print("couldn't find the service")
			sys.exit(1)

		first_match = service_matches[0]
		self.port = first_match["port"]
		self.name = first_match["name"]
		self.host = first_match["host"]

		print("connecting to \"%s\" on %s" % (self.name, self.host))  # e.g., "connecting to "Serial Port Service - Channel 2" on F4:4E:FD:D3:E5:EE"

		self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  # RFCOMM is client-server protocol (client asks services and server replies), similar to TCP/IP
		self.s.connect((self.host, self.port))

	def close_bluetooth_connection(self):
		self.handle_turn_off_lamp_intent('')
		self.s.close()

	def send_via_bluetooth(self, string):
		try:
			self.s.send(self.h(string))
		except bluetooth.btcommon.BluetoothError:
			print("BluetoothError, trying to reconnect to smart lamp")
			self.open_connection_with_car()
			self.send_via_bluetooth(string)

	def h(self, v):
		return binascii.unhexlify(v)

	def handle_go_ahead_intent(self, message):
		self.send_via_bluetooth('8')

		print("go ahead done")
		self.speak_dialog("done")

	def handle_go_back_intent(self, message):
		self.send_via_bluetooth('2')

		print("go back done")
		self.speak_dialog("done")

	def handle_turn_left_intent(self, message):
		self.send_via_bluetooth('4')

		print("turn left done")
		self.speak_dialog("done")

	def handle_turn_right_intent(self, message):
		self.send_via_bluetooth('6')

		print("turn right done")
		self.speak_dialog("done")

	def stop(self):
		self.close_bluetooth_connection()


def create_skill():
	return HerrAugustSmartCarSkill()
