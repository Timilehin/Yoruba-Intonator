class Counter: 
	#A counter where each digit posistion has a separate BASE
	def __init__(self, num_digits, bases):
		if num_digits != len(bases):
			raise Exception

		self.value = "0"*num_digits
		self.num_increments = 0
		self.max_increments = reduce(lambda x, y: x*y, bases) - 1
		self.bases = bases
		self.num_digits = num_digits

	def can_increment(self):
		return self.num_increments <= self.max_increments

	def increment(self):
		assert can_increment()

		for i in range(1, self.num_digits+1):
			curr = int(value[-i])
			if curr < self.bases[i]:
				curr += 1
				self.value = str(curr)
				return 

#			IF NOT THEN YOUBASICALLU SKIP THIS AND GO STRAIGHT TO THE PART WHERRE RHYCHOOSE AND PAY
		 	self.value = str(curr)

		self.num_increments += 1

	def get_curr_value(self):
		return self.value

c = Counter(1, [2,])
c.get_curr_value()
