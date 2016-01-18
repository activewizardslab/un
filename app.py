from flask import Flask, render_template, url_for, request, redirect, flash
from flask_wtf import Form
from wtforms import SelectField, IntegerField
from wtforms.validators import input_required, none_of
import pandas as pd

app = Flask(__name__)
app.config.from_object('config')

class ChooseForm(Form):
    relation = SelectField('Type of relation',
        coerce=int,
        choices=[
            (0, 'Type of relation'),
            (1, 'Causal link (->)'),
             (2, 'Causal link (<-)'),
             (3, 'Constraint, barriers, challanges'),
             (4, 'Recommendatins')],
        default=0,
        validators=[
            input_required(message="Please, choose type of relation"),
            none_of([0], message="Please, choose type of relation")
            ])
    category = SelectField(
        coerce=int,
        choices=[(0, 'Category'),
                 (1, u'no poverty'),
                 (2, u'zero hunger'),
                 (3, u'good health and well beeing'),
                 (4, u'quality education'),
                 (5, u'gender equality'),
                 (6, u'clean water and sanitation'),
                 (7, u'affordable and clean energy'),
                 (8, u'decent work and economic growth'),
                 (9, u'industry innowation and infrastructure'),
                 (10, u'reduced inequalities'),
                 (11, u'responsible consumption and production'),
                 (12, u'climate action'),
                 (13, u'life below water'),
                 (14, u'life on land'),
                 (15, u'piece justice and strong institutions'),
                 (16, u'partnership for the goals')],
        default=0,
        validators=[
            input_required(message="Please, choose category"),
            none_of([0], message="Please, choose category")
            ])
    messages_number = IntegerField('Limit',
        validators=[
            input_required(message="Please, choose number of messages")])

def unique(s):
    
    n = len(s)
    if n == 0:
        return []
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]
    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u

@app.route('/', methods=['GET','POST'])
def index():
    form = ChooseForm()
    if request.method == 'POST' and form.validate():

        category = form.data['category']
        relationship = form.data['relation']
        limit = form.data['messages_number']

        mergeData_general = pd.read_csv('../../work/un-linkssds/data/mergeData_general.csv')
        mergeData_temp = mergeData_general[mergeData_general['SDG{}Word'.format(category)] != '-0']

        if relationship == 1:
            mergeData_temp1 = mergeData_temp[(mergeData_temp['common'] == 1)&(mergeData_temp['direction'] == 1)]
        elif relationship == 2:
            mergeData_temp1 = mergeData_temp[(mergeData_temp['common'] == 1)&(mergeData_temp['direction'] == 2)]
        elif relationship == 3:
            mergeData_temp1 = mergeData_temp[(mergeData_temp['common'] == 0)&(mergeData_temp['constraint'] == 1)]
        elif relationship == 4:
            mergeData_temp1 = mergeData_temp[(mergeData_temp['common'] == 0)&(mergeData_temp['recommendation'] == 1)]
        mergeData_temp2 = mergeData_temp1['text']

        result = unique(mergeData_temp2.values)[:int(limit)]
        return render_template('main.html', form=form, data = result, choise = [category,relationship,limit])
    return render_template('main.html', form=form)

@app.route('/graph')
def graph():
    return render_template('graph2.html')

if __name__ == '__main__':
    app.run(debug=True)
