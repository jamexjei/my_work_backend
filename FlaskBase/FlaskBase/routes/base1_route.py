from FlaskBase import api
from FlaskBase.controllers import base1


api.add_resource(base1.base_prueba , "/api/prueba")
