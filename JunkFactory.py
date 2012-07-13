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

# Constants
WAIT = 0.5
DEFAULT_NAME = 'Player X'

# Simple functions
# Will be put into another class soon
def ucwords(s):
	return string.capwords(s)
	
def randint(low, high):
	return random.randint(low, high)

def readln(s):
	# write(s)
	return raw_input(s)
		
def println(s):
	# write(s)
	print s
		
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
		println('Statistics for ' + self.name + ':')
		println('Level: ' + str(self.get_level()))
		println('Experience: ' + str(self.exp))
		println('Total Cash: ' + str(self.cash))
	
	# Sets a new name
	def new_name(self):
		self.name = ucwords(readln('Enter your name: ')).strip()
		
# The game class
class Main:
	def __init__(self):
		pass
	
	# Loads the pickle file
	def load(self, name):
		try:
			to_read = open('pickle.jff', 'r')
			player = pickle.load(to_read)
			println('Account found, data loaded!')
			to_read.close()
			return player
		except IOError:
			global DEFAULT_NAME
			return Player(DEFAULT_NAME)
		
	# The general game initiation process
	def start(self):
		global WAIT
		# Clears the screen
		if os.name == 'posix':
			os.system('clear')
		else:
			os.system('cls')
		println('')
		println('--------------------------------')
		println('Welcome to the Junk Factory RPG!')
		println('Created by Whac and Swmaster001!')
		println('--------------------------------')
		println('')
		time.sleep(WAIT)
		
# The actual game processing
desired_name = ''
m = Main()
m.start()
p = Player(DEFAULT_NAME)
p.new_name()
desired_name = p.name
println('Thanks for entering your name, ' + p.name + '!\n')

# Save data loading here
p = m.load(p.name)
p.name = desired_name
time.sleep(WAIT)

# Processing command input
println('Processing command input:\n')

while True:
	command = readln('>>> ').lower()
	if command == 'stats':
		p.stats()
	if command == 'train':
		amount = randint((p.exp/8), (p.exp/4))
		p.exp += amount
		println('You have trained and have gained ' + str(amount) + ' exp.')
	if command == 'work':
		amount = randint((p.exp/512), (p.exp/64))
		p.cash += amount
		println('You have worked and have gained ' + str(amount) + ' cash.')
	if command == 'quit' or command == 'exit':
		println('Cya later!\n')
		exit()
	# Player save data writing
	# Called after every command, shouldn't cause too much lag
	to_write = open('pickle.jff', 'w')
	pickle.dump(p, to_write)
	to_write.flush()
	to_write.close()

# End of script