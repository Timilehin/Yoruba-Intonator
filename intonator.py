"""read from commandline for the word you want to get the mostlikely sentence. 
Then you transform it into the mapping? 
Cool 
"""
import counter
import dictionary_generator
import transformations
import unicodedata
import utils

def get_word_generator(possibilities_per_position):
	def word_generator(number):
		position_and_selection = enumerate(number)
		final_word = map(lambda x: possibilities_per_position[x[0]][int(x[1])], position_and_selection)
		return final_word
	return word_generator

def get_all_possibilities(word):
	print(word)
	letters = list(word)
	letters_in_TCHSET = map(lambda x : "ENG_"+ x, letters)
	possibilities_in_TCHSET = map(lambda x: eng_to_readablechars[x] if eng_to_readablechars[x] else x, letters_in_TCHSET)
	possibilities_per_slot = map(lambda x: len(x) if x else 1, possibilities_in_TCHSET)
	if possibilities_per_slot == 0:
		return [word]
	possibility_counter = counter.Counter(len(word), possibilities_per_slot)
	generate_word = get_word_generator(possibilities_in_TCHSET)
	all_possibilities = []
	selection_number = possibility_counter.get_curr_value()
	all_possibilities.append(generate_word(selection_number))

	while possibility_counter.can_increment():
		possibility_counter.increment()
		selection_number = possibility_counter.get_curr_value()
		all_possibilities.append(generate_word(selection_number))

	all_possibilities = map(lambda x : "".join(x), all_possibilities)
	return all_possibilities

	
yoruba_dictionary = utils.get_yoruba_dictionary()
eng_to_readablechars = transformations.all_accent_transformations()

def get_verified_possibilities(word):
	all_possibilities = get_all_possibilities(word)
	res = []
	for i in all_possibilities:
		curr = unicodedata.normalize('NFD', i.decode("utf-8"))
		if curr in yoruba_dictionary:
			#res.append(curr)
			curr = unicodedata.normalize('NFC', curr)
			res.append(curr)
		#else: 
		#	print "[unable find word in dict]={}=".format(curr.encode("utf-8"))
	if not res:
		res = [word.decode("utf-8")]
	#[i.decode("utf-8") for i in all_possibilities if i.decode("utf-8") in yoruba_dictionary]
	#filter(lambda x : x in yoruba_dictionary, all_possibilities)
	return res



"""while 1:
	word = raw_input("type in the sentence you want to intonate\nword: ")
	verified_words = get_verified_possibilities(word)
	print "There are {0} verified possibilities".format(len(verified_words))
	for word in verified_words:
		print word
		"""