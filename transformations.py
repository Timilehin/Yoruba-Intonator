from char_to_unicode import readable_char_to_unicode
import string

eng_letters = string.ascii_letters


"""Creates a dictionary from english chars to all possible
readable unicode chars"""
def all_accent_transformations():
	readablechars = readable_char_to_unicode.keys()
	transformations = {}
	for ch in eng_letters:
		valid_keys = filter(lambda key: key[0] == ch, readablechars)
		letter_mappings = map(lambda x : readable_char_to_unicode[x], valid_keys)
		transformations['ENG_' + ch] = letter_mappings

	return transformations

eng_to_readable_chars = all_accent_transformations()
# accent_transformations = transformations

"""Takes an english word and generates all possible 
unicode_char variations. Note that the number of possibilities grows
exponentially with the length of the word."""
def all_variants(word):
	
	def add_all_suffixes(word, variants):
		if len(word) == 0:
			return variants

		new_variants = []
		eng_ch = word[-1]
		for variant in variants: 
			suffix_list = [ch + '/' + variant for ch in eng_to_readable_chars['ENG_' + eng_ch]]
			new_variants += suffix_list
	    
		return add_all_suffixes(word[:-1], new_variants)

	return add_all_suffixes(word, [""])

"""Creates a dictionary of word -> possible_variations(word) for each word in a list"""
def all_wordset_variants(words):
	return dict([(word, all_variants(word)) for word in words])

if __name__ == "__main__":
	print(all_variants('hello'))
	print(all_wordset_variants(['hello', 'world']))
