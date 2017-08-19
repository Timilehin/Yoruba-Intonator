#!/usr/bin/python
# -*- coding: latin-1 -*-

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