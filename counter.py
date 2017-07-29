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
		return self.num_increments <= self.max_increments

	def increment(self, ):
		assert self.can_increment()

		#increment case
		i=1

		while i < self.num_digits and self.can_increment():
			curr = int(self.value[-i])
			if curr < self.bases[-i]-1:
				curr += 1
				self.value[-i] = str(curr)
				print "1value is now" + str(self.value)
				return

			#Carry case
			self.value[-i] = "0"
			print "2value is now" + str(self.value)
			i+=1
			pos = i 
			while self.value[-pos] == self.bases[-pos] -1:
				pos += 1
			self.value[-pos] = str(int(self.value[-pos])+1)
			print "3value is now" + str(self.value)
			self.num_increments += 1
			return

	def get_curr_value(self, ):
		return str(self.value)

c = Counter(2, [1,2,])
print c.get_curr_value()
while c.can_increment():
	c.increment()
	print c.get_curr_value()