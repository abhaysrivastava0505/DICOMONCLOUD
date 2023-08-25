from flask import Flask, render_template
from flask import request
from forms import LoginForm, SignUpForm
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

db.create_all()

@app.route('/')
def home():  # put application's code here
    return render_template("home.html")



@app.route("/login", methods= ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data),None)
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form=form, message="Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.id
            return render_template("login.html", message="Successfully Logged In!")
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home', _scheme='http', _external=True))
@app.route("/signup",methods=["GET","POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(full_name=form.full_name.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form, message="Email already exist in the system, Please login")
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    return render_template("signup.html", form=form)

if __name__ == '__main__':
    app.run()
