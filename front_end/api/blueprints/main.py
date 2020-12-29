#api relate to general information
from flask import Blueprint, render_template
import time


main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template('main/site_landing_page.html')

"""
@main_bp.route("/")
def index():
    #FIXME: for now
    return {'message': 'this is index page'}
"""


@main_bp.route("/time")
def get_time():
    return {'time': time.time()}

