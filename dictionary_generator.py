#!/usr/bin/python
# -*- coding: latin-1 -*-

def lower_case(word):
	"""this function takes in a marked yoruba word and returns the lower case version"""
	result = ""
	marked_capital_letters = {"À":"à", 
							  "Á":"á", 
							  "É":"é", 
							  "È":"è",
							  "Ẹ":"ẹ", 
							  "Ì":"ì",
							  "Í":"í",
							  "Ó":"ó", 
							  "Ò":"ò", 
							  "Ṣ":"ṣ", 
							  "Ọ":"ọ",
							  "Ú":"ú",
							  "Ù":"ù"
							 }
	for letter in word:
		if letter in marked_capital_letters.keys():
			result += marked_capital_letters[letter]
		else:
			result += letter.lower()
	return result

#load the words in the dictionary into a set 

def get_yoruba_dictionary():
	yoruba_words = set() 

	filename = "cleaned_yoruba_dict.txt"
	file = open(filename, "r")
	for line in file:
  		yoruba_words.add(lower_case(line.strip()))
  	return yoruba_words