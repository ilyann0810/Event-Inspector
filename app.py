from flask import Flask,render_template,request,flash,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
import sqlite3
import datetime

db = SQLAlchemy()

class profile(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    Phone_Number = db.Column(db.String(30))
    email = db.Column(db.String(30))
    description = db.Column(db.String(500))

class Case(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    events = db.relationship('Event', backref='Case', lazy=True)
    
    def __repr__(self):
        return f'<File {self.filename}>'
    

class Event(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(500))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'),nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    profile_name = db.Column(db.String(30))
    
    



def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static',)
    app.config['SECRET_KEY'] = 'dqzdqzd nftn'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

app =create_app()

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/event_manager.html' , methods=['GET','POST'])
def event_manager():
    
    if request.method =='POST':
        Case_Name = request.form.get('Case_Name')
        if Case_Name !=None:
            new_case = Case(name=Case_Name)
            db.session.add(new_case)
            db.session.commit()
        else:
            print("cancel")
        
        
    
    cases = Case.query.all()
    
    cases = [case  for case in cases]
    return render_template('event_manager.html',cases=cases)

@app.route('/Add customer.html', methods=['GET','POST'])
def Add_customer():
    data = request.form
    print(data)
    if request.method =='POST':
        Name = request.form.get('Name')
        Surname = request.form.get('Surname')
        Phone = request.form.get('Phone Number')
        Email = request.form.get('Email')
        Description = request.form.get('Description')
        
        new_profile = profile(name=Name,surname=Surname,
                            Phone_Number=Phone,email=Email,description=Description)
        db.session.add(new_profile)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('Add customer.html')

@app.route('/edit_customer.html')
def edit_customer():
    
    profiles = profile.query.all()
    profiles = [profile  for profile in profiles]
    return render_template('edit_customer.html',profiles=profiles)


@app.route('/<case_id>', methods=['GET','POST'])
def file_page(case_id):
   
    case = Case.query.get_or_404(case_id)
    profiles = profile.query.all()


    
    profiles = [profile  for profile in profiles]
    return render_template('file_page.html', case=case,profiles=profiles)




@app.route('/create_event/<case_id>', methods=['GET', 'POST'])
def create_event(case_id):
    if request.method == 'POST':
        name = request.form.get('Event_title')
        Description = request.form.get('Event_Description')
        profile_name = request.form.get('profile_name')
        timestamp_str = request.form.get('time')
        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
        new_Event= Event(name=name,description=Description,case_id=case_id,profile_name=profile_name,timestamp=timestamp)
        db.session.add(new_Event)
        db.session.commit()
           

    return redirect(url_for('file_page', case_id=case_id))
   


@app.route('/delete_event/<case_id>', methods=['GET', 'POST'])
def delete_event(case_id):
    if request.method == 'POST':
        event_id = request.form.get('Event_id')
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        print("event :",event_id)
    
    
    return redirect(url_for('file_page', case_id=case_id))


@app.route('/get_profiles')
def get_profiles():
    profiles = profile.query.all()
    profiles_data = [{'id': p.id, 'name': p.name, 'email': p.email,'surname' : p.surname,
                      'description' : p.description,'Phone_Number' : p.Phone_Number} for p in profiles]
    return jsonify(profiles_data)


@app.route('/update_profile', methods=['GET', 'POST'])

def update_profile():
    data = request.form
    print(data)
    if request.method == 'POST':
        profile_id = request.form['profile_id']
        user = profile.query.get(profile_id)
        user.name = request.form['Name']
        user.surname = request.form['Surname']
        user.description = request.form['Description']
        user.Phone_Number = request.form['Phone Number']
        user.email = request.form['Email']
    
        db.session.commit()
    
    return redirect(url_for('edit_customer'))