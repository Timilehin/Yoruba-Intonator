"""read from commandline for the word you want to get the mostlikely sentence. 
Then you transform it into the mapping? 
Cool 
"""
import transformations

word = raw_input("type in the sentence you want to intonate\nword: ")

eng_to_readablechars = transformations.all_accent_transformations()

letters = list(word)
letters_in_TCHSET = map(lambda x : "ENG_"+ x, letters)
possibilities_in_TCHSET = map(lambda x: eng_to_readablechars[x], letters_in_TCHSET)
print possibilities_in_TCHSET

#print letters_in_TCHSET