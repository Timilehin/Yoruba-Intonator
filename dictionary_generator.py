#!/usr/bin/python
# -*- coding: latin-1 -*-

def get_yoruba_dictionary():
	#load the words in the dictionary into a set 
	yoruba_words = set() 
	filename = "cleaned_yoruba_dict.txt"#replace with the name of your dictionary of yoruba words.
	file = open(filename, "r")
	for line in file:
  		yoruba_words.add(line.strip())
  	return yoruba_words