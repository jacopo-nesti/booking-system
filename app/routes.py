from flask import Blueprint, render_template
from app.database import get_treatments, get_treatment_by_id

main = Blueprint('main', __name__)

# route
@main.route("/")
def home_page():
    treatments = get_treatments()
    return render_template("index.html", treatments=treatments)

@main.route("/availability/<int:treatment_id>")
def availability_page(treatment_id):
    treatment = get_treatment_by_id(treatment_id)
    return render_template("availability.html", treatment=treatment)