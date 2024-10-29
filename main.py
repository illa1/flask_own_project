from flask import Flask, request, session, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


import os
from sqlalchemy.testing.suite.test_reflection import users


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flask.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#========== MODELS ====================================
app.secret_key = 'NDhZjx_aafafTMCafajfxRBkqh-0uYFFur0afafsmA8DVaw'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), default=0, nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'


with app.app_context():
    db.create_all()

#========== ROUTS =====================================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/left-sidebar')
def left_sidebar():
    return render_template('left-sidebar.html')


@app.route('/right-sidebar')
def right_sidebar():
    return render_template('right-sidebar.html')


@app.route('/two-sidebar')
def two_sidebar():
    return render_template('two-sidebar.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if not session.get('username'):
        return redirect('/login')

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('index.html')
    else:
        return render_template('registration.html')


@app.route('/login', methods=['GET'])
def login():
    message = 'Enter you Login password'
    return render_template('login.html', message=message)


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        message = 'Enter correct email'
        return render_template('login.html', message=message)
    else:
        if user.password != password:
            message = 'Enter correct password'
            return render_template('login.html', message=message)
        else:
            session['username'] = user.username
            return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)