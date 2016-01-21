from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_wtf import Form
from wtforms import SelectField, IntegerField
from wtforms.validators import input_required, none_of
import pandas as pd
from collections import Counter

app = Flask(__name__)
app.config.from_object('config')

class ChooseForm(Form):
    relation = SelectField('Type of relation',
        coerce=int,
        choices=[
            (0, 'Type of relation'),
            (1, 'Causal link (->)'),
             (2, 'Causal link (<-)'),
             (3, 'Constraint, barriers, challenges'),
             (4, 'Recommendations')],
        default=0,
        validators=[
            input_required(message="Please, choose type of relation"),
            none_of([0], message="Please, choose type of relation")
            ])
    category = SelectField(
        coerce=int,
        choices=[(0, 'Category'),
                 (1, u'No poverty'),
                 (2, u'Zero hunger'),
                 (3, u'Good health and well beeing'),
                 (4, u'Quality education'),
                 (5, u'Gender equality'),
                 (6, u'Clean water and sanitation'),
                 (7, u'Affordable and clean energy'),
                 (8, u'Decent work and economic growth'),
                 (9, u'Industry innowation and infrastructure'),
                 (10, u'Reduced inequalities'),
                 (12, u'Responsible consumption and production'),
                 (13, u'Climate action'),
                 (14, u'Life below water'),
                 (15, u'Life on land'),
                 (16, u'Piece justice and strong institutions'),
                 (17, u'Partnership for the goals')],
        default=0,
        validators=[
            input_required(message="Please, choose category"),
            none_of([0], message="Please, choose category")
            ])
    messages_number = IntegerField('Limit',
        validators=[
            input_required(message="Please, choose number of messages")])

class CloudForm(Form):
    cloud_category = SelectField(
        coerce=int,
        choices=[(0, 'Category'),
                 (1, u'No poverty'),
                 (2, u'Zero hunger'),
                 (3, u'Good health and well beeing'),
                 (4, u'Quality education'),
                 (5, u'Gender equality'),
                 (6, u'Clean water and sanitation'),
                 (7, u'Affordable and clean energy'),
                 (8, u'Decent work and economic growth'),
                 (9, u'Industry innowation and infrastructure'),
                 (10, u'Reduced inequalities'),
                 (12, u'Responsible consumption and production'),
                 (13, u'Climate action'),
                 (14, u'Life below water'),
                 (15, u'Life on land'),
                 (16, u'Piece justice and strong institutions'),
                 (17, u'Partnership for the goals')],
        default=0,
        validators=[
            input_required(message="Please, choose category"),
            none_of([0], message="Please, choose category")
            ])

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
mergeData_general = pd.read_csv('static/data/mergeData_general.csv')

@app.route('/', methods=['GET','POST'])
def index():
    form1 = ChooseForm()
    form2 = CloudForm()
    category = 1

    mergeData_temp1 = mergeData_general[mergeData_general['SDG{}Word'.format(category)] != '-0']
    mergeData_temp2 = mergeData_temp1['text']
    result = unique(mergeData_temp2.values)


    text1 = ' '.join(list(mergeData_temp1['SDG11Word'].values))
    text2 = ' '.join(list(mergeData_temp1['SDG{}Word'.format(category)].values))

    cloud1 = Counter(mergeData_temp1['SDG11Word'].values).items()
    cloud2 = Counter(mergeData_temp1['SDG{}Word'.format(category)].values).items()

    return render_template('main.html', form1=form1, form2=form2, cloud=[cloud1,cloud2])


@app.route('/one', methods=['POST'])
def one():
    form = ChooseForm(request.form)
    if form.validate():
        category = form.data['category']
        relationship = form.data['relation']
        limit = form.data['messages_number']

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
        return jsonify(data=result)
    else:
        return jsonify(error=form.errors)

@app.route('/two', methods=['POST'])
def two():
    form = CloudForm(request.form)
    if form.validate():
        category = form.data['cloud_category']

        mergeData_temp1 = mergeData_general[mergeData_general['SDG{}Word'.format(category)] != '-0']
        mergeData_temp2 = mergeData_temp1['text']
        result = unique(mergeData_temp2.values)


        text1 = ' '.join(list(mergeData_temp1['SDG11Word'].values))
        text2 = ' '.join(list(mergeData_temp1['SDG{}Word'.format(category)].values))

        cloud1 = Counter(mergeData_temp1['SDG11Word'].values).items()
        cloud2 = Counter(mergeData_temp1['SDG{}Word'.format(category)].values).items()

        return jsonify(data=[cloud1,cloud2])
    else:
        return jsonify(error=form.errors)

if __name__ == '__main__':
    app.run(debug=True)
