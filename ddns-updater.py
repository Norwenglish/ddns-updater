#!/usr/bin/python
# coding=UTF-8

from urllib import urlopen
from optparse import OptionParser
import socket
import subprocess
import logging
import os

logger = logging.getLogger('DDNS-UPDATER')

def check_ip(ip):
	logger = logging.getLogger('DDNS-UPDATER')
	try:
		socket.inet_aton(ip)
	except socket.error:
		logger.error("IP: %s is incorrect", ip)
		return 0
	else:
		return ip

def get_ip_from_dns(host):
	DIG_CMD = ['/usr/bin/dig', '+short', host]
	try:
		 ip = subprocess.check_output(DIG_CMD).rstrip()
	except subprocess.CalledProcessError:
		logger.error("Dig exited abnormally")
		exit(0)
	except Exception, e:
		logger.error("Couldn't get launch dig: %s" % e)
		exit(0)
	else:
		logger.debug("Last IP from DNS: %s", ip)
		return check_ip(ip)

def get_current_ip():
	try:
		ip = urlopen('http://automation.whatismyip.com/n09230945.asp').read()
	except Exception, e:
		logger.error("Couldn't get current ip: %s" % e)
		exit(0)
	else:
		logger.debug("Current IP from whatismyip: %s", ip)
		return check_ip(ip)

def update_ddns(ip):
	UPDATE_CMD = ['/opt/local/bin/ez-ipupdate', '-c', '/Users/mac/.ddns', '-a', '%s' % ip]
	try:
		fnull = open(os.devnull, 'w')
		subprocess.check_call(UPDATE_CMD, stdout = fnull)
		fnull.close()
		return 1
	except subprocess.CalledProcessError:
		logger.error("ez-ipupdate exited abnormally")
		exit(0)
	except Exception, e:
		logger.error("Couldn't update ddns: %s" % e)
		exit(0)

def main():
	parser = OptionParser(usage="usage: %prog [options]")
	parser.add_option("-H", "--host", dest="host", default = 'trebuha.dyndns.org',
					help="DDNS hostname")
	parser.add_option("-d", "--debug",
					action="store_true", dest="verbose", default=False,
					help="Verbose mode")

	(options, args) = parser.parse_args()
	if options.verbose:
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.INFO)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)

	last_ip = get_ip_from_dns(options.host)
	

	cur_ip 	= get_current_ip()
	
	if last_ip != cur_ip:
		logger.debug("Trying to update DDNS")
		update_ddns(cur_ip)
	else:
		logger.debug("IP is not changed")
		pass


if __name__ == "__main__":
	main()

