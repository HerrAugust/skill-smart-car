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


import bluetooth
import binascii

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'HerrAugust'

LOGGER = getLogger(__name__)


class SmartLampSkill(MycroftSkill):
	def __init__(self):
		super(SmartLampSkill, self).__init__(name="SmartLampSkill")

	def initialize(self):
		turn_on_lamp_intent = IntentBuilder("TurnOnLampIntent"). \
			require("TurnOnLampKeyword").build()
		self.register_intent(turn_on_lamp_intent, self.handle_turn_on_lamp_intent)

		turn_off_lamp_intent = IntentBuilder("TurnOffLampIntent"). \
			require("TurnOffLampKeyword").build()
		self.register_intent(turn_off_lamp_intent, self.handle_turn_off_lamp_intent)

		make_red_intent = IntentBuilder("MakeRedIntent"). \
			require("MakeRedKeyword").build()
		self.register_intent(make_red_intent, self.handle_make_red_intent)

		make_green_intent = IntentBuilder("MakeGreenIntent"). \
			require("MakeGreenKeyword").build()
		self.register_intent(make_green_intent, self.handle_make_green_intent)

		make_blue_intent = IntentBuilder("MakeBlueIntent"). \
			require("MakeBlueKeyword").build()
		self.register_intent(make_blue_intent, self.handle_make_blue_intent)


		# self.serverMACAddress = 'F4:4E:FD:D3:E5:EE'  # MAC of bluetooth device. You'll need to change it
		# self.port = 1
		self.open_bluetooth_connection()

	def open_bluetooth_connection(self):
		print("No BT address specified. Searching all nearby bluetooth devices for")
		print("the SPP service, which Chsmartbulb uses. (May take some time.)")
		
		# SPP
		uuid = "00001101-0000-1000-8000-00805F9B34FB"
		service_matches = find_service(uuid=uuid, address=addr)

		if len(service_matches) == 0:
			print("couldn't find the service")
			sys.exit(1)

		first_match = service_matches[0]
		self.port = first_match["port"]
		self.name = first_match["name"]
		self.host = first_match["host"]

		print("connecting to \"%s\" on %s" % (name, host))  # e.g., "connecting to "Serial Port Service - Channel 2" on F4:4E:FD:D3:E5:EE"

		self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  # RFCOMM is client-server protocol (client asks services and server replies), similar to TCP/IP
		self.s.connect((self.host, self.port))

	def close_bluetooth_connection(self):
		self.handle_turn_off_lamp_intent('')
		self.s.close()

	def h(self, v):
		return binascii.unhexlify(v)

	def handle_turn_on_lamp_intent(self, message):
		self.speak_dialog("wait")

		self.s.send(self.h('01fe0000538310000000000050ff0000'))

		self.speak_dialog("done")

	def handle_make_red_intent(self, message):
		self.speak_dialog("wait")

		self.s.send(self.h('01fe0000538310000000ff0050000000'))

		self.speak_dialog("done")

	def handle_make_green_intent(self, message):
		self.speak_dialog("wait")

		self.s.send(self.h('01fe000053831000ff00000050000000'))

		self.speak_dialog("done")

	def handle_make_blue_intent(self, message):
		self.speak_dialog("wait")

		self.s.send(self.h('01fe00005383100000ff000050000000'))

		self.speak_dialog("done")

	def handle_turn_off_lamp_intent(self, message):
		self.speak_dialog("wait")

		self.s.send(self.h('01fe0000538310000000000050000000'))

		self.speak_dialog("done")

	def stop(self):
		self.close_bluetooth_connection()


def create_skill():
	return SmartLampSkill()
