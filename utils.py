#!/usr/bin/python
# -*- coding: latin-1 -*-
import collections
import os
import urllib2
from itertools import chain

flatten = lambda lst: list(chain.from_iterable(lst))
setify = lambda row: set(list(row))

def load_or_run(runner, loader, *fpaths):
	if all(os.path.exists(fpath) for fpath in fpaths):
		if len(fpaths) > 1:
			return tuple(loader(fpath) for fpath in fpaths) 
		return loader(fpaths[0])
	else:
		return runner(*fpaths)


def download_file_unicode(path):
	resp = urllib2.urlopen(path)
	encoding = resp.headers.getparam('charset')
	return unicode(resp.read(), encoding)

def lower_case(word):
	"""this function takes in a marked yoruba word and returns the lower case version"""
	result = ""
	marked_capital_letters = {
							  "À":"à", "Á":"á", "É":"é", "È":"è","Ẹ":"ẹ", 
							  "Ì":"ì", "Í":"í", "Ó":"ó", "Ò":"ò", "Ṣ":"ṣ", 
							  "Ọ":"ọ", "Ú":"ú", "Ù":"ù"
							 }
	for letter in word:
		if letter in marked_capital_letters.keys():
			result += marked_capital_letters[letter]
		else:
			#print letter
			result += letter.lower()
	return result

def sentencifier(input_filepath, output_filepath):
	#takes a file and makes a new file with just one sentence per line
	with open(input_filepath, "r") as f:
		sents = nltk.tokenize.sent_tokenize(f.read())
		with open (output_filepath, "w+") as o:
			for line in sents:
				o.writeline(line)

def get_all_pairs(words): 
	#TODO(timifasubaa):rename to get_semantic_bigram_pairs
	#given a sentence, return all the pairs of words in the sentence
	result = []
	def all_pairs_helper(left_word, remaining_words):
		for right_word in remaining_words: 
			result.append([left_word, right_word])
	for i in range(len(words)):
		all_pairs_helper(words[i],words[i+1:])
	return result

assert get_all_pairs(["a", "b", "c"]) == [['a', 'b'], ['a', 'c'], ['b', 'c']]

def line_cleaner(line):
	#This function removes unnecessary embellishments so out bigram model is more effective.
	result = []
	bad_chars = [".", ",", ":"]
	for word in line:
		word = lower_case(word.translate(None, '.,:;-()\'\"\"'))
		result.append(word)
	return result


def get_bigram_pairs(sentence):
	#returns a counter containing bigram frequencies.
	bigram = collections.Counter()
	for i in range(len(sentence)-1):
		bigram[(sentence[i], sentence[i+1])] += 1
	return bigram

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