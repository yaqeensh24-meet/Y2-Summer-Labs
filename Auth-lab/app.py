from flask import Flask, render_template,url_for,redirect,request, session 
import pyrebase
Config = {
  "apiKey": "AIzaSyC0urAgXru4EdaPxCGRiWCoqg99Lhcp758",
  "authDomain": "auth-lab-66d53.firebaseapp.com",
  "projectId": "auth-lab-66d53",
  "storageBucket": "auth-lab-66d53.appspot.com",
  "messagingSenderId": "1082519331200",
  "appId": "1:1082519331200:web:42af54685f8c5e6c5b6165",
  "measurementId": "G-PBQ2EM7QZQ",
  "databaseURL": "https://auth-lab-66d53-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "yaqeen"

@app.route('/', methods = ['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      print("welcome")
      session['user'] = auth.create_user_with_email_and_password(email, password)
      session['quote'] = ""
      session['quotes'] = []
      return redirect(url_for('home'))
    except Exception as e:
      erorr_massege=str(e)
      return render_template('error.html',erorr_massege=erorr_massege)
  return render_template("signup.html")


@app.route('/sign-in', methods=['GET','POST'])
def signIn():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    try:
      session['user'] = auth.sign_in_with_email_and_password(email, password)
      session['quote'] = ""
      session['quotes'] = []
      return redirect(url_for('home'))
    except:
      erorr_massege=str(e)
      return render_template('error.html',erorr_massege=erorr_massege)
  return render_template("signin.html")

@app.route('/home', methods = ['GET','POST'])
def home():
  if request.method == 'POST':
    print(session['quote'])
    quote = request.form['quote']
    session['quote'] = quote
    session['quote'].append(quote)
    session.modified=True
    additional_info=request.form.get("additional_info","")
    quote_dict={"qouts":quote, "speaker":speaker,"additional_info":additional_info}
    return redirect(url_for('thanks'))
  return render_template('home.html')

@app.route('/display')
def display():
  quotes = session['quotes']
  print(session['quotes'])
  return render_template("display.html", quotes = quotes)

@app.route('/thanks')
def thanks():
  quote = session['quote']
  session['quotes'].append(quote)
  session.modified = True
  print(session['quotes'])
  return render_template("thanks.html",quote = quote)

@app.route('/sign-out')
def signOut():
  session['user']=None
  auth.current_user = None
  return redirect(url_for('signIn'))

if __name__ == '__main__':
    app.run(debug=True)