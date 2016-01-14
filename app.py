from flask import Flask, render_template, jsonify, url_for, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/handle', methods=['POST'])
def handle():
    form = request.form
    print form
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
