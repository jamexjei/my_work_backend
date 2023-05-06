import os
from flask import Flask
#from flask_marshmallow import Marshmallow
from flask_restful import Api
#from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import app_config

app = Flask(__name__) 
#Api Resources / Marshmallow serialization para SQLAlchemy
api = Api(app)
#ma = Marshmallow(app)
#DB init
config_name = os.getenv('FLASK_ENV')
app.config.from_object(app_config[config_name])

db = SQLAlchemy(app)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})

from FlaskBase.routes import base1_route,my_work_routes

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()
