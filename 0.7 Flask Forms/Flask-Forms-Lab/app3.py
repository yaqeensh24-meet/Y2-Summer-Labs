from flask import Flask,render_template,url_for,redirect,request
import random
app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        birth_month = request.form['birth_month']
        return render_template('fortune3.html', birth_month=birth_month,  fortune=chosen_fortune)
    return render_template('home3.html')
    
@app.route('/fortune')
def fortune():
    birth_month = request.args.get('birth_month', '')
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
    return render_template('fortune3.html', fortune=chosen_fortune)

if __name__ == '__main__':
    app.run(debug=True)
