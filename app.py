from flask import Flask, render_template, url_for, request, redirect, flash
from flask_wtf import Form
from wtforms import SelectField, IntegerField
from wtforms.validators import input_required, none_of

app = Flask(__name__)
app.config.from_object('config')

class ChooseForm(Form):
    relation = SelectField('Type of relation',
        coerce=int,
        choices=[
            (0, 'Type of relation'),
            (1, 'Item 1'),
            (2, 'Item 2'),
            (3, 'Item 3')],
        default=0,
        validators=[
            input_required(message="Please, choose type of relation"),
            none_of([0], message="Please, choose type of relation")
            ])
    category = SelectField(
        coerce=int,
        choices=[(0, 'Category'),
                 (1, 'Item 1'),
                 (2, 'Item 2'),
                 (3, 'Item 3')],
        default=0,
        validators=[
            input_required(message="Please, choose category"),
            none_of([0], message="Please, choose category")
            ])
    messages_number = IntegerField('Number of messages',
        validators=[
            input_required(message="Please, choose number of messages")])

@app.route('/', methods=['GET','POST'])
def index():
    form = ChooseForm()
    if request.method == 'POST' and form.validate():
        flash("Good")
        return redirect(url_for('index'))
    return render_template('main.html', form=form)

@app.route('/graph')
def graph():
    return render_template('graph2.html')

if __name__ == '__main__':
    app.run(debug=True)
