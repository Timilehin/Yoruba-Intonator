#!/usr/bin/python
# -*- coding: latin-1 -*-

import unicodedata

def get_yoruba_dictionary():
	#load the words in the dictionary into a set 
	yoruba_words = set() 
	filename = "data/dictionary.txt"#replace with the name of your dictionary of yoruba words.
	file = open(filename, "r")
	for line in file:
		#print line
		item = unicodedata.normalize('NFD', line.strip().decode("utf-8")) 
  		yoruba_words.add(item)
  	return yoruba_words

"""fh = open("unique_dict.txt", "w")

words = get_yoruba_dictionary()
for word in words:
  	fh.write("{}\n".format(word))

fh.close()"""