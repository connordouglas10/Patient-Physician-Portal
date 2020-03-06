import os
import json
import secrets
import pdfkit
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from flasksite import app, db, bcrypt
from flasksite.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePatientAccountForm, UpdatePhysicianAccountForm
from flasksite.models import Patient, Physician, Users, Connection
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.category == 'patient':
            physicians = Physician.query.all()
            drs = []
            for entry in physicians:
                drDict = { "first_name": entry.first_name,"last_name":entry.last_name, "email":entry.email, "school":entry.school, "specialty":entry.specialty, "id":entry.id, "image":entry.image}
                drs.append(drDict)
            return render_template('patient-home.html', title='Home', physicians=drs)
        else:
            patients = Patient.query.all()
            pts = []
            for entry in patients:
                ptDict = {"first_name": entry.first_name, "last_name": entry.last_name, "email": entry.email, "age": entry.age, "sex": entry.sex, "notes": entry.notes, "image":entry.image}
                pts.append(ptDict)
            return render_template('physician-home.html', title='Home', pts=pts)
    else:
        return render_template('home.html', title='Home')

@app.route("/addConnection", methods=['GET', 'POST'])
def addConnection():
    if request.method == "POST":
        print("patient", request.json['patient'])
        print("doc", request.json['doctor'])
        pat1 = Users.query.filter_by(id=request.json['patient']).first()
        myPatientId = Patient.query.filter_by(email=pat1.email).first()
        myID = myPatientId.id
        arr = Connection.query.filter_by(patient_id=myID, physician_id=request.json['doctor']).first()
        if arr:
            print("Connection already exists.")
            return redirect(url_for('home'))
        print(request.json['patient'])
        print(request.json['doctor'])

        conn = Connection(patient_id=myID, physician_id=request.json['doctor'])
        db.session.add(conn)
        db.session.commit()
    return redirect(url_for('home'))

@app.route("/removeConnection", methods=['GET', 'POST'])
def removeConnection():
    if request.method == "POST":
        print(request.json['patient'])
        print(request.json['doctor'])
        pat1 = Users.query.filter_by(id=request.json['patient']).first()
        myPatientId = Patient.query.filter_by(email=pat1.email).first()
        myID = myPatientId.id
        Connection.query.filter_by(patient_id=myID, physician_id=request.json['doctor']).delete()
        db.session.commit()
    return redirect(url_for('home'))
            

@app.route("/myPhysicians")
def myPhysicians():
    connections = Connection.query.filter_by(patient_id=Patient.query.filter_by(email=current_user.email).first().id)
    docs=[]
    for entry in connections:
        doc = Physician.query.filter_by(id=entry.physician_id).first()
        docDict = {"first_name" : doc.first_name, "last_name" : doc.last_name, "school": doc.school, "specialty": doc.specialty, "email" : doc.email, "id" : doc.id}
        docs.append(docDict)
        #first name, last name, email, specialty, id, curr_user id

    return render_template('myPhysicians.html', title='My Physicians', docs= docs)

@app.route("/myPatients")
def myPatients():
    connections = Connection.query.filter_by(physician_id=Physician.query.filter_by(email=current_user.email).first().id)
    pts = []
    for entry in connections:
        pt = Patient.query.filter_by(id=entry.patient_id).first()
        ptDict = {"first_name":pt.first_name, "last_name":pt.last_name, "email": pt.email, "notes": pt.notes, "height": pt.height, "weight": pt.weight, "age": pt.age, "sex": pt.sex}
        pts.append(ptDict)
    return render_template('myPatients.html', title='My Patients', pts=pts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.category.data == "patient":
            patient = Patient(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed, sex=form.sex.data, age=form.age.data, category=form.category.data, notes='N/A')
            db.session.add(patient)
            db.session.commit()
        else: 
            physician = Physician(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed, sex=form.sex.data, age=form.age.data, category=form.category.data, specialty='N/A', school='N/A')
            db.session.add(physician)
            db.session.commit()
        user = Users(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, age=form.age.data, password=hashed, category=form.category.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.category.data} {form.first_name.data} {form.last_name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.category == 'patient':
        print("create patient account form")
        form = UpdatePatientAccountForm()
        print(form.errors)
        print(form.validate_on_submit())
        if form.validate_on_submit():
            print('validated on submit')
            temp = Patient.query.filter_by(email=current_user.email).first()
            current_user.email = form.email.data
            current_user.age = form.age.data
            if form.image.data:
                print("picture data")
                picture_file = save_pic(form.image.data)
                current_user.image = picture_file
                temp.image = picture_file
            temp.email = form.email.data
            temp.age = form.age.data
            temp.height = form.height.data
            temp.weight = form.weight.data
            temp.notes = form.notes.data
            db.session.commit()
            flash('Account updated!', 'success')
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.age.data = current_user.age
            form.height.data = Patient.query.filter_by(email=current_user.email).first().height
            form.weight.data = Patient.query.filter_by(email=current_user.email).first().weight
            form.notes.data = Patient.query.filter_by(email=current_user.email).first().notes
        elif form.validate():
            print(form.errors)
        image = url_for('static', filename='pictures/' + current_user.image)
        return render_template('patient-account.html', title='Account', image=image, form=form)
    else:
        form = UpdatePhysicianAccountForm()
        print("create physician account form")
        print(form.validate_on_submit())
        if form.validate_on_submit():
            temp = Physician.query.filter_by(email=current_user.email).first()
            current_user.email = form.email.data
            current_user.age = form.age.data
            if form.image.data:
                picture_file = save_pic(form.image.data)
                current_user.image = picture_file
                temp.image = picture_file
            print(temp)
            temp.email = form.email.data
            temp.age = form.age.data
            temp.specialty = form.specialty.data
            temp.school = form.school.data
            db.session.commit()
            flash('Account updated!', 'success') 
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.age.data = current_user.age
            form.specialty.data = Physician.query.filter_by(email=current_user.email).first().specialty
            form.school.data = Physician.query.filter_by(email=current_user.email).first().school
        image = url_for('static', filename='pictures/' + current_user.image)
        return render_template('physician-account.html', title='Account', image=image, form=form)

@app.route("/renderForm", methods=['POST'])
def renderForm():
    if request.method == "POST":
        fn = request.form['patient_first_name']
        ln = request.form['patient_last_name']
        em = request.form['patient_email']
        h = request.form['patient_height']
        w = request.form['patient_weight']
        a = request.form['patient_age']
        s = request.form['patient_sex']
        n = request.form['patient_notes']
        i = Patient.query.filter_by(email=em).first().image
        i = "static/pictures/"+ i
        print(i)
        pdfRender = render_template('pdfPrint.html',patient_first_name= fn,patient_last_name= ln,patient_email= em, patient_height= h,patient_weight= w,patient_age= a,patient_sex= s,patient_notes= n, image_ref= i)
        pdf = pdfkit.from_string(pdfRender, False)
        response = make_response(pdf)
 
        response.headers['Content-Type'] = "application/pdf"
        response.headers['Content-Disposition'] = 'attachment; filename='+ fn + ln + 'Report.pdf'
        print("PDF Should have loaded")
        return response



