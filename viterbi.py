from __future__ import division 
import intonator
import collections

"""
load in the probability disctiobutions into a discionary.
pass in a list of lists for each word from the intonator. 
Then make the mapping from word to (word, score, ()) and (word, 1, (prev_word1,prev_word2,..)) fro the base ones in particular 

You keep going higher on the array levels. For each new level, for each item in the array, we check the immediate past and for each item there we want to find the product of their score and the probability of the pair of them followed by me. Then we will choose the maximum of these and makeit our value. 
"""

def get_probability_distributions():
	probability_pairs = {}
	filename = "bigram_probabilities.txt"
	file = open(filename, "r")
	for line in file:
		line = line.split(",")
		line = map(lambda x: x.strip(), line)
		#print line
		if len(line) != 3:
			continue
		probability_pairs[(line[0], line[1])] = line[2]
	return probability_pairs

bigram_probabilities = get_probability_distributions()

while 1:
	sentence = raw_input("type in the sentence you want to intonate\nsentence: ")
	sentence = sentence.split()
	all_word_possibliities = map(lambda x: intonator.get_verified_possibilities(x), sentence)

	Node = collections.namedtuple("Node", "word, score, so_far")
	for i in range(len(all_word_possibliities)):
		init_val = 1 if i == 0 else 0
		all_word_possibliities[i] = map(lambda x : Node(x, init_val, [x]), all_word_possibliities[i])
		


	#print all_word_possibliities
	
	for layer in range(1, len(all_word_possibliities)):
		for curr_node_pos in range(len(all_word_possibliities[layer])):
			max_val = float('-inf')
			max_node = None
			curr_node=all_word_possibliities[layer][curr_node_pos]
			for prev_node_pos in range(len(all_word_possibliities[layer-1])):
				#compute the max productof all the combinations of the lower to the higher? 
				prev_node=all_word_possibliities[layer-1][prev_node_pos]
				bigram_prob = float(bigram_probabilities[(prev_node.word, curr_node.word)]) if (prev_node.word, curr_node.word) in bigram_probabilities else 0
				print bigram_prob,"is the probability of ",prev_node.word,curr_node.word
				score = prev_node.score * bigram_prob
				if score > max_val or not  max_node:
					max_val = score
					max_node = prev_node
			print "!!"
			print curr_node
			print max_node
			print max_val
			print "!!"
			all_word_possibliities[layer][curr_node_pos] = Node(curr_node.word, max_val, max_node.so_far + [curr_node.word])

	final_layer = all_word_possibliities[-1]
	final_layer = [node for node in final_layer if node.score != 0]
	print "The most likely intended intonations and their probabilities are: \n"
	if final_layer:
		for prediction in final_layer:
			print prediction.score, " ".join(prediction.so_far)
	else:
		print "Sorry, I don't have any predictions. My model is still improving I'll soon be able to give a better answer"

	#print "There are {0} verified possibilities".format(len(verified_words))
	#for word in verified_words:
	#	print word
	