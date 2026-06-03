from flask import Blueprint, render_template, request, redirect
from app.database import get_treatments, get_treatment_by_id, add_bookings
from app.services import get_available_slots

main = Blueprint('main', __name__)

# route
@main.route("/")
def home_page():
    return render_template("home.html")

@main.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@main.route("/contacts")
def contacts_page():
    return render_template("contacts.html")

@main.route("/selection")
def selection_page():
    treatments = get_treatments()
    return render_template("selection.html", treatments=treatments)

@main.route("/book", methods=["GET", "POST"])
def book_page():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        booking_date = request.form.get("booking_date")
        booking_time = request.form.get("booking_time")
        treatment_id = request.form.get("treatment_id")
        interaction_level = request.form.get("interaction_level")

        if not interaction_level:
            return render_template("book.html", error="Seleziona una preferenza di interazione.")
        
        add_bookings(
            name, 
            surname, 
            email, 
            booking_date, 
            booking_time, 
            treatment_id,
            interaction_level
        )
        return render_template("success.html")
    
    booking_date = request.args.get("booking_date")
    booking_time = request.args.get("booking_time")
    treatment_id = request.args.get("treatment_id")

    treatment = get_treatment_by_id(treatment_id)

    return render_template(
        "book.html",
        booking_date=booking_date,
        booking_time=booking_time,
        treatment=treatment,
        treatment_id=treatment_id,
    )

@main.route("/availability")
def availability_redirect():
    booking_date = request.args.get("booking_date")
    treatment_id = request.args.get("treatment_id")
    return redirect(f"/availability/{booking_date}/{treatment_id}")

@main.route("/availability/<booking_date>/<int:treatment_id>")
def availability(booking_date, treatment_id):
    slots = get_available_slots(booking_date, treatment_id)

    return render_template(
        "availability.html",
        slots=slots,
        booking_date=booking_date,
        treatment_id=treatment_id
        )