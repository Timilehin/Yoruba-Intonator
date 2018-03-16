import collections
import utils
import nltk


def generate_bigram(filename, contextual_bigram=True):
	# given a tokenized file, generate bigram and contextual bigram data 
	#filename = "tokenized_sentences.txt"
	#filename = "newbi.txt"
	file = open(filename, "r")


	semantic_bigram_freq = collections.Counter()
	bigram_freq = collections.Counter()

	for f_line in file:
		line = f_line.split()
		bigrams = nltk.ngrams(line, 2)
		for gram in bigrams:
			bigram_freq[gram] += 1

		#semantic_bigram
		if contextual_bigram:
			all_pairs = utils.get_all_pairs(line)
			for pair in all_pairs:
				pair.sort()
				semantic_bigram_freq[tuple(pair)] += 1

	if contextual_bigram:
		fh = open("contextual_bigram_data.txt","w")

		for words, freq in semantic_bigram_freq.items():
		  	fh.write("{},{},{}\n".format(words[0], words[1], freq))

		fh.close()


	bigram_file = open("bigram_data.txt","w")

	for words, freq in bigram_freq.items():
	  	bigram_file.write("{},{},{}\n".format(words[0], words[1], freq))

	bigram_file.close()

	#make a utils.py to have these things you reuse.

	#have a list of word pairs containing the two words. THey should be interchangeable. 
	#Also see if you can implement the gaussian approach to share the weight in the sentence pretty equally. 