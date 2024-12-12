from flask import session, jsonify
from datetime import datetime
from sqlinterogate import User
from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

class SelfApi():
    def give_api(self):    
        try:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            result = {'message': "https://excelstore.gabrielchiorcea.tech/" + "/metoda/" + user.identification}
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})

    

