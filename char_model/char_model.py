import anago 

def intonate(sentence):
	model = anago.Sequence()
	model = model.load("char_model/best_model")
	resp = model.analyze(list(sentence))
	return marked_output(resp)

def marked_output(json_output):
	#takes in the json output from the character model 
	#and decodes it to return the marked text
	res = ""
	words = json_output['words']
	entities = {i['beginOffset']: int(i['type']) for i in json_output['entities']}
	for i in range(len(words)):
		res += decode(words[i], entities.get(i, 0))
	return res

def decode(letter, number):
    MI = u'\u0301'
    DO = u'\u0300'
    DOT = u'\u0323'
    
    if number == 0:
        return letter
    elif number == 1:
        return letter+DO
    elif number == 2:
        return letter + MI
    elif number == 3:
        return letter+DOT
    elif number == 4:
        return letter+DOT+DO
    elif number == 5:
        return letter+DOT+MI
