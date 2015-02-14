# -*- coding: utf-8 -*-
from time import time
import subprocess
import re
import shlex

"""
	Requires: amixer.

	Copied from https://github.com/viggee/configi3
	Modified by tethik.
"""

class Py3status:
	def volume(self, i3s_output_list, i3s_config):
		data = subprocess.check_output(['amixer', '-M', '-c', '0', 'sget', 'Master']).decode('utf-8')
		volumeobj = re.search(r"\[.*%\]", data, re.M)
		volume = int(volumeobj.group()[1:-2])

		status = re.search(r"\[on\]", data, re.M)
		if status == None:
			volumeicon = " "
		else:
			volumeicon = " "
		volumestr = volumeicon + "{:3.0f}".format(volume) + "%"

		response = {'full_text': '', 'name': 'volume'}
		response['color'] = "#268bd2"
		response['full_text'] = volumestr
		response['cached_until'] = time() + 60
		return (0, response)

	def on_click(self, i3s_output_list, i3s_config, event):
		if event['button'] == 1:
			subprocess.Popen(shlex.split("amixer -q set Master toggle"))
		if event['button'] == 4:
			subprocess.Popen(shlex.split("amixer -q set Master 5%+ unmute"))
		if event['button'] == 5:
			subprocess.Popen(shlex.split("amixer -q set Master 5%- unmute"))
		subprocess.Popen(["killall", "-USR1", "py3status"])

if __name__ == "__main__":
	"""
	Test this module by calling it directly.
	"""
	from time import sleep
	x = Py3status()
	x.on_click(None, [], {'button':1})
	while True:
	    print(x.volume([], {}))
	    sleep(1)
