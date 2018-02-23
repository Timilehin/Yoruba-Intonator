from flask import Flask, render_template 
from flask_wtf import FlaskForm 
from wtforms import StringField, RadioField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

#from char_model.char_model import intonate
from char_model.char_model import intonate

from flask_bootstrap import Bootstrap
import viterbi

app = Flask(__name__)
app.config['SECRET_KEY']= 'THIS IS A SECRET!'
bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
	model = RadioField('What model to use?', coerce=str, choices=[('word','word based model'),('char','char based model')])
	unmarked_yoruba = StringField('Unmarked Yoruba: ', validators=[InputRequired()],  widget=TextArea())



@app.route('/', methods=['GET', 'POST'])
def form():
	form = LoginForm()
	if form.validate_on_submit():
		if form.model.data == 'char':
			translated_sentence = intonate(form.unmarked_yoruba.data)
		if form.model.data == 'word':
			translated_sentence = viterbi.get_most_likely_sentence_markings(form.unmarked_yoruba.data)

		unable_to_translate = form.unmarked_yoruba.data == translated_sentence
		if unable_to_translate:
			import os
			filename = 'untranslatable.txt'

			if os.path.exists(filename):
			    append_write = 'a' # append if already exists
			else:
			    append_write = 'w' # make a new file if not

			untranslated_sentences = open(filename,append_write)
			untranslated_sentences.write(translated_sentence + '\n')
			untranslated_sentences.close()

		response = "<h1>Sorry, I was unable to translate:</h1>" if unable_to_translate else "<h1> The translated version is:</h1>"
		#log words you can't mark

		return u'{}<br/> {} <a href=''><br/>Translate more </a>'.format(response, translated_sentence)

	return render_template('form.html', form=form)

@app.route('/untranslated', methods=['GET', 'POST'])
def untranslated():
	try:
		untranslated_sentences = open("untranslatable.txt",'r')
	except:
		return "There are no untranslated sentences yet"
	result = ""
	for line in untranslated_sentences:
		result+=line
	return result

if __name__ == '__main__':
	app.run(debug=True)
