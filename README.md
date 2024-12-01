# PYC3



## Arhitecture.

This application serves as a backend capable of processing and reading data from Excel files. To utilize this backend and connect it to a frontend, a user account is required. The account is essential as it provides a unique API key for authentication and authorization.

Excel files are read using Pandas, which converts the file content into a DataFrame. Once transformed into a DataFrame, the data is further converted into JSON format based on the specific functions or filters requested. This enables dynamic and customizable data extraction from the Excel file.

The Excel file itself is stored in the database as a binary large object (BLOB), ensuring secure and efficient storage


## Get and store the excel file

The Excel file is uploaded via the /excel endpoint of the API. At this endpoint, the file undergoes validation to ensure it is an Excel file, even if the frontend does not perform this check. Once validated, the file is renamed for consistency and security.

The renaming process involves appending a unique ID, derived from the user’s API key, to the file name. The resulting format is {ID}.xlsx. The renamed file is then securely stored in the database as a BLOB with its new identifier, ensuring traceability and efficient management.

```python
@app.route('/excel', methods=['POST'])
@csrf.exempt
def upload_excel():
    try:
        # Check if a file is present in the request
        if 'file' not in request.files:
            return jsonify({'res': 'No file found in the request'}), 400
        
        file_in = request.files['file']
        id = request.args.get('id')

        # Validate the user ID parameter
        if not id:
            return jsonify({'res': 'Missing user ID'}), 400

        # Check if the file name is empty
        if file_in.filename == '':
            return jsonify({'res': 'File name is empty'}), 400

        # Validate the file extension (only .xlsx and .xls are allowed)
        if not (file_in.filename.endswith('.xlsx') or file_in.filename.endswith('.xls')):
            return jsonify({'res': 'Invalid file type, only Excel files are allowed (.xlsx, .xls)'}), 400

        file_content = file_in.read()
        
        # Ensure the file is not empty
        if not file_content:
            return jsonify({'res': 'Uploaded file is empty'}), 400

        # Generate a unique name for the file based on the user ID
        file_name = f"{id}.xlsx"

        # Create a new database record for the Excel file
        new_excel_file = Excel(name=file_name, excel=file_content)

        # Add the file to the database session and commit
        db.session.add(new_excel_file)
        db.session.commit()

        return jsonify({'res': 'File uploaded successfully'}), 200

    except Exception as e:
        # Roll back the database transaction in case of an error
        db.session.rollback()
        print(f"Error: {e}")  # Log the error details to the console
        return jsonify({'res': f'An error occurred while processing the file: {str(e)}'}), 500

```



## How the backend know what data to give you

The below API endpoint, accessible via /<string:para>/<string:ident> with a GET request, dynamically processes Excel files stored in a database. It retrieves the file based on an id query parameter, reads it into a Pandas DataFrame, and executes specific functions depending on the para value (e.g., counting null values, extracting data, summarizing content, filling missing values, or generating charts). The user's existence and identification (ident) are validated against the database, and if necessary, new identification records are created. By utilizing specialized classes (RespondGet and ResponseFill), the endpoint ensures modular and efficient data manipulation while maintaining robust error handling and database consistency.



```python
@app.route('/<string:para>/<string:ident>', methods=['GET'])
@csrf.exempt
def get_with_ident(para, ident):
    identificare = quote(ident)
    id = request.args.get('id')
    filename = str(id)+'.xlsx'
    retrieved_excel_file = Excel.query.filter_by(name=filename).first()
    excel_data = retrieved_excel_file.excel
    excel_df = pd.read_excel(io.BytesIO(excel_data))
    isntance_of_class = RespondGet(excel_df, id)
    isntance_of_fill = ResponseFill(excel_df, id)
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

        time = datetime.now()
        ident = Identification(timestamp=time, identification= identificare)
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
        return jsonify({'val': exist}), 400
```




