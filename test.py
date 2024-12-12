from flask import Flask, jsonify, request, render_template, session, redirect
from excel import RespondGet, ResponseFill, Chart
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
from sqlinterogate import  db, UserEnter, ErrorLog
from flask_cors import CORS
from helpers import SelfApi
import pandas as pd
from datetime import datetime
from sqlinterogate import Identification, User
from urllib.parse import quote



# start configuration
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pydbsuperuser:Eva1Japo2@89.39.209.15:3306/pydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
api = Api(app)
db.init_app(app)
csrf = CSRFProtect(app)
# end configuration

# Global
excel_df_key = 'excel_df'
#excel_df = None
api_id = None
# end


# USER ENTER 
@app.route('/create-account', methods=['GET', 'POST'])
def start():
    isntance_of_class = UserEnter()
    return isntance_of_class.create()

@app.route('/sing-up', methods=['GET', 'POST'])
def sing():
    isntance_of_class = UserEnter()
    return isntance_of_class.sing()

@app.route('/user', methods = ['GET', 'POST'] )
def user_page():
    isinstance_of_class = UserEnter()
    return isinstance_of_class.user_page()

@app.route('/logout')
def logout():
    isinstance_of_class = UserEnter()
    return isinstance_of_class.logout()
# USER OUT


# NAV BAR ROOT
@app.route('/', methods = ['GET'])
def frontpage():
    return render_template('index.html', title='home')

@app.route('/create-account', methods = ['GET'])
def logpage():
    return render_template('create.html', title='Create account')

@app.route('/sing-up', methods = ['GET'])
def singpage():
    return render_template('sing-up.html', title='sing-up')
# END OF NAV BAR



# start, validation of excel
@app.route('/excel', methods=['POST'])
@csrf.exempt
def upload_excel():
    #global excel_df

    try:
        print(request.files)  # Afișați detaliile cererii în consolă
        if 'file' not in request.files:
            return jsonify({'res': 'Empty folder'}), 400

        file_in = request.files['file']

        if file_in.filename == '':
            return jsonify({'res': 'Name of the file is empty'}), 400

        print(f'File received: {file_in.filename}')
        excel_df = pd.read_excel(file_in)
        session[excel_df_key] = excel_df
        return jsonify({'res': 'File is uploaded'}), 200

    except Exception as e:
        print(e)  # Afișați detaliile erorii în consolă
        return jsonify({'res': f'Error on processing the file, details: {str(e)}'}), 500

# start the interogate
@app.route('/give_api')
def give_api():
    isinstance_of_class = SelfApi()
    return isinstance_of_class.give_api()


@app.route('/<string:para>/<string:ident>', methods=['GET'])
def get_with_ident(para, ident):
    excel_df = session.get(excel_df_key)
    identificare = quote(ident)

    isntance_of_class = RespondGet(excel_df)
    isntance_of_fill = ResponseFill(excel_df)
    exist = User.query.filter_by(identification=identificare).first()
    identt = Identification.query.filter_by(identification=identificare).first()

    if(exist != None  and identt != None):
            if para == "CountNullValue":
                count = isntance_of_class.resp_get_null()
                return count
            elif para == "ExtractValue":
                ex_val = isntance_of_class.resp_get_ex_val()
                return ex_val
            elif para == "ExcelSummary":
                sumar = isntance_of_class.resp_get_ex_sumar()
                return sumar
            elif para == 'fillNANW0':
                fill_na = isntance_of_fill.fill_na()
                return fill_na
            elif para == 'Chart':
                chart = isntance_of_class.chart_columns()
                return chart
    elif(exist and identt == None):
        id = session.get('user_id')
        time = datetime.now()
        user = User.query.filter_by(id=id).first()
        ident = Identification(timestamp=time, identification=user.identification)
        db.session.add(ident)
        db.session.commit()
        if para == "CountNullValue":
            count = isntance_of_class.resp_get_null()
            return count
        elif para == "ExtractValue":
            ex_val = isntance_of_class.resp_get_ex_val()
            return ex_val
        elif para == "ExcelSummary":
            sumar = isntance_of_class.resp_get_ex_sumar()
            return sumar
        elif para == 'fillNANW0':
            fill_na = isntance_of_fill.fill_na()
            return fill_na
        elif para == 'Chart':
            chart = isntance_of_class.chart_columns()
            return chart
    else:
        return jsonify({'val': "no such question"}), 400



@app.route('/chart', methods = ['POST'] )
@csrf.exempt
def generare_grafic():
    excel_df = session.get(excel_df_key)
    data = request.get_json()
    isntance_of_class = Chart(excel_df)
    chart = isntance_of_class.generare_grafic_to_send(data)
    return chart
# end interogate

# @app.errorhandler(Exception)
# def handle_error(e):
#     isinstance_of_class = ErrorLog()
#     isinstance_of_class.insertError(e)
    

@app.route('/errors', methods = ['GET'])
def errors():
    if not session.get('logged_in'):
        return redirect('/')
    else:
        isinstance_of_class = ErrorLog()
        return isinstance_of_class.error()




if __name__ == '__main__':
    app.run( debug= True)