from flask import Flask, render_template, url_for, redirect, request, session
import pyrebase

# Firebase configuration
Config = {
    "apiKey": "AIzaSyC0urAgXru4EdaPxCGRiWCoqg99Lhcp758",
    "authDomain": "auth-lab-66d53.firebaseapp.com",
    "databaseURL": "https://auth-lab-66d53-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "auth-lab-66d53",
    "storageBucket": "auth-lab-66d53.appspot.com",
    "messagingSenderId": "1082519331200",
    "appId": "1:1082519331200:web:7f9e6e1cbac6401f5b6165",
    "measurementId": "G-JZ6WQW4385"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "yaqeen"

@app.route('/', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            session['quotes'] = []

            user_data = {
                "full_name": full_name,
                "email": email,
                "username": username
            }
            db.child("Users").child(user['localId']).set(user_data)
            
            return redirect(url_for('home'))
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    return render_template("signup.html")

@app.route('/sign-in', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            session['quotes'] = []
            return redirect(url_for('home'))
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    return render_template("signin.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect(url_for('signUp'))
    if request.method == 'POST':
        text = request.form['quote']
        said_by = request.form['said_by']
        quote = {
            "text": text,
            "said_by": said_by,
            "uid": session['user']['localId']
        }
        db.child("Quotes").push(quote)
        return redirect(url_for('thanks'))
    return render_template('home.html')

@app.route('/display')
def display():
    if 'user' not in session:
        return redirect(url_for('signUp'))
    quotes = db.child("Quotes").get().val()
    return render_template("display.html", quotes=quotes)

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route('/sign-out', methods=['POST'])
def signOut():
    session.pop('user', None)
    return redirect(url_for('signIn'))

@app.route('/error')
def error():
    error_message = request.args.get('message', 'An error occurred. Please try again.')
    return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
