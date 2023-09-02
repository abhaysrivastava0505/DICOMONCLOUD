from flask import Flask, render_template, abort
from flask import request
from forms import LoginForm, SignUpForm
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patientrecords-1.db'
db = SQLAlchemy(app)

"""Model for Patients."""
class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    type = db.Column(db.String)
    modality = db.Column(db.String)
    posted_by =db.Column(db.String, db.ForeignKey('user.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    patientRecords = db.relationship('PatientRecord', backref='user')

db.create_all()

# Create "team" user and add it to session
team = User(full_name = "PatientRecord Team", email = "team@patientrecord.com", password = "adminpass")
db.session.add(team)

# Create all PatientRecord
nelly = PatientRecord(title = "Nelly", type = "DICOM", modality = "CT")
yuki = PatientRecord(title = "Yuki", type = "DICOM", modality = "CT")
basker = PatientRecord(title = "Basker", type = "DICOM", modality = "CT")
mrfurrkins = PatientRecord(title = "Mr. Furrkins", type = "DICOM", modality = "CT")

# Add all PatientRecord to the session
db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mrfurrkins)

# Commit changes in the session
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
finally:
    db.session.close()

@app.route('/')
def home():  # put application's code here
    patientRecords = PatientRecord.query.all()
    return render_template("home.html", patientRecords=patientRecords)


@app.route("/details/<int:patient_record_id>")
def patientRecords_details(patient_record_id):

    patient_record = PatientRecord.query.get(patient_record_id)
    if patient_record is None:
        abort(404, description="No Patient was Found with the given ID")
    return render_template("details.html", patient_record = patient_record)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data),None)
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template("login.html", form=form, message="Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.id
            return render_template("login.html", message="Successfully Logged In!")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home', _scheme='http', _external=True))


@app.route("/signup", methods=["GET", "POST"])
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
