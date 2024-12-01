import pandas as pd
from flask import  jsonify, request, send_file
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

matplotlib.use('Agg')


class ExcelReader:
    def __init__(self, file_path, id):
        self.df = file_path
        self.id = id



class RespondGet(ExcelReader):
    def __init__(self, file_path, id):
      super().__init__(file_path, id)
        
    def resp_get_null(self):
        try:
          df = self.df
          ex = df.isna().sum().sum()
          ex_str = str(ex)
          return jsonify({'sessionID' : str(self.id), "value" : str(ex_str)}), 200
        except Exception as e:
          return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    def resp_get_ex_val(self):
        try:
          df = self.df
          col= df.columns
          col_nr = len(col)
          random_number = random.randint(0, col_nr - 1)
          col_name = col[random_number]
          col_name_data = df.loc[:,col_name]
          row_value = random.choice(col_name_data)

          if isinstance(row_value, str):
              inde_str = df[df[col_name] == row_value].index
              inde_list_str = inde_str.tolist()
              inde_list_concat_str = ', '.join(map(str, inde_list_str))
              dat = [inde_list_concat_str, col_name, row_value]
          elif pd.isnull(row_value):
              nan_indexes = df.index[df[col_name].isna()]
              nan_list = nan_indexes.tolist()
              nan_list_concat = ', '.join(map(str, nan_list))
              dat = [nan_list_concat, col_name, "empty cell"]
          else:
              inde = df[df[col_name] == row_value].index
              inde_list = inde.tolist()
              inde_list_concat = ', '.join(map(str, inde_list))
              dat = [inde_list_concat, col_name, round(row_value, 1)]

          return jsonify({'sessionID' : str(self.id),
                        'value' : str(dat[2]), 
                        'columns' : str(dat[1]), 
                         "row" : str(dat[0])}), 200

        except Exception as e:
          return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    def resp_get_ex_sumar(self):
         try:
          df = self.df

          col = df.columns
          value_old = []
          value = []
          col_dtypes = []
          data_types = df.dtypes

          for ma in col:
            col_name = pd.to_numeric(df[ma], errors='coerce').max()
            value_old.append(col_name)


          for col_name, col_dtype in data_types.items():
            if col_dtype == 'object':
             like = 'string'
             col_dtypes.append([col_name , str(like)])
            else:
             like = col_dtype
             col_dtypes.append([col_name , str(like)])
      

          value_new = [value for value in value_old if not math.isnan(value)]  

          for val in value_new:
            if isinstance(val, np.int64):
             value.append(int(val))
            elif isinstance(val, float):
             value.append(round(val, 1))

          rows, columns = df.shape        
          sort = sorted(value)

          return jsonify({'sessionID' : str(self.id),
                          "col_dtypes": col_dtypes,
                          "rows": rows,
          "columns": columns,
          "max_value": str(sort[-1]),
          "min_value": str(sort[0]) }), 200
         except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    
    def chart_columns(self):
      try:
        df = self.df
        columns = df.columns.tolist()
        return jsonify({'sessionID' : str(self.id), "value" : columns}), 200
      except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



class ResponseFill( ExcelReader):
    def __init__(self, file_path, id):
      super().__init__(file_path , id)

    @staticmethod
    def highlight_null(val):
         try:
          if pd.isna(val):
            val= 0
            modify = 'modified'
          else:
            modify = 'no modified'
          return val, modify
         except Exception as e:
          return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def fill_na(self):
       try:   
        df = self.df
        id = self.id
        data = []
        for column in df:
          for index, val in df[column].items():
              val, modify = ResponseFill.highlight_null(val)
              data.append([column, val, modify])

          for loc in data:
            if isinstance(loc[1], pd.Timestamp):
             loc[1] = loc[1].strftime('%Y-%m-%d')

          result = {}
          for column, val, modify in data:
            if column not in result:
              result[column] = { 'column': column, 'arr': []}
          for column, val, modify in data:  
           result[column]['arr'].append({ 'sessionID' : str(self.id), 'value': val, 'status': modify})
        return result, 200
       except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500




class Chart( ExcelReader):
  def __init__(self, file_path, id):
    super().__init__(file_path, id)

  def generare_grafic_to_send(self, data):
    try:
        data = request.get_json()
        df = self.df
        columnxone = data.get('columnX1')
        columnxtow = data.get('columnX2')
        Y = data.get('Y')

        df = df.dropna(subset=[columnxone[0], columnxtow[0], Y])

        x1 = df[columnxone[0]]
        x2 = df[columnxtow[0]]
        y = df[Y]

        plt.figure(figsize=(10, 6))
        plt.bar(x1, y, width=0.7, label=columnxone[0], color=columnxone[1], align='center')
        plt.bar(x2, y, width=0.7, label=columnxtow[0], color=columnxtow[1], align='edge')

        plt.xlabel('Etichete')
        plt.legend()
        plt.xticks(rotation=90)

        # Salvează imaginea într-un obiect BytesIO în loc să o salvezi pe disc
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        # Returnează imaginea direct ca răspuns, fără a o salva pe disc
        return send_file(img_buf, mimetype='image/png'), 200
    except Exception as e:
        return jsonify({"error": f"A intervenit o eroare: {str(e)}"}), 500
