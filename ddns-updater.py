#!/usr/bin/python
# coding=UTF-8

from urllib import urlopen
import socket
import subprocess

ip = '127.0.0.1'
PREV_UPDATE_FILE = '/Users/mac/.prev_ddns_update'
def check_ip(ip):
	try:
		socket.inet_aton(ip)
	except socket.error:
		print "IP is incorrect"
		return 0
	else:
		return ip

def get_ip_from_file(PREV_UPDATE_FILE):
	try:
		prev_update_file = open(PREV_UPDATE_FILE)
	except Exception, e:
		print "Couldn't open file: %s" % e
		ip = get_current_ip()
		if ip:
			update_file(PREV_UPDATE_FILE, ip)
		exit(0)
	else:
		try:
			ip = prev_update_file.readline()
		except Exception, e:
			print "Couldn't get ip from file: %s" % e
			ip = Null
		else:
			prev_update_file.close()
			return check_ip(ip)

def get_current_ip():
	try:
		ip = urlopen('http://automation.whatismyip.com/n09230945.asp').read()
	except Exception, e:
		print "Couldn't get current ip: %s" % e
		exit(0)
	else:
		return check_ip(ip)

def update_file(PREV_UPDATE_FILE, ip):
	try:
		file_ip = open(PREV_UPDATE_FILE, 'w')
		file_ip.write(ip)
		file_ip.close()
	except Exception, e:
		print "Could not update file: %s " % e
	return 1

def update_ddns(ip):
	UPDATE_CMD = ['/opt/local/bin/ez-ipupdate', '-c', '/Users/mac/.ddns', '-a', '%s' % ip]
	try:
		#print "trying to update ddns"
		fnull = open(os.devnull, 'w')
		if not subprocess.call(UPDATE_CMD, stdout = fnull):
			#print "Updated successfully"
			pass
		else:
			print "ez-ipupdate exited abnormally"
		fnull.close()
	except Exception, e:
		print "Couldn't update ddns: %s" % e
		exit(0)

def main():
	last_ip = get_ip_from_file(PREV_UPDATE_FILE)
	cur_ip = get_current_ip()
	if last_ip != cur_ip:
		update_ddns(cur_ip)
		update_file(PREV_UPDATE_FILE, cur_ip)
	else:
		#print "ip not changed"
		pass


if __name__ == "__main__":
	main()

