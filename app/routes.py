from flask import Blueprint, render_template
from app.database import get_treatments

main = Blueprint('main', __name__)

# route
@main.route("/")
def home_page():
    treatments = get_treatments()
    return render_template("index.html", treatments=treatments)