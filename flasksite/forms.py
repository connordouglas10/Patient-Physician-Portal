from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasksite import login_manager


from flasksite.models import Patient, Physician, Users, Connection

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = RadioField('Select below', choices=[('male','Male'),('female','Female')], validators=[DataRequired()])
    category = RadioField('Select below', choices=[('patient','Patient'),('Physician','Physician')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Patient.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address already taken')

# new below
class UpdatePatientAccountForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    height = IntegerField('Height')
    weight = IntegerField('Weight')
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    notes = StringField('Notes')
    submit = SubmitField('Update')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address already taken')

class UpdatePhysicianAccountForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    specialty = StringField('Specialty', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address already taken')