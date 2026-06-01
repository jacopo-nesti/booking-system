from flask import Blueprint, render_template, request
from app.database import get_treatments, get_treatment_by_id, add_bookings

main = Blueprint('main', __name__)

# route
@main.route("/")
def home_page():
    treatments = get_treatments()
    return render_template("index.html", treatments=treatments)

@main.route("/availability/<int:treatment_id>")
def availability_page(treatment_id):
    treatment = get_treatment_by_id(treatment_id)
    if not treatment:
        return "Trattamento non trovato", 404
    return render_template("availability.html", treatment=treatment)

@main.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]
    booking_date = request.form["booking_date"]
    booking_time = request.form["booking_time"]
    treatment_id = request.form["treatment_id"]
    add_bookings(name, surname, email, booking_date, booking_time, treatment_id)
    return "Prenotazione salvata con successo! A presto!"