from flask import Flask, render_template
import random
app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/fortune')
def fortune():
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
    ]
    chosen_fortune = random.choice(fortunes)
    return render_template('fortune.html', fortune=chosen_fortune)

if __name__ == '__main__':
    app.run(debug=True)
