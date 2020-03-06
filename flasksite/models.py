from flasksite import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.String, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sex = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, default='N/A')
    height = db.Column(db.Integer, default=0)
    weight = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Patient('{self.id}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.image}', '{self.password}', '{self.sex}', '{self.age}', '{self.notes}', '{self.height}', '{self.weight}')"


class Physician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.String, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sex = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    specialty = db.Column(db.String, default='N/A')
    school = db.Column(db.String, default='N/A')

    def __repr__(self):
        return f"Physician('{self.id}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.image}', '{self.password}', '{self.sex}', '{self.age}', '{self.specialty}, '{self.school}')"


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image = db.Column(db.String, nullable=False, default='default.jpg')
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    category = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.image}', '{self.age}', '{self.password}', '{self.category}')"

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    physician_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Connection('patientID: {self.patient_id}, 'physicianID: {self.physician_id})"

