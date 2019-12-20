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


import bluetooth, binascii, sys, datetime
from time import sleep

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
			require("TurnLeftKeyword").build()
		self.register_intent(turn_left_intent, self.handle_turn_left_intent)

		turn_right_intent = IntentBuilder("TurnRightIntent"). \
			require("TurnRightKeyword").build()
		self.register_intent(turn_right_intent, self.handle_turn_right_intent)

		go_ahead_intent = IntentBuilder("GoAheadIntent"). \
			require("GoAheadKeyword").build()
		self.register_intent(go_ahead_intent, self.handle_go_ahead_intent)

		go_back_intent = IntentBuilder("GoBackIntent"). \
			require("GoBackKeyword").build()
		self.register_intent(go_back_intent, self.handle_go_back_intent)

		stop_intent = IntentBuilder("StopIntent"). \
			require("StopKeyword").build()
		self.register_intent(stop_intent, self.handle_stop_intent)

		self.bluetoothModuleMACAddress = '80:C3:C2:54:52:9B'  # you need to modify this
		self.port = 1

		self.open_connection_with_car()
		self.stop()

	def open_connection_with_car(self):
		print( "Before to use the Smart Car skill, remember to pair  \
				computer and HC-06 Arduino module. No need to connect them manually!" )

		# Bluetooth SPP, which the HC-06 (or simular) Arduino bluetooth module uses
		self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  # RFCOMM is client-server protocol (client asks services and server replies), similar to TCP/IP
		self.s.connect((self.bluetoothModuleMACAddress, self.port))

		print( "At this point, the HC-06 blinking blue led gets stable blue, i.e. connected" )

	def close_bluetooth_connection(self):
		self.s.close()

	def send_via_bluetooth(self, string):
		try:
			self.s.send(string)
		except bluetooth.btcommon.BluetoothError:
			print("BluetoothError, trying to reconnect to smart car")
			self.open_connection_with_car()
			self.send_via_bluetooth(string)

	def handle_go_ahead_intent(self, message):
		init = datetime.datetime.now()
		while True:
			self.goAhead()
			delta = datetime.datetime.now() - init
			sec = delta.seconds
			if sec >= 0.5:  # 500 ms
				self.stop()
				break
			sleep(0.1) # 100 ms

		self.speak_dialog("done")

	def handle_go_back_intent(self, message):
		init = datetime.datetime.now()
		while True:
			self.goBack()
			delta = datetime.datetime.now() - init
			sec = delta.seconds
			if sec >= 0.5:  # 500 ms
				self.stop()
				break
			sleep(0.1) # 100 ms

		self.speak_dialog("done")

	def handle_turn_left_intent(self, message):
		# then left
		init = datetime.datetime.now()
		while True:
			self.turnLeft()
			delta = datetime.datetime.now() - init
			sec = delta.seconds
			if sec >= 0.5:  # 500 ms
				self.stop()
				break
			sleep(0.1) # 100 ms

		self.speak_dialog("done")

	def handle_turn_right_intent(self, message):
		# then right
		init = datetime.datetime.now()
		while True:
			self.turnRight()
			delta = datetime.datetime.now() - init
			sec = delta.seconds
			if sec >= 0.5:  # 500 ms
				self.stop()
				break
			sleep(0.1) # 100 ms

		self.speak_dialog("done")

	def handle_stop_intent(self, message):
		self.stop()
		self.speak_dialog("stop")


	########### low level functions

	def goAhead(self):
		print("go ahead")
		self.send_via_bluetooth('goa')

	def goBack(self):
		print("go back")
		self.send_via_bluetooth('gob')

	def turnLeft(self):
		print("turn left")
		self.send_via_bluetooth('tlf')

	def turnRight(self):
		print("turn right")
		self.send_via_bluetooth('trg')

	def stop(self):
		print("stop")
		init = datetime.datetime.now()
		while True:
			self.send_via_bluetooth('stp')
			delta = datetime.datetime.now() - init
			sec = delta.seconds
			if sec >= 0.4:  # 400 ms
				break
			sleep(0.1) # 100 ms


def create_skill():
	return HerrAugustSmartCarSkill()
