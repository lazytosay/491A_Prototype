#api relate to general information
from flask import Blueprint
import time


main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def index():
    #FIXME: for now
    return {'message': 'this is index page'}


@main_bp.route("/time")
def getTime():
    return {'time': time.time()}

