"""read from commandline for the word you want to get the mostlikely sentence. 
Then you transform it into the mapping? 
Cool 
"""
import counter
import transformations
import dictionary_generator

word = raw_input("type in the sentence you want to intonate\nword: ")

eng_to_readablechars = transformations.all_accent_transformations()

letters = list(word)
letters_in_TCHSET = map(lambda x : "ENG_"+ x, letters)
possibilities_in_TCHSET = map(lambda x: eng_to_readablechars[x], letters_in_TCHSET)
possibilities_per_slot = map(lambda x: len(x), possibilities_in_TCHSET)
possibility_counter = counter.Counter(len(word), possibilities_per_slot)

def get_word_generator(possibilities_per_position):
	def word_generator(number):
		position_and_selection = enumerate(number)
		final_word = map(lambda x: possibilities_per_position[x[0]][int(x[1])], position_and_selection)
		return final_word
	return word_generator

generate_word = get_word_generator(possibilities_in_TCHSET)
all_possibilities = []
selection_number = possibility_counter.get_curr_value()
all_possibilities.append(generate_word(selection_number))

while possibility_counter.can_increment():
	possibility_counter.increment()
	selection_number = possibility_counter.get_curr_value()
	all_possibilities.append(generate_word(selection_number))

yoruba_dictionary = dictionary_generator.get_yoruba_dictionary()
#print all_possibilities
all_possibilities = map(lambda x : "".join(x), all_possibilities)
verified_words = filter(lambda x : x in yoruba_dictionary, all_possibilities)
print "There are {0} verified possibilities".format(len(verified_words))
for word in verified_words:
	print word
