from char_to_unicode import readable_char_to_unicode
import string

eng_letters = string.ascii_letters

# transformations = {
# 	"ENG_a": ["a_re", "a_do", "a_mi"],
# 	"ENG_e": ["e_re", "e_do", "e_mi", "e_dot_do", "e_dot_re", "e_dot_mi"],
# 	"ENG_E": ["E_re", "E_do", "E_mi", "E_dot_do", "E_dot_re", "E_dot_mi"],
# 	"ENG_i": ["i_re", "i_do", "i_mi"],
# 	"ENG_I": ["I_re", "I_do", "I_mi"],
# 	"ENG_o": ["o_re", "o_do", "o_mi", "o_dot_do", "o_dot_re", "o_dot_mi"],
# 	"ENG_O": ["O_re", "O_do", "O_mi", "O_dot_do", "O_dot_re", "O_dot_mi"],
# 	"ENG_u": ["u_re", "u_do", "u_mi"],
# 	"ENG_U": ["U_re", "U_do", "U_mi"],
# 	"ENG_s": ["s", "s_dot"],
# 	"ENG_S": ["S", "S_dot"],

# 	"ENG_k": ["k"],
# }

"""Creates a dictionary from english chars to all possible
readable unicode chars"""
def all_accent_transformations():
	readablechars = readable_char_to_unicode.keys()
	transformations = {}
	for ch in eng_letters:
		transformations['ENG_' + ch] = filter(lambda key: key[0] == ch, readablechars)

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
