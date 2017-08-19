#!/usr/bin/python
# -*- coding: latin-1 -*-

import string 
import utils

#TODO(timifasubaa):refactor this fn out! nowin utils.py
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
			#print letter
			result += letter.lower()
	return result


filename = "yoruba_dictionary.txt"
file = open(filename, "r")
bad_chars = ["<", "?", ".", ",", "(", ")", ":", ";", "-", "\"", "'", "+", "\
̣", "!", "“", "`","c"] + list(string.digits)

fh = open("cleaned_yoruba_dict.txt","w")

for line in file:
	
	if not any([bad_char in line for bad_char in bad_chars]):
  		fh.write(lower_case(line.strip()))
  		fh.write("\n")

fh.close()