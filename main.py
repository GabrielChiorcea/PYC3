from flask import Flask, jsonify, request, render_template
from Clasess import RespondGet, ResponseFill, Chart
from form import MyForm, SingUp
from flask_restful import Api
from flask_cors import CORS
import pandas as pd
import pandas as pd

app = Flask(__name__)

CORS(app)

api = Api(app) 

excel_df = None
app.config['SECRET_KEY'] = 'secret_key_here'




@app.route('/login', methods=['GET', 'POST'])
def log():
    form = MyForm()
    text = 'login.html'
    if form.validate_on_submit():
        name = form.name.data
        prename = form.prename.data
        print(f"Name: {name} , PreName: {prename}")
        text = 'user.html'
    return render_template(text, form = form)



@app.route('/sing-up', methods=['GET', 'POST'])
def sing():
    form = SingUp()

    if form.validate_on_submit():
        name = form.name.data
        prename = form.prename.data
        print(f"Name: {name} , PreName: {prename}")
    return render_template('sing-up.html', title='sign-up', form=form)






@app.route('/', methods = ['GET'])
def frontpage():
    return render_template('index.html', title='home')

@app.route('/login', methods = ['GET'])
def logpage():
    return render_template('login.html', title='login')

@app.route('/sing-up', methods = ['GET'])
def singpage():
    return render_template('sing-up.html', title='sing-up')





@app.route('/excel', methods = ['POST'])
def upload_excel():
    global excel_df

    if 'file' not in request.files:
        return jsonify({'res' : 'Empty folder'}), 400
    file_in = request.files['file']

    if file_in.filename == '':
        return jsonify({'res': "Name of the file is empty" }), 400

    try:
        excel_df = pd.read_excel(file_in)
        return jsonify({'res' : 'File is uploaded'}), 200
    except Exception as e:
        return jsonify({'res' : f'Error on processing the file, details: {str(e)}'}), 500


@app.route('/<string:para>', methods=['GET'])
def get(para):
        isntance_of_class = RespondGet(excel_df)
        isntance_of_fill = ResponseFill(excel_df)

        if(para == "Count null value"): 
            count = isntance_of_class.resp_get_null()
            return count
        if(para == "Extract value"):
            ex_val = isntance_of_class.resp_get_ex_val()
            return ex_val
        if(para == "Excel summary"):
            sumar = isntance_of_class.resp_get_ex_sumar()
            return sumar
        if(para == 'fill NAN W 0'):
            fill_na = isntance_of_fill.fill_na() 
            return fill_na
        if(para == 'Chart'):
            chart = isntance_of_class.chart_columns()
            return chart
        else:
         return  jsonify({'val' : "no such qustion"}), 400


@app.route('/chart', methods = ['POST'] )
def generare_grafic():
    data = request.get_json()
    isntance_of_class = Chart(excel_df)
    chart = isntance_of_class.generare_grafic(data)
    return chart
   



if __name__ == "__main__":
    app.run(  port=5000)