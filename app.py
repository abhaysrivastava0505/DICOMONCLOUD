from flask import Flask, render_template
from flask import request
from forms import LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
users = {
    "a.abc@gmail.com": "abc",
    "b.abc@gmail.com": "bcd"
}


@app.route('/')
def home():  # put application's code here
    return render_template("home.html")



@app.route("/login", methods= ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        for u_name, u_password in users.items():
            if u_name == form.email.data and u_password == form.password.data:
                return render_template("login.html", form = form , message = "Successful Login")
            else:
                return render_template("login.html", form=form, message="Incorrect Email or Password !!!")
    elif form.errors:
        print(form.errors.items())
    return render_template("login.html", form = form)

if __name__ == '__main__':
    app.run()
