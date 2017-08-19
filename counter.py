class Counter: 
	#A counter where each digit posistion has a separate BASE
	def __init__(self, num_digits, bases):
		if num_digits != len(bases):
			raise Exception
		if 0 in bases:
			print "Zero is not acceptable as a base here"
			raise Exception

		self.value = ["0"]*num_digits
		self.num_increments = 0
		self.max_increments = reduce(lambda x, y: x*y, bases) - 1
		self.bases = bases
		self.num_digits = num_digits

	def can_increment(self, ):
		return self.num_increments < self.max_increments

	def increment(self, ):
		assert self.can_increment()
		#increment case
		#print self.bases
		curr = int(self.value[-1])
		if curr < self.bases[-1]-1:
			curr += 1
			self.value[-1] = str(curr)
			#print "1*value is now" + str(self.value)
			self.num_increments += 1
			return

		#Carry case
		self.value[-1] = "0"
		#print "2value is now" + str(self.value)
		pos = 2
		#print "val="+str(int(self.value[-pos]))
		#print "base="+str(int(self.bases[-pos]) -1)
		while int(self.value[-pos]) == int(self.bases[-pos]) -1:
			self.value[-pos] = "0"
			pos += 1
			#print "3value is now" + str(self.value)
		self.value[-pos] = str(int(self.value[-pos])+1)
		#print "4*value is now" + str(self.value)
		self.num_increments += 1
		return

	def get_curr_value(self, ):
		return "".join(self.value)