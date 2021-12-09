import os

from flask import Flask, render_template, redirect, session, url_for, request, flash, abort
from flask_bcrypt import bcrypt, generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afsdlmafmamowe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()+"/static"

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from model import User, UserData, FeedbackDB, LanguagesSpoken, ExperienceDB
from form import Search, RegistrationForm, LoginForm, Feedback, EditData, Suggest, Experience


@app.before_first_request
def setup_db():
    #db.drop_all()
    #session.clear()
    db.create_all()


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.filter(User.id == id).first()
    except:
        return None


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Search()
    if form.validate_on_submit():
        province = form.province.data
        return redirect(url_for('search', province=province.capitalize()))

    return render_template('index.html', form=form)


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    me = False
    form = Feedback()
    form_exp = Experience()
    userdata = UserData.query.filter_by(username=username).first()
    if not userdata:
        flash('Profile not founded')
        render_template('404')
    user = User.query.filter_by(email=userdata.email).first()
    sender = UserData.query.filter_by(username=session['username']).first()
    if form.validate_on_submit():
        #if current_user.is_authenticated:
        if sender:
            fb = FeedbackDB(sender=sender.username, receiver=userdata.username, star=form.star.data, review=form.review.data, date=datetime.date.today())
            db.session.add(fb)
            db.session.commit()
            flash("Feedback Sent", category="success")
        else:
            flash("You need to log in before entering a feedback", category="error")
    if form_exp.validate_on_submit():
        exp = ExperienceDB(
            username=session['username'],
            province=form_exp.province.data.capitalize(),
            description=form_exp.description.data,
            date_of_addition=datetime.date.today(),
            date_of_experience=form_exp.date_of_experience.data,
            end_date=form_exp.end_date.data,
            price=form.price.data
        )
        db.session.add(exp)
        db.session.commit()
        flash("Experience added, thank you!", category="experience")
        return redirect(url_for('profile', username=session['username']))
    if sender:
        if sender.username == username:
            me = True
    fr = FeedbackDB.query.filter_by(receiver=userdata.username)
    return render_template('profile.html', username=username, form=form, user=user, me=me, feedback_received=fr, userdata=userdata, form_exp=form_exp)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #if session["username"]:
    #    return redirect(url_for('profile'), username=session["username"])
    form = RegistrationForm()
    if form.validate_on_submit():
        pass_hashed = generate_password_hash(form.password.data)
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        usr = UserData.query.filter_by(username=form.username.data).first()
        if usr:
            flash("Username already used", category="error")
        if user:
            flash("Email already used", category="error")
        elif form.password.data != form.confirm.data:
            flash("Make sure you typed the password correctly", category="error")
        else:
            username = form.username.data
            new_user2 = User(
                email=email.lower(),
                password=pass_hashed)
            new_user = UserData(
                username=username.lower(),
                name=form.name.data.capitalize(),
                surname=form.surname.data.capitalize(),
                bio=form.bio.data,
                phone=form.phone.data,
                email=form.email.data.lower(),
                province=form.province.data.capitalize()
            )
            db.session.add(new_user2)
            db.session.commit()
            db.session.add(new_user)
            db.session.commit()
            for l in form.language.data:
                lang_user = LanguagesSpoken(username=username, lang=l)
                db.session.add(lang_user)
                db.session.commit()
            flash("Account created!", category="success")
            session['username'] = new_user.username
            #if not os.path.exists('static/' + str(session.get('username'))):
             #   os.makedirs('static/' + str(session.get('username')))
            #file_url = os.listdir('static/' + str(session.get('username')))
            #file_url = [str(session.get('username')) + "/" + file for file in file_url]
            #filename = photos.save(form.profile_picture.data, name=str(session.get('username')) + '.jpg', folder=str(session.get('username')))
            #file_url.append(filename)
            #login_user(new_user2)
            return redirect(url_for('profile', username=form.username.data))

    return render_template('signup.html', form=form)


@app.route('/signup4guides', methods=['GET', 'POST'])
def signup4guides():
    form = RegistrationForm()
    #if session['username']:
    #   return redirect(url_for('profile', username=session['username']))
    if form.validate_on_submit():
        pass_hashed = generate_password_hash(form.password.data)
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        usr = UserData.query.filter_by(username=form.username.data).first()
        if usr:
            flash("Username already used", category="error")
        if user:
            flash("Email already used", category="error")
        elif form.password.data != form.confirm.data:
            flash("Make sure you typed the password correctly", category="error")
        else:
            username = form.username.data
            new_user2 = User(
                email=email.lower(),
                password=pass_hashed)
            new_user = UserData(
                username=username.lower(),
                name=form.name.data.capitalize(),
                surname=form.surname.data.capitalize(),
                bio=form.bio.data,
                phone=form.phone.data,
                email=form.email.data.lower(),
                guide=1,
                professional=form.professional.data,
                province=form.province.data.capitalize()
            )
            db.session.add(new_user2)
            db.session.commit()
            db.session.add(new_user)
            db.session.commit()
            for l in form.language.data:
                lang_user = LanguagesSpoken(username=username, lang=l)
                db.session.add(lang_user)
                db.session.commit()
            flash("Account created!", category="success")
            session['username'] = new_user.username
            #if not os.path.exists('static/' + str(session.get('username'))):
             #   os.makedirs('static/' + str(session.get('username')))
            #file_url = os.listdir('static/' + str(session.get('username')))
            #file_url = [str(session.get('username')) + "/" + file for file in file_url]
            #filename = photos.save(form.profile_picture.data, name=str(session.get('username')) + '.jpg', folder=str(session.get('username')))
            #file_url.append(filename)
            #login_user(new_user2)
            return redirect(url_for('profile', username=form.username.data))
    return render_template('signup4guides.html', form=form)


@app.route('/search/<province>', methods=['GET', 'POST'])
def search(province):
    experiences = ExperienceDB.query.filter_by(province=province.capitalize())
    number_of_experiences = experiences.count()
    form = Suggest()
    if form.validate_on_submit():
        #send an email
        mail = 1
        flash("Mail sent, thank you!", category="success")
    exp = ExperienceDB.join(UserData, Experience.username == UserData.username).query.filter_by(province=province.capitalize())
    return render_template('search.html', province=province, exp=exp, number_of_experiences=number_of_experiences, form=form)


@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                usr = UserData.query.filter_by(email=email).first()
                #login_user(user, remember=form.remember.data)
                session['username'] = usr.username
                next = request.args.get('next')
                # if not is_safe_url(next):
                #   return abort(400)
                # return redirect(next or url_for('index'))
                username = usr.username
                return redirect(url_for('profile', username=username))
            flash("wrong password", category="error")
            return redirect(url_for('login'))
        flash("invalid email", category="error")
        return redirect(url_for('login'))
    if current_user.is_authenticated:
        return redirect('profile', username=current_user.user_id)
    return render_template('login.html', form=form)


@app.route('/logout')
#@login_required
def logout():
    #logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route('/editdata', methods=['GET', 'POST'])
def editdata():
    if not session['username']:
        return redirect('login')
    form = EditData()
    if form.validate_on_submit():
        update_statement = UserData.update().where(username=session['username']).values(
            name=form.name.data,
        )
        db.execute(update_statement)
        return redirect('profile', username=session['username'])
    return render_template('editdata.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
