from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

# @app.route('/graph')
# def graph():
#     return render_template('graph2.html')

@app.route('/handle', methods=['POST'])
def handle():
    form = request.form
    print form
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
