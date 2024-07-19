"""from flask import Flask,render_template,url_for,redirect,request,session
import random
app = Flask(__name__)
app.secret_key='your_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        birth_month = request.form['birth_month']
        session['name'] = name
        session['birth_month'] = birth_month
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'name' not in session or 'birth_month' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return redirect(url_for('fortune'))
    return render_template('home.html', name=session['name'])


@app.route('/fortune')
def fortune():
    if 'birth_month' not in session:
        return redirect(url_for('login'))
    birth_month = session['birth_month']
    fortunes = [
        "You will have a great day!",
        "Something unexpected will happen soon.",
        "You will meet someone special today.",
        "A pleasant surprise is waiting for you.",
        "You will achieve your goals.",
        "Good news is on the way.",
        "A new opportunity will present itself.",
        "You will find what you are looking for.",
        "Today is your lucky day!",
        "Happiness is in your future."
        "you will find light in the end of the road"
        "your dreams are waiting for you to take action"]

    index = len(birth_month) % len(fortunes)
    chosen_fortune = fortunes[index]
    return render_template('fortune.html', fortune=chosen_fortune)
    

if __name__ == '__main__':
    app.run(debug=True)"""
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        birth_month = request.form['birth_month']
        session['name'] = name
        session['birth_month'] = birth_month
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'name' not in session or 'birth_month' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return redirect(url_for('fortune'))
    return render_template('home.html', name=session['name'])

@app.route('/fortune', methods=['GET', 'POST'])
def fortune():
    if 'birth_month' not in session:
        return redirect(url_for('login'))
    
    birth_month = session['birth_month']
    fortunes = [
        "You will have a great day!",
        "Something unexpected will happen soon.",
        "You will meet someone special today.",
        "A pleasant surprise is waiting for you.",
        "You will achieve your goals.",
        "Good news is on the way.",
        "A new opportunity will present itself.",
        "You will find what you are looking for.",
        "Today is your lucky day!",
        "Happiness is in your future.",
        "You will find light at the end of the road.",
        "Your dreams are waiting for you to take action."
    ]
    
    index = len(birth_month) % len(fortunes)
    chosen_fortune = fortunes[index]
    session['fortune'] = chosen_fortune
    
    return render_template('fortune.html', fortune=chosen_fortune)

if __name__ == '__main__':
    app.run(debug=True)