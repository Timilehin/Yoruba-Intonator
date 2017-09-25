"""load ngram data into counter. 
check:
1. the number of times tthat word has been seen 
2. the number of times it has been inthesame context as the other one."""
from __future__ import division
import collections
import intonator

def get_bigram_distribution():
	#Takes in bigrams of the form a,b,2 ... a,c,3 and returns counts of the form {'a':[('b', 2), ('c', 3)]}
	word_mappings = {}

	file = open("data/bigram_data.txt","r")
	for line in file:
		w1, w2, freq = line.split(",")
		if w1 not in word_mappings:
			word_mappings[w1] = []
		word_mappings[w1].append((w2, freq))
	return word_mappings


def get_probability_distribution(word, nexts_and_counts):
	#takes in a word, 'a' and n_and_c like [('b', 2), ('c', 3)] and returns probabilities of the form 
	#{(a,b):2/5, (a, c):3/5}
	total = 0
	result = {}
	#print nexts_and_counts
	for w2, count in nexts_and_counts:
		#print count,"---"
		count = int(count.strip())
		total += count
		result[(word, w2)] = count

	for w2, count in nexts_and_counts:
		count = int(count.strip())
		result[(word, w2)] /= total
	#get all the words now and make their p
	return result


bigram_prob_file = open("data/bigram_probabilities.txt","w")

bigram_distribution = get_bigram_distribution()
for distribution in bigram_distribution.items():
	pair_probabilities = get_probability_distribution(distribution[0], distribution[1])
	for pair, probability in pair_probabilities.items():
		#print pair
		#print probability
		bigram_prob_file.write(pair[0]+","+pair[1]+","+str(probability)+"\n")

bigram_prob_file.close()

#write a function that takes in word, [follower, count] and returns 

""" only uncomment this if you want to use bigram_probabilities from the command line. 
TODO(timifasubaa):refactor to make user able to select what service to use from cmdline flag
while 1:
	word1 = raw_input("type in the first word of the pair\nword1: ")
	word2 = raw_input("Now the second\nword2: ")
	word1_possibilities = intonator.get_verified_possibilities(word1)
	word2_possibilities = intonator.get_verified_possibilities(word2)
	for w1 in word1_possibilities:
		for w2 in word2_possibilities:
			words = [w1, w2]
			words.sort()
			print w1 +" and " + w2 + " occur together " + str(bigram_frequencies[tuple(words)]) + " times"
	#get all possibilities and generate all pairs
	"""