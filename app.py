from flask import Flask, session, redirect, url_for, escape, request, flash
from flask import render_template
from gothonweb import planisphere
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
import os
import psycopg2

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Wi$$ows12@localhost/gothons'
DATABASE_URL = os.environ['postgres://xtrdxjlqkvxjqh:7eb9ed8ef4b09f88f67745c810a715e399fb7c0e1b8b4c54db69734f1207d307@ec2-54-225-115-234.compute-1.amazonaws.com:5432/drpbg9st86t3']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
Bootstrap(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playername = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(80))
    data = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    playername = StringField('player name', validators=[InputRequired(message='Player name required!'), Length(max=10, message='Max length 10 characters')])
    password = PasswordField('password', validators=[InputRequired(message='Password required!'), Length(max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    playername = StringField('player name', validators=[InputRequired(message='Player name required!'), Length(max=10, message='Max length 10 characters')])
    password = PasswordField('password', validators=[InputRequired(message='Password required!'), Length(max=80)])


@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    count = 100000

    if form.validate_on_submit():
        new_player = User(playername=form.playername.data, password=form.password.data, data=count)

        db.session.add(new_player)
        db.session.commit()
        flash("Registration successful, log in to play.")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm()
    session['room_name'] = planisphere.START # passing session list the name of starting room variable

    if form.validate_on_submit():
        user = User.query.filter_by(playername=form.playername.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for("dashboard")) # redirects to dashboard route below
        return '<h1> Invalid username or password </h1>'
    return render_template('login.html', form=form)

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
#    users = User.query.order_by(User.data)
    users = User.query.with_entities(User.data, User.playername).all()
    print(users)        
    users.sort()
    for user in users:
        print(user)
        print(user[0])
        if user[0] == 100000:
            users[:] = [user for user in users if user[0] != 100000]          
        print(users)
    user_scores = [x[0] for x in users]
    user_names = [x[1] for x in users]
    return render_template('dashboard.html', name=current_user.playername, user_scores=user_scores, user_names=user_names)


#turns = 0
class Counter():
    count = 0
turns = Counter()

@app.route("/game", methods=['GET', 'POST'])
def game():
    user = User()
    form = RegisterForm()
    room_name = session.get('room_name') # returns name of room object from the session list
# if room_name = you_win then add 'winner' to user's place in database and the count. On dashboard, the only usernames that appear
# should be those with winner

    if request.method == "GET":
        if room_name:
            room = planisphere.load_room(room_name) # returns actual Room object
            return render_template("show_room.html", room=room, turns=turns) # renders show_room.html and sets room param for the template
        else:
            return render_template("you_died.html")
    else: # if POST
        action = request.form.get('action') # takes user input from form here as string
#       print(action)
#       print(type(action))

        if room_name and action: 
            room = planisphere.load_room(room_name)
            print(room) # this is the actual name of the room - "Central Corridor"
#            print(type(room))
            next_room = room.go(action)
            print(room_name) # room name is central_corridor and a string
            print(next_room)
#            print(type(room_name))

            if not next_room:
                session['room_name'] = planisphere.name_room(room)
                flash("Your last attempt was incorrect.")
                turns.count += 1
                print(turns.count)
                return redirect(url_for("game"))
 
            else:
                if action not in ["tell a joke", planisphere.code, "slowly place the bomb"]:
                    session['room_name'] = planisphere.name_room(next_room)
                    turns.count += 1
#                    print(turns.count)
                    print('potato')
#                    print(type(action))
                    if (action == '2') and current_user.data == 100000:
                        current_user.data = turns.count
                        db.session.commit()
                        print('new score added to user')
                    else:
                        if (action == '2') and current_user.data > turns.count:
                            current_user.data = turns.count
                            db.session.commit()
                            print('score updated')
                        else:
                            pass
#                    print('data updated')
#                    print(current_user.data)
                    return redirect(url_for("game"))
                else:
                    session['room_name'] = planisphere.name_room(next_room)
                    turns.count += 1
#                    print(turns.count)
#                    print(current_user.data)
                    return render_template("room_complete.html", room=room)
        
        else:
            flash("Your last attempt was incorrect.")
            turns.count += 1
#            print(turns.count)
            return redirect(url_for("game"))


@app.route("/help")
def help():
    room_name = session.get('room_name')
    room = planisphere.load_room(room_name)
    return render_template("help.html", room=room)

@app.route("/logout")
@login_required
def logout():
    logout_user
    return redirect(url_for("index"))

@app.route("/playagain")
@login_required
def play_again():
    session['room_name'] = planisphere.START
    turns.count = 0
    return redirect(url_for("game"))


if __name__ == "__main__":
    app.run(debug=False)
