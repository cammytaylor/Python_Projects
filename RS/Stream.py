# Stream.py
# Converted to Python
# Credits Whackatre and Scape-JAVA

class Stream:

	currentOffset = 0
	buffer = []
	
	def __init__(self):
		currentOffset = 0
		buffer = []
	
	def toByte(self, val):
		return (((val + 128) % 256) - 128)
	
	def readUnsignedWord(self):
		self.currentOffset += 2
		return (((self.buffer[self.currentOffset - 2] & 0xff) << 8) + self.buffer[self.currentOffset - 1] & 0xff)
	
	def writeWord(self, i):
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(i >> 8)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(i)
	
	def writeByte(self, i):
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(i)
	
	def writeQWord(self, l):
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 56)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 48)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 40)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 32)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 24)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 16)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l >> 8)
		self.currentOffset += 1
		self.buffer[self.currentOffset] = self.toByte(l)
	
	def writeString(self, s):
		max = self.currentOffset + len(s)
		for i in range(self.currentOffset, max):
			self.buffer[self.currentOffset + i] = s[i]
			self.currentOffset += len(s)
			self.currentOffset += 1
			self.buffer[self.currentOffset] = 10
	
	def readUnsignedByte(self):
		self.currentOffset += 1
		return self.buffer[self.currentOffset] & 0xff
	
	def readSignedByte(self):
		self.currentOffset += 1
		return self.buffer[self.currentOffset]
	
	def readSignedWord(self):
		self.currentOffset += 2
		i = ((self.buffer[self.currentOffset - 2] & 0xff) << 8) + (self.buffer[self.currentOffset - 1] & 0xff)
		if i > 32767:
			i -= 0x10000
		return i
	
	# Seems to me like the bit shift numbers get tripled i.e offset - 3 << 16       
	def readDWord(self):
		self.currentOffset += 4
		return ((self.buffer[self.currentOffset - 4] & 0xff) << 24) + (self.buffer[self.currentOffset - 3] & 0xff << 16) + (self.buffer[self.currentOffset - 2] & 0xff) << 8 (self.buffer[self.currentOffset - 1] & 0xff)
	
	# Fixed, drunk?
	def readQWord(self):
		l = self.toLong(self.readDWord() & 0xffffffff)
		l1 = self.toLong(self.readDWord() & 0xffffffff)
		return (l << 32) + l1
	
	def toLong(self, val):
		return ((val + 1) / 2)
	
	def readString(self):
		s = ''
		i = self.currentOffset
		while self.buffer[self.currentOffset] != 10:
			for i in range(self.currentOffset, (self.currentOffset - i - 1)):
				s += self.buffer[i]
		return s
			
	# The fuck..
	def readBytes(self, abyte0, i, j):
		for k in range(j, (j+1)):
			abyte0[k] = self.buffer[self.currentOffset]

# End

s = Stream()
s.writeByte(3)