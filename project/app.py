from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
from timeit import default_timer as timer

app = Flask(__name__,
template_folder='templates',static_folder='static')
app.secret_key = 'your_secret_key'
firebaseConfig = {
  "apiKey": "AIzaSyDV7pQ4P60uoyis8kpmt8OyhyVCO9KlEUE",
  "authDomain": "website-habitracker.firebaseapp.com",
  "projectId": "website-habitracker",
  "storageBucket": "website-habitracker.appspot.com",
  "messagingSenderId": "424966838761",
  "appId": "1:424966838761:web:d6f60ff3acb904b174d378",
  "measurementId": "G-B5GF3F5ZYL",
  "databaseURL":"https://website-habitracker-default-rtdb.europe-west1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_name=request.form['user_name']
        name=request.form['name']
    
        try:
            user = auth.create_user_with_email_and_password(email, password)
            
            user_id = user['localId']
            session['user_id'] = user_id

            db.child("users").child(user_id).set({
                'email': email,
                'profile': {
                    'name': name,
                    'username': user_name
                },
                'habits': None
            })
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Error creating user: {e}")
            return "Error creating user, please try again."
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user_id'] = user['localId']
            return redirect(url_for('dashboard'))
        except:
            return "Invalid email or password."
    return render_template('signin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_id = session['user_id']

    if request.method == 'POST':
        key = request.form['key']
        habit_ref = db.child("users").child(user_id).child("habits").child(key)
        habit = habit_ref.get().val()
        if habit and 'counter' in habit:
            current_value = habit['counter']
            new_value = current_value + 1
      
        # Update the counter value in the database
        db.child("users").child(user_id).child("habits").child(key).update({"counter": new_value})

    user_habits = db.child("users").child(user_id).child("habits").get().val()
    if user_habits is None:
        user_habits = {}

    return render_template('dashboard.html', habits=user_habits)

@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'GET':
        return render_template('add_habit.html')
    else:
        try:
            name = request.form['habit_name']
            describtion = request.form['habit_discription']
            habit = {
            'name' : name , 
            "describtion" : describtion,
            "counter" : 0
            }

            print(habit)

            user_id = session['user_id']

            print(user_id)

        
            db.child("users").child(user_id).child("habits").push(habit)
            return redirect(url_for("dashboard"))
        except:
            return "error in making habit"

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    user_id = session['user_id']
    if request.method == 'POST':
        name = request.form['name']
        email=request.form['email']
        db.child("users").child(user_id).update({"name": name, "email":email})
        return redirect(url_for('dashboard'))



    user_data = db.child("users").child(user_id).get().val()
    profile_data = db.child("users").child(user_id).child("profile").get().val()
    return render_template('profile.html', user_data=user_data, profile_data = profile_data)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)