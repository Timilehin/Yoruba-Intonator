from __future__ import division 
import intonator
import collections
from operator import attrgetter
import contextual_bigram_generator
import unicodedata


"""
load in the probability disctiobutions into a discionary.
pass in a list of lists for each word from the intonator. 
Then make the mapping from word to (word, score, ()) and (word, 1, (prev_word1,prev_word2,..)) fro the base ones in particular 

You keep going higher on the array levels. For each new level, for each item in the array, we check the immediate past and for each item there we want to find the product of their score and the probability of the pair of them followed by me. Then we will choose the maximum of these and makeit our value. 
"""

def get_bigram_probabilities():
	probability_pairs = {}
	filename = "data/bigram_probabilities.txt"
	file = open(filename, "r")
	for line in file:
		line = line.split(",")
		line = map(lambda x: x.strip(), line)
		#print line
		if len(line) != 3:
			continue
		left = unicodedata.normalize('NFD', line[0].decode("utf-8"))
		right = curr = unicodedata.normalize('NFD', line[1].decode("utf-8"))
		probability_pairs[(left, right)] = line[2]
	print probability_pairs.items()[0]
	return probability_pairs

bigram_probabilities = get_bigram_probabilities()
contextual_bigram_freqs = contextual_bigram_generator.get_contextual_bigram_frequencies()

def get_most_likely_sentence_markings(sentence):
	sentence = str(sentence)
	sentence = sentence.split()
	sentence = map(lambda x : x.lower().translate(None, '.,:;-()\'\"\"'), sentence)
	all_word_possibliities = map(lambda x: intonator.get_verified_possibilities(x), sentence)
	# print"===="
	# print all_word_possibliities

	Node = collections.namedtuple("Node", "word, score, so_far")
	for i in range(len(all_word_possibliities)):
		init_val = 1 if i == 0 else 0
		all_word_possibliities[i] = map(lambda x : Node(x, init_val, [x]), all_word_possibliities[i])
		
	
	for layer in range(1, len(all_word_possibliities)):
		for curr_node_pos in range(len(all_word_possibliities[layer])):
			max_val = float('-inf')
			max_node = None
			curr_node=all_word_possibliities[layer][curr_node_pos]
			#curr_node.word=all_word_possibliities[layer][curr_node_pos].word.encode("utf-8")
			for prev_node_pos in range(len(all_word_possibliities[layer-1])):
				#compute the max productof all the combinations of the lower to the higher? 
				prev_node=all_word_possibliities[layer-1][prev_node_pos]
				# print(type(curr_node.word))
				a=unicodedata.normalize('NFD', prev_node.word)
				b=unicodedata.normalize('NFD', curr_node.word)
				bigram_prob = float(bigram_probabilities[(a, b)])\
					if (a, b) in bigram_probabilities else 0
				#print bigram_prob,"is the probability of ",prev_node.word,curr_node.word
				score = prev_node.score * bigram_prob
				#print score
				#print bigram_prob
				contextual_bigram_score = 0.0001
				for word in prev_node.so_far:
					words = [unicodedata.normalize('NFD', word), b]
					words.sort()
					contextual_bigram_score += int(contextual_bigram_freqs[tuple(words)])/200

				score = (0.75)*score + (0.25)*contextual_bigram_score

				if score > max_val or not max_node:
					max_val = score
					max_node = prev_node
			all_word_possibliities[layer][curr_node_pos] = Node(curr_node.word, max_val, max_node.so_far + [curr_node.word])

	#print all_word_possibliities
	final_layer = all_word_possibliities[-1]
	final_layer = [node for node in final_layer if node.score != 0]
	if final_layer:
		#print "I get here"
		#print "The most likely intended intonation(s) in descending order are:"
		final_layer = sorted(final_layer, key=attrgetter('score'), reverse=True)
		return " ".join(final_layer[0].so_far)
		#for prediction in final_layer:
		#	print prediction.score, " ".join(prediction.so_far)
	else:
		return None#" ".join(sentence)

	#print "There are {0} verified possibilities".format(len(verified_words))
	#for word in verified_words:
	#	print word

def repl():
	while 1:
		sentence = raw_input("type in the sentence you want to intonate\nsentence: ")
		print(get_most_likely_sentence_markings(sentence))	