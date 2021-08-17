from flask import Flask

app = Flask(__name__)

from .GetProfile import GetProfile
from .EditProfile import EditProfile
from .GetJobCondition import GetJobCondition
from .EditJobCondition import EditJobCondition

app.register_blueprint(GetProfile.mod)
app.register_blueprint(EditProfile.mod)
app.register_blueprint(GetJobCondition.mod)
app.register_blueprint(EditJobCondition.mod)

