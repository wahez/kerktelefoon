#!/usr/bin/env python3

import subprocess
import time
import sys
import os
import threading

NAME = 'Schaapskooi'
URL  = 'http://kerkdienstgemist.nl/streams/456.mp3'
BACKGROUND = '/home/pi/projects/kerktelefoon/kerkdienst.jpg'


TODO='''
logfile schrijven
'''


def set_display_no_sleep():
	subprocess.check_call('/usr/bin/xset s off'.split())


def shutdown():
	# blijkbaar werken sudo en subprocess niet goed samen
	# subprocess.check_call(['/usr/bin/sudo', '-n', '--', 'shutdown -h now'], shell=True)
	os.system('sudo shutdown -h now')


class CEC(object):
	def __init__(self, name):
		self._name = name
		self._thread = threading.Thread(target=self._run, daemon=True)
		self._thread.start()
	def _run(self):
		self._process = subprocess.Popen(('/usr/local/bin/cec-client -o %s' % NAME).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
		self._process.stdin.write(u'on 0\n') # turn tv on
		self._process.stdin.write(u'as\n')   # set this as active source
		self._process.stdin.flush()
		for line in self._process.stdout:
			sys.stdout.write(line)
			if line.strip().endswith(u'>> 0f:36'): # tv switching to standby
				self._process.kill()
				break
	def is_stopped(self):
		return not self._thread.is_alive()
	def _del_(self):
		self._thread.join()


class Player(object):
	def __init__(self, url):
		self._thread = threading.Thread(target=self._run, daemon=True)
		self._thread.start()
	def _run(self):
		image_process = subprocess.Popen(('/usr/bin/feh -F %s' % BACKGROUND).split())
		self._process = subprocess.call(('/usr/bin/omxplayer %s' % URL).split())
		image_process.kill()
	def is_stopped(self):
		return not self._thread.is_alive()
	def _del_(self):
		self._thread.join()


def run_checks():
	'''
	check and print:
		ip-address
		ping to 8.8.8.8
		hostname lookup
	'''
	pass


def run_player(cec):
	run_checks()
	player = Player(URL)
	while not cec.is_stopped() and not player.is_stopped():
		time.sleep(1)
	

def run():
	cec = CEC(NAME)
	set_display_no_sleep()
	while not cec.is_stopped():
		run_player(cec)
	shutdown()


if __name__ == '__main__':
	run()
