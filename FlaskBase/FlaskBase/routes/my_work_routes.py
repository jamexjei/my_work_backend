from FlaskBase import api
from FlaskBase.controllers import my_work_controller

api.add_resource(my_work_controller.JsonToExcel,"/api/myWork/jsonToExcel")
api.add_resource(my_work_controller.PixelImage,"/api/myWork/pixelImage")