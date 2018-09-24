vowels = ['a', 'e', 'i', 'o', 'u']

def break_down(word):
	if len(word) == 0:
		return [word]
	if word[0] in vowels:
		if len(word)>1 and word[1] == 'n':
			return [word[:2]] + break_down(word[2:])
		return [word[0]] + break_down(word[1:])
	else:
		if len(word) > 2 and word[2] == 'n':
			#a-(hon)
			return [word[:3]] + break_down(word[3:])
		if word[0] == 'g' and len(word)>2 and word[1] == 'b':
			#su-(gbon)
			if len(word) > 3 and word[2] in vowels and word[3] == 'n':
				return [word[:4]] + break_down(word[4:])
			return [word[:3]] + break_down(word[3:])
		return [word[:2]] + break_down(word[2:])

def syllabify(word):
	if not word:
		return None
	elif word[0] in vowels:
		return [word[0]] + break_down(word[1:])
	return(break_down(word))