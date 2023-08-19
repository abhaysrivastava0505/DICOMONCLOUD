from flask import Flask, render_template
from flask import request
from forms import LoginForm, SignUpForm
from flask import session, redirect, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
users = [
    {"id": 1, "full_name": "admin", "email": "admin@dicomoncloud.com", "password": "admin"},
]


@app.route('/')
def home():  # put application's code here
    return render_template("home.html")



@app.route("/login", methods= ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data),None)
        if user is None:
            return render_template("login.html", form=form, message="Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user
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
        new_user = {"id": len(users) + 1, "full_name": form.full_name.data, "email": form.email.data,
                    "password": form.password.data}
        users.append(new_user)
        return render_template("signup.html", message="Successfully signed up")
    return render_template("signup.html", form=form)

if __name__ == '__main__':
    app.run()
