# MSN Bot
# by Whac
# July 13, 2012

# Thanks to:
# http://www.codeproject.com/Articles/17761/Connect-To-MSN-Messenger-Using-The-MSN-Protocol
# http://www.hypothetic.org/docs/msn/general/connections.php
# For login protocol :)

import socket
import urllib2

HOST = 'messenger.hotmail.com'
PORT = 1863
EMAIL = raw_input('Enter your email: ')
PASSWORD = raw_input('Enter your password: ')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3) # Timeout in seconds

try:
	s.connect((HOST, PORT))
	print 'Connected successfully to ', HOST, PORT
except:
	print 'Error connecting to ', HOST, PORT

# Structs: http://docs.python.org/library/struct.html

# Prints information
def read(extra = ''):
	info = str(s.recv(500))
	print extra + info
	return info.split(' ')

# Login protocol
s.send('VER 1 MSNP8 CVR0\n')
read('Version: ')
s.send('CVR 2 0x0409 win 4.10 i386 MSNMSGR 6.2.0208 MSMSGS ' + EMAIL + '\n')
read('Client Info: ')
s.send('USR 3 TWN I ' + EMAIL + '\n')
args = read('Notifcation Server: ')

# The notification server information
notif_server_info = args[3].split(':')
notif_server_ip = notif_server_info[0]
notif_server_port = int(notif_server_info[1])

s.close()
print 'Connection to version server ', HOST, 'closed'
print 'Connecting to notification server (', notif_server_ip, notif_server_port, ')'
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((notif_server_ip, notif_server_port))
	print 'Connected successfully to notification server'
except:
	print 'Error connecting to notification server'
	
s.send('VER 4 MSNP8 CVR0\n')
read('Version: ')
s.send('CVR 5 0x0409 win 4.10 i386 MSNMSGR 6.2.0208 MSMSGS ' + EMAIL + '\n')
s.send('USR 6 TWN I ' + EMAIL + '\n')
read('Client Info: ')
challenge_string = read('Challenge String Info: ')[4]
print 'Challenge String: ' + challenge_string

page = urllib2.urlopen('https://nexus.passport.com/rdr/pprdr.asp')
info = str(page.info()).split(',')
login_server = ''

for arg in info:
	print arg
	if 'DALogin' in arg:
		# print 'Found login server!'
		login_server = 'https://' + arg[8:]
		
long_string = 'Passport1.4 OrgVerb=GET,OrgURL=http%3A%2F%2Fmessenger%2Emsn%2Ecom,sign-in=' + EMAIL.replace('@', '%40') + ',pwd=' + PASSWORD + ',' + challenge_string + '\n'
print long_string

page.close()

# Problems with authorization, can anybody fix?
# Possible reasons: bad syntax, bad challenge string, invalid headers, what else?
headers = {'Authorization':long_string}
request = urllib2.Request(login_server, None, headers)
page = urllib2.urlopen(login_server)
print page.read()
page.close()

print 'Client shutting down'
s.send('OUT')
s.close()
exit()