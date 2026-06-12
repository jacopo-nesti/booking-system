from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.database import get_treatments, get_treatment_by_id, add_bookings, create_user, get_user_by_email, get_bookings_by_user, get_user_by_id, get_all_bookings, create_treatment, update_treatment, delete_treatment
from app.services import get_available_slots, get_filtered_bookings
from app.auth import (hash_password, verify_password, validate_password, validate_email)
from app.config import (PASSWORD_ERROR)
from app.helpers import login_required, admin_required

main = Blueprint('main', __name__)

# route
@main.route("/")
def home_page():
    return render_template("home.html")

@main.route("/contacts")
def contacts_page():
    return render_template("contacts.html")

@main.route("/selection")
def selection_page():
    treatments = get_treatments()
    return render_template("selection.html", treatments=treatments)

@main.route("/book", methods=["GET", "POST"])
@login_required
def book_page():
    if request.method == "POST":
        user_id = session.get("user_id")

        if not user_id:
            return redirect(url_for("main.login_page"))
        
        booking_date = request.form.get("booking_date")
        booking_time = request.form.get("booking_time")
        treatment_id = request.form.get("treatment_id")
        interaction_level = request.form.get("interaction_level")
        
        if not interaction_level:
            interaction_level = "non specificata"
        
        add_bookings(
            user_id, 
            booking_date, 
            booking_time, 
            treatment_id,
            interaction_level,
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
@login_required
def availability_redirect():
    booking_date = request.args.get("booking_date")
    treatment_id = request.args.get("treatment_id")

    return redirect(url_for(
        "main.availability",
        booking_date=booking_date,
        treatment_id=treatment_id
    ))

@main.route("/availability/<booking_date>/<int:treatment_id>")
@login_required
def availability(booking_date, treatment_id):
    slots = get_available_slots(booking_date, treatment_id)

    return render_template(
        "availability.html",
        slots=slots,
        booking_date=booking_date,
        treatment_id=treatment_id
        )

@main.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")

        form_data = {
            "name": name,
            "surname": surname,
            "email": email
        }
        
        if not validate_email(email):
            return render_template(
                "register.html",
                error="Email non valida - inserire una mail valida",
                form_data = form_data
            )
        
        if not validate_password(password):
            return render_template(
                "register.html",
                error=PASSWORD_ERROR,
                form_data = form_data
            )
        
        if get_user_by_email(email):
            return render_template(
                "register.html",
                error="Email già registrata - mi dispiace",
                form_data = form_data
            )
        
        password_hash = hash_password(password)

        create_user(
            name,
            surname,
            email,
            password_hash
        )

        return redirect(url_for("main.login_page"))

    return render_template("register.html", form_data={}) 

@main.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")

        if not email or not password:
            return render_template(
                "login.html", 
                error="Compila tutti i campi",
                email=email
            )
        
        user = get_user_by_email(email)

        if not user:
            return render_template(
                "login.html",
                error="Dati non corretti",
                email=email
            )
        
        if not verify_password(password, user["password_hash"]):
            return render_template(
                "login.html",
                error="Dati non corretti",
                email=email
            )
        
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        session["name"] = user["name"]

        if remember:
            session.permanent = True
        else:
            session.permanent = False

        if user["role"] == "admin":
            return redirect(url_for("main.admin_dashboard"))
        else:
            return redirect(url_for("main.dashboard_page"))
        
    return render_template("login.html")

@main.route("/logout")
def logout_page():
    session.clear()
    return redirect("/")

@main.route("/dashboard")
@login_required
def dashboard_page():
    user_id = session["user_id"]

    user = get_user_by_id(user_id)
    bookings = get_bookings_by_user(user_id)
    
    return render_template(
        "dashboard.html",
        user=user,
        bookings=bookings
    )

@main.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    data_specifica = request.args.get('data_specifica')
    id_trattamento = request.args.get('id_trattamento')
    data_inizio = request.args.get('data_inizio')
    data_fine = request.args.get('data_fine')

    questa_settimana = request.args.get('questa_settimana') == '1'
    questo_mese = request.args.get('questo_mese') == '1'
    piu_recente = request.args.get('piu_recente') == '1'

    filters = {
        'order_by_specific_date': data_specifica if data_specifica else None,
        'order_for_this_week': questa_settimana,
        'order_for_this_month': questo_mese,
        'filter_by_treatment': id_trattamento if id_trattamento else None,
        'order_from_most_recent': piu_recente,
        'order_from_range': [data_inizio, data_fine] if (data_inizio and data_fine) else None,
    }

    bookings = get_filtered_bookings(filters)

    return render_template(
        "admin_dashboard.html",
        bookings=bookings
        )

@main.route("/admin/treatments")
@admin_required
def admin_treatments():
    treatments = get_treatments()

    return render_template(
        "admin_treatments.html",
        treatments=treatments
        )

@main.route("/admin/treatments/create", methods=["GET", "POST"])
@admin_required
def create_treatment_page():
    if request.method == "POST":
        service_name = request.form.get("service_name")
        duration_min = int(request.form.get("duration_min"))
        price = float(request.form.get("price"))
        category = request.form.get("category")

        create_treatment(
            service_name,
            duration_min,
            price,
            category
        )

        return redirect(url_for("main.admin_treatments"))
    
    return render_template("create_treatment.html")

@main.route("/admin/treatments/edit/<int:treatment_id>", methods=["GET", "POST"])
@admin_required
def edit_treatment_page(treatment_id):
    if request.method == "GET":
        treatment = get_treatment_by_id(treatment_id)

        return render_template(
            "edit_treatment.html",
            treatment=treatment
        )
    
    if request.method == "POST":
        service_name = request.form.get("service_name")
        duration_min = int(request.form.get("duration_min"))
        price = float(request.form.get("price"))
        category = request.form.get("category")

        update_treatment(
            treatment_id,
            service_name,
            duration_min,
            price,
            category
        )
        return redirect(url_for("main.admin_treatments"))
    
@main.route("/admin/treatments/delete/<int:treatment_id>", methods=["POST"])
@admin_required
def delete_treatment_page(treatment_id):
    
    if delete_treatment(treatment_id):
        flash(f"Trattamento eliminato con successo!", "success")
    else:
        flash(f"Impossibile eliminare il trattamento: ci sono prenotazione attive associate a questo ID!", "danger")

    return redirect("/admin/treatments")