from flask import Flask, request,send_file
from flask_restful import Api, Resource, reqparse
import json
import pandas as pd
from io import BytesIO
import random,werkzeug
parser = reqparse.RequestParser()

parser.add_argument('json_data',type=str,location="form")
parser.add_argument('nombre_archivo',type=str,location="form")
parser.add_argument('data', type=werkzeug.FileStorage, location='files')

class JsonToExcel(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            obj_json =args['json_data']
            obj_nombre=args['nombre_archivo']
            
            if not obj_nombre:
                obj_nombre='generic_name'
            if not obj_json:
                raise ValueError(f"por favor ingrese un texto formato json")
                    
            obj_json=json.loads(obj_json)
            df = pd.DataFrame(obj_json)
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)
            return send_file(excel_file, download_name=f'{obj_nombre}.xlsx', as_attachment=True)         
        except Exception as e:
            raise ValueError(f"ha ocurrido una excepcion causa:{e} ")