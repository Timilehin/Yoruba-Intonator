import collections
import utils

def get_all_pairs(words): 
	#given a sentence, return all the pairs of words in the sentence
	result = []
	def all_pairs_helper(left_word, remaining_words):
		for right_word in remaining_words: 
			result.append([left_word, right_word])
	for i in range(len(words)):
		all_pairs_helper(words[i],words[i+1:])
	return result

assert get_all_pairs(["a", "b", "c"]) == [['a', 'b'], ['a', 'c'], ['b', 'c']]

def line_cleaner(line):
	#This function removes unnecessary embellishments so out bigram model is more effective.
	result = []
	bad_chars = [".", ",", ":"]
	for word in line:
		word = utils.lower_case(word.translate(None, '.,:;-()\'\"\"'))
		result.append(word)
	return result


filename = "yoruba_sentences.txt"
file = open(filename, "r")


semantic_bigram_freq = collections.Counter()
bigram_freq = collections.Counter()

for f_line in file:
	line = f_line.split()
	clean_line = line_cleaner(line)

	#bigram
	if len(clean_line) > 1:
		for i in range(len(clean_line)-1):
			bigram_freq[(clean_line[i], clean_line[i+1])] += 1

	#semantic_bigram
	all_pairs = get_all_pairs(clean_line)
	for pair in all_pairs:
		pair.sort()
		semantic_bigram_freq[tuple(pair)] += 1


#write to file
#for words, freq in semantic_bigram_freq.items():
#	if freq > 100:
#		print words[0]
#		print words[1]
#		print freq
#		print "~~~"



fh = open("contextual_bigram_data.txt","w")

for words, freq in semantic_bigram_freq.items():
  	fh.write(words[0]+", "+words[1]+", "+str(freq))
  	fh.write("\n")

fh.close()


bigram_file = open("bigram_data.txt","w")

for words, freq in semantic_bigram_freq.items():
  	bigram_file.write(words[0]+", "+words[1]+", "+str(freq))
  	bigram_file.write("\n")

bigram_file.close()



#have a list of word pairs containing the two words. THey should be interchangeable. 
#Also see if you can implement the gaussian approach to share the weight in the sentence pretty equally. 