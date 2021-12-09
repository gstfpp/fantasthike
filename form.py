from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, SelectField, TextAreaField, PasswordField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, EqualTo, NumberRange, Email, Length
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    remember = BooleanField('remember me')
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    phone = StringField('phone')
    language = SelectMultipleField('languages', choices=[('DE','German'), ('EN','English'), ('FR','French'), ('IT','Italian'), ('PO','Portuguese'), ('AR','Arabic'), ('CH','Chinese')])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    professional = BooleanField('professional')
    confirm = PasswordField('confirm')
    province = StringField('province')
    #profile_picture = FileField('ProfilePicture', validators=[FileAllowed('jpg', 'png'), DataRequired()])
    submit = SubmitField('Create account')


class EditData(FlaskForm):
    name = StringField('name')
    surname = StringField('surname')
    bio = TextAreaField('Bio')
    phone = StringField('phone')
    password = PasswordField('NewPassword', validators=[EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('RepeatPassword')
    language = SelectMultipleField('languages', choices=[('DE','German'), ('EN','English'), ('FR','French'), ('IT','Italian'), ('PO','Portuguese'), ('AR','Arabic'), ('CH','Chinese')])
    province = StringField('province')
    ProfilePicture = FileField('ProfilePicture', validators=[FileAllowed('jpg', 'png')])
    submit = SubmitField('Edit')


class Search(FlaskForm):
    province = StringField('province')
    submit = SubmitField('submit')


class Suggest(FlaskForm):
    email = StringField('email',validators=[DataRequired(), Email()])
    submit = SubmitField('submit')


class Feedback(FlaskForm):
    star = IntegerField(default=3, validators=[DataRequired(), NumberRange(1,5)])
    review = TextAreaField('review', validators=[DataRequired()])
    submit = SubmitField('submit')


class Experience(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1,20, "Title must be between 1 and 20 characters")])
    description = TextAreaField('description', validators=[DataRequired()])
    province = StringField('province', validators=[DataRequired()])
    date_of_experience = DateField('date_of_experience', format='%Y-%m-%d')
    end_date = DateField('end_date', format='%Y-%m-%d')
    price = IntegerField('price', validators=[DataRequired()], default=0)
    submit = SubmitField('submit')