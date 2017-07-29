"""read from commandline for the word you want to get the mostlikely sentence. 
Then you transform it into the mapping? 
Cool 
"""
import transformations

word = raw_input("type in the semtence you want to intonate\nword: ")

letters = list(word)
letters_in_TCHSET = map(lambda x : "ENG_"+ x, letters)
possibilities_in_TCHSET = map(lambda x: transformations.transformations[x], letters_in_TCHSET)
print possibilities_in_TCHSET

#print letters_in_TCHSET