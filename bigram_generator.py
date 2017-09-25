"""load ngram data into counter. 
check:
1. the number of times tthat word has been seen 
2. the number of times it has been inthesame context as the other one."""

#also make a bigram model

import collections
import intonator


def get_semantic_bigram_frequencies():
	file = open("data/contextual_bigram_data.txt","r")
	freq_counter = collections.Counter()

	for line in file:
		w1, w2, freq = line.split(",")
		freq_counter[(w1.strip(), w2.strip())] = freq
	file.close()
	return freq_counter

def get_bigram_frequencies():
	file = open("data/bigram_data.txt","r")
	freq_counter = collections.Counter()

	for line in file:
		w1, w2, freq = line.split(",")
		freq_counter[(w1.strip(), w2.strip())] = freq
	file.close()
	return freq_counter

	

"""bigram_frequencies = get_bigram_frequencies()
bigram_frequency_items = bigram_frequencies.items()

print("welcome to the semantic bigram. \
	Give me two words and I'll tell you howmany times they appeared in the same context in our corpus.")
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