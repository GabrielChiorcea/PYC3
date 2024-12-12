from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, session, jsonify, flash
from wtforms.validators import ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from form import Create, SingUp
from datetime import datetime


db = SQLAlchemy()




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    identification = db.Column(db.String(120), nullable =False)

class UserErrorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    error_message = db.Column(db.String(255), nullable=False)  

class Identification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    identification = db.Column(db.String(255), nullable=False) 
    
class Excel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    excel = db.Column(LargeBinary)
    

class UserEnter():
    def create(self):
        form = Create()
        try:
         if form.validate_on_submit():
                current_datetime = datetime.now() 
                name = form.name.data
                password = form.password.data
                user_identification = name[:3] + str(current_datetime.day) + name[-3:] + str(current_datetime.month)
                user = User.query.filter_by(username=name).first()
                if (user): 
                    form.validate_username(True)
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new = User(username=name, password=hashed_password, identification=user_identification)
                db.session.add(new)
                db.session.commit()
                return redirect('sing-up')
        except ValidationError as e:
            flash('Acest user este folosit.')
            return render_template('create.html' , form=form)
        return render_template('create.html', form=form)
    
    def sing(self):
        form = SingUp()
        try:
            if form.validate_on_submit():
                name = form.name.data
                password = form.password.data
                user = User.query.filter_by(username=name).first()
                if user is not None and check_password_hash(user.password, password):
                    session['user_id'] = user.id # folosim coocke pentru a pastra o sesiune pentru a ramane logati 
                    session['logged_in'] = True
                    return redirect('/user')
                else:
                    form.validate_user(True)
        except ValidationError as e:
            flash("User sau parola incorecte")
        return render_template('sing-up.html', title='sign-up', form=form)
    
    def user_page(self): #daca dam refresh sa ramanem logati
        if not session.get('logged_in'):
            return redirect('/')
        return render_template('user.html')
    
    def logout(self):
        session.pop('user_id', None)
        session['logged_in'] = False  
        result = {'message': 'Nu asa se acceseaza aceasta resursa'}
        return jsonify(result)
    


class ErrorLog():
    
    def insertError(self, data):
        id = session.get('user_id')
        error_log = UserErrorLog( user_id = id , error_message=str(data))
        db.session.add(error_log)
        db.session.commit()

    def error(self):
        if not session.get('logged_in'):
           return redirect('/')
        else:
            id = session.get('user_id')
            errors = UserErrorLog.query.filter_by(user_id = id).all()
            messages = []
            for error in errors:
                message = {
                    'timestamp': error.timestamp,
                    'error_message': error.error_message
                }
                messages.append(message)
        return jsonify(messages)
