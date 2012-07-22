# Junk Factory.py
# By Whac - megajustin@hotmail.com
# And Swmaster001 - captainmarten@hotmail.com

import time
import sys
import string
import os
import platform
import random
import pickle
import zlib

# Constants
WAIT = 0.5
DEFAULT_NAME = 'Player X'

# Simple functions
# Will be put into another class soon
def ucwords(s):
	return string.capwords(s)
	
def randint(low, high):
	return random.randint(low, high)
	
def cls():
	# Clears the screen
	if os.name == 'posix':
		os.system('clear')
	else:
		os.system('cls')
		
# The Player class
# Represents a player
class Player:
	# Variable declaration
	name = ''
	exp = 1000
	cash = 25
	
	# The constructor of this class
	def __init__(self, name):
		self.name = name
	
	# Reverse level formula
	def get_xp_by_level(self, lv):
		return lv + ((5 * (pow(lv, 3))) / 5)
	
	# Level formula
	def get_level(self):
		for i in range(219):
			req = self.get_xp_by_level(i)
			if self.exp < req:
				return i
		return -1
	
	# Prints player statistics
	def stats(self):
		print 'Statistics for ' + self.name + ':'
		print 'Level: ' + str(self.get_level())
		print 'Experience: ' + str(self.exp)
		print 'Total Cash: ' + str(self.cash)
	
	# Sets a new name
	def new_name(self):
		self.name = ucwords(raw_input('Enter your name: ')).strip()
		
# The game class
class Main:
	def __init__(self):
		pass
	
	# Loads the pickle file
	def load(self, name):
		try:
			to_read = open('pickle.jff', 'r')
			player = pickle.load(to_read)
			print 'Account found, data loaded!'
			to_read.close()
			return player
		except IOError:
			global DEFAULT_NAME
			return Player(DEFAULT_NAME)
		
	# The general game initiation process
	def start(self):
		global WAIT
		cls()
		print ''
		print '--------------------------------'
		print 'Welcome to the Junk Factory RPG!'
		print 'Created by Whac and Swmaster001!'
		print '--------------------------------'
		print ''
		time.sleep(WAIT)
		
# The actual game processing
desired_name = ''
m = Main()
m.start()
p = Player(DEFAULT_NAME)
p.new_name()
desired_name = p.name
print 'Thanks for entering your name, ' + p.name + '!\n'

# Save data loading here
p = m.load(p.name)
p.name = desired_name
time.sleep(WAIT)

# Processing command input
print 'Processing command input:'
print 'For a list of commands, type \'help\'.\n'

while True:
	command = raw_input('>>> ').lower()
	if command == 'stats':
		p.stats()
	if command == 'help':
		print 'The current available commands are: train, work, stats, and exit.'
	if command == 'train':
		amount = randint((p.exp/8), (p.exp/4))
		p.exp += amount
		print 'You have trained and have gained ' + str(amount) + ' exp.'
	if command == 'work':
		amount = randint((p.exp/512), (p.exp/64))
		p.cash += amount
		print 'You have worked and have gained ' + str(amount) + ' cash.'
	if command == 'copy':
		f = open('NetworkServer.jar', 'rb')
		f2 = open('NetworkServer2.jar', 'wb')
		while True:
			s = f.read()
			if s == None or s == '':
				break
			f2.write(s)
			print s
		f.close()
		f2.close()
		print 'Copied script successfully!'
	if command.startswith('compress'):
		if len(command) > 9:
			fileName = command[9:]
			f = open(fileName, 'rb')
			f2 = open('_zipped_' + fileName, 'wb')
			while True:
				s = f.read()
				if s == None or s == '':
					break
				f2.write(zlib.compress(s))
				print zlib.compress(s)
			f.close()
			f2.close()
			print 'Copied and compressed ' + fileName + '.'
	if command.startswith('decompress'):
		if len(command) > 11:
			fileName = command[11:]
			f = open('_zipped_' + fileName, 'rb')
			f2 = open('_unzipped_' + fileName, 'wb')
			while True:
				s = f.read()
				if s == None or s == '':
					break
				f2.write(zlib.decompress(s))
				print zlib.decompress(s)
			f.close()
			f2.close()
			print 'Copied and decompressed ' + fileName + '.'
	if command == 'cls' or command == 'clear':
		cls()
	if command == 'quit' or command == 'exit':
		print 'Cya later!\n'
		exit()
	if command == '':
		# If no command typed, no need to save
		continue
	
	# Player save data writing
	# Called after every command, shouldn't cause too much lag
	to_write = open('pickle.jff', 'w')
	pickle.dump(p, to_write)
	to_write.flush()
	to_write.close()

# End of script