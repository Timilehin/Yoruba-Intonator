from flask import Flask, render_template 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

from flask_bootstrap import Bootstrap
import viterbi

app = Flask(__name__)
app.config['SECRET_KEY']= 'THIS IS A SECRET!'
bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
	unmarked_yoruba = StringField('Unmarked Yoruba: ', validators=[InputRequired()],  widget=TextArea())

@app.route('/', methods=['GET', 'POST'])
def form():
	form = LoginForm()

	if form.validate_on_submit():
		return '<h1> The translated version is:</h1><br/> {} <a href=''>Translate more </a>'.format(viterbi.get_most_likely_sentence_markings(form.unmarked_yoruba.data))

	return render_template('form.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
