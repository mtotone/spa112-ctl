#!/usr/bin/env python3

import re
import sys
import hashlib
import requests
import docopt
import termcolor

usage = """SPA112 Controller.

Usage:
	spa112-ctl.py [-h|--help]
	spa112-ctl.py (reset|reboot) (-i <ip>|--ip-address <ip>) [-l <login>|--login <login>] [-p <password>|--password <password>] 
	spa112-ctl.py --version

Commands:
	reboot		Reboot the SPA112.
	reset		Reset the SPA112.

Options:
	-h --help 		Show this screen.
	--version		Show the controller version.
	-i, --ip-address	SPA112 IP Address
	-l, --login		SPA112 login
	-p, --password		SPA112 password
"""

args = docopt.docopt(doc=usage, version='1.0')

def success(message):
	print('[ %s ] %s.' % (termcolor.colored('ok', 'green'), message))

def failure(message):
	sys.exit('[%s] %s ... %s' % (termcolor.colored('FAIL', 'red'), message, termcolor.colored('failed!', 'red')))

def post(url, data):
	try:
		r = requests.post(url, data=data, timeout=5)
	except requests.exceptions.Timeout:
		failure('Timeout from SPA112')
	except requests.exceptions.ConnectionError:
		failure('Could not connect to SPA112')
	except Exception as e:
		failure('Cannot post request to SPA112: %s' % (str(e)))

	try:
		return r.text
	except Exception as e:
		failure('Cannot retrieve SPA112 response: %s' % (str(e)))

def login(ip, user, password):
	return post('http://%s/login.cgi' % (ip), 'submit_button=login&keep_name=0&enc=1&user=%s&pwd=%s' % (user, encode_value(password)))

def reset(ip, session_id):
	result = post('http://%s/apply.cgi;session_id=%s' % (ip, session_id), 'submit_button=Factory_Defaults&gui_action=Apply&FactoryDefaults=1&VoiceDefaults=1&session_key=%s' % (session_id))
	check_result(result, 'reset')

def reboot(ip, session_id):
	result = post('http://%s/apply.cgi;session_id=%s' % (ip, session_id), 'submit_button=Reboot&gui_action=Apply&need_reboot=1&session_key=%s' % (session_id))
	check_result(result, 'reboot')

def check_result(result, action):
	if re.search('You will be returned to the Login page in (a )?few minutes', result):
		success('Successfully %s SPA112' % (action))
	else:
		failure('Cannot %s SPA112' % (action))

def get_session_id(regex, result):
	search = re.search(regex, result)
	if not search:
		failure('Missing session id in HTML result')
	else:
		session_id = re.sub(regex, r'\1', search.group())

	if not session_id:
		failure('Cannot extract session id from HTML result')

	return session_id

def md5sum(data):
	try:
        	return hashlib.md5(data.encode('utf-8')).hexdigest()
	except Exception as e:
		failure('Cannot generate md5sum: %s' % (str(e)))

def encode_value(data):
        password_changed = '%s%s' % (data, str(len(data)).zfill(2))
        while len(password_changed) < 64:
                password_changed += password_changed

        return md5sum(password_changed[0:64])

if not args['reboot'] and not args['reset']:
	sys.exit(usage)

regex = "var session_key='([0-9a-f]{32})';"
ip = args['<ip>']
user = 'admin' if not args['-l'] and not args['--login'] else args['<login>']
password= 'admin' if not args['-p'] and not args['--password'] else args['<password>']

login = login(ip, user, password)
session_id = get_session_id(regex, login)

if args['reboot']:
	reboot(ip, session_id)
elif args['reset']:
	reset(ip, session_id)
