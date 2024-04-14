from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# database name
db_path = 'database/test.db'

# config app to use database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# define admin and user
ADMIN_ID = 'admin'
ADMIN_PASSWORD = 'admin1234'
USER_ID = 'user'
USER_PASSWORD = 'user1234'


class LoginForm(FlaskForm):
    id = StringField('ID', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/wrong')
def wrong():
    return render_template('wrong.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.id.data == ADMIN_ID and form.password.data == ADMIN_PASSWORD:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('wrong'))
    return render_template('admin_login.html', form=form)


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.id.data == USER_ID and form.password.data == USER_PASSWORD:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('wrong'))
    return render_template('user_login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
