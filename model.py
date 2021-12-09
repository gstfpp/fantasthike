from flask_login._compat import text_type

from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), autoincrement=True)
    email = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return text_type(self.id)

    def get(self, id):
        return unicode(self.id)

    def __repr__(self):
        return '<Email %r>' % self.email


class UserData(db.Model):
    __tablename__ = 'userdata'
    username = db.Column(db.String, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120), db.ForeignKey(User.email), unique=True, nullable=False)
    guide = db.Column(db.Boolean, default=0)
    professional = db.Column(db.Boolean, default=0)
    province = db.Column(db.String)
    ProfilePicture = db.Column(db.Text)


class LanguagesSpoken(db.Model):
    __tablename__ = 'languagesspoken'
    username = db.Column(db.Integer, db.ForeignKey(UserData.username), primary_key=True)
    lang = db.Column(db.String(40), primary_key=True)


class FeedbackDB(db.Model):
    __tablename__ = 'feedback'
    sender = db.Column(db.Integer, db.ForeignKey(User.email), primary_key=True)
    receiver = db.Column(db.Integer, db.ForeignKey(User.email), primary_key=True)
    star = db.Column(db.Integer)
    date = db.Column(db.Date, primary_key=True)
    review = db.Column(db.String())


class ExperienceDB(db.Model):
    __tablename__ = 'experience'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(), db.ForeignKey(UserData.username))
    title = db.Column(db.String(), nullable=False)
    province = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text)
    date_of_addition = db.Column(db.Date, nullable=False)
    date_of_experience = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    price = db.Column(db.Integer, nullable=False)
