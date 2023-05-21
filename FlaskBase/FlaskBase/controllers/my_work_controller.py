from flask import Flask, request,send_file
from flask_restful import Api, Resource, reqparse
import json
import pandas as pd
from io import BytesIO
import random,werkzeug
import argparse
from werkzeug.datastructures import FileStorage
from PIL import Image
import tempfile
from functools import reduce
parser = reqparse.RequestParser()

parser.add_argument('data', type=FileStorage, location='files')
#parser.add_argument('file_data', type=FileStorage)
parser.add_argument('json_data',type=str,location="form")
parser.add_argument('nombre_archivo',type=str,location="form")
parser.add_argument('ancho_pixel',type=int,location="form")


#functions
def leer_archivo(archivo):
    contenido = archivo.read()
    archivo.close()
    return contenido



#classes

class JsonToExcel(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            obj_json =args['json_data']
            obj_nombre=args['nombre_archivo']
            obj_file=args['data']
            
            if obj_json:
                obj_json=json.loads(obj_json)
            if obj_file:
                try:
                    obj_json=leer_archivo(obj_file)
                    obj_json=obj_json.decode('utf-8')
                    obj_json=obj_json.replace("\r","")
                    obj_json=obj_json.replace("\n","")
                    obj_json=json.loads(obj_json)
                except Exception as e:
                    raise ValueError(f"el archivo json no tiene un formato legible ")    
            if not obj_nombre:
                obj_nombre='generic_name'
            df = pd.DataFrame(obj_json)
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)
            return send_file(excel_file, download_name=f'{obj_nombre}.xlsx', as_attachment=True)         
        except Exception as e:
            raise ValueError(f"ha ocurrido una excepcion causa:{e} ")
        
        
        
class PixelImage(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            obj_file=args['data']
            obj_ancho_pixel=args['ancho_pixel']
            if not obj_file:
                raise ValueError("no se envio ningun archivo")
            obj_image=leer_archivo(obj_file)
            image=Image.open(BytesIO(obj_image))
            ancho, alto = image.size
            bloques_ancho = ancho // obj_ancho_pixel
            bloques_alto = alto // obj_ancho_pixel
            imagen_pixelada = Image.new('RGB', (bloques_ancho, bloques_alto))
            for i in range(bloques_ancho):
                for j in range(bloques_alto):
                    bloque = image.crop((i * obj_ancho_pixel, j * obj_ancho_pixel, (i + 1) * obj_ancho_pixel, (j + 1) * obj_ancho_pixel))
                    promedio_color = reduce(
                        lambda x, y: (
                            x[0] + y[0],
                            x[1] + y[1],
                            x[2] + y[2]
                        ),
                        bloque.getdata()
                    )
                    promedio_color = (promedio_color[0] // (obj_ancho_pixel * obj_ancho_pixel), promedio_color[1] // (obj_ancho_pixel * obj_ancho_pixel), promedio_color[2] // (obj_ancho_pixel * obj_ancho_pixel))
                    for x in range(obj_ancho_pixel):
                        for y in range(obj_ancho_pixel):
                            imagen_pixelada.putpixel((i, j), promedio_color)
            with tempfile.NamedTemporaryFile(delete=True,suffix=".png") as temp_file:
                imagen_pixelada.save(temp_file.name)   
            return send_file( temp_file.name ,mimetype='image/png',  attachment_filename='imagen_pixelada.png',as_attachment=True)
        except Exception as e:
            raise ValueError(f"ha ocurrido una excepcion causa:{e} ")
                    