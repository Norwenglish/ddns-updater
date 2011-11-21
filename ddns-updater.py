#!/usr/bin/python
# coding=UTF-8

from urllib import urlopen
import socket
import subprocess


host = 'trebuha.dyndns.org'
def check_ip(ip):
	try:
		socket.inet_aton(ip)
	except socket.error:
		print "IP is incorrect"
		return 0
	else:
		return ip

def get_ip_from_dns(host):
	DIG_CMD = ['/usr/bin/dig', '+short', host]
	try:
		 ip = subprocess.check_output(DIG_CMD).rstrip()
	except CalledProcessError as e:
		print "Dig error: %s" % e
		exit(0)
	except Exception, e:
		print "Couldn't get launch dig: %s" % e
		exit(0)
	else:
		return check_ip(ip)

def get_current_ip():
	try:
		ip = urlopen('http://automation.whatismyip.com/n09230945.asp').read()
	except Exception, e:
		print "Couldn't get current ip: %s" % e
		exit(0)
	else:
		return check_ip(ip)

def update_ddns(ip):
	UPDATE_CMD = ['/opt/local/bin/ez-ipupdate', '-c', '/Users/mac/.ddns', '-a', '%s' % ip]
	try:
		fnull = open(os.devnull, 'w')
		subprocess.check_call(UPDATE_CMD, stdout = fnull)
		fnull.close()
		return 1
	except CalledProcessError as e:
		print "ez-ipupdate exited abnormally: %s" % e
		exit(0)
	except Exception, e:
		print "Couldn't update ddns: %s" % e
		exit(0)

def main():
	last_ip = get_ip_from_dns(host)
	cur_ip 	= get_current_ip()
	if last_ip != cur_ip:
		update_ddns(cur_ip)
	else:
		#print "ip not changed"
		pass


if __name__ == "__main__":
	main()

