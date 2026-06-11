# Regole del sistema
# - Apertura: 09:00 - 18:00
# - Pausa pranzo: 13:00 - 14:00
# - Chiuso: domenica e lunedì
# - Ogni trattamento ha una durata
# - Un appuntamento occupa il tempo necessario alla sua durata

# Gestione prenotazioni - Algoritmo semplificato:
# 1. Provo uno start_time (es. 09:00)
# 2. Calcolo: end_time = start_time + durata
# 3. Controllo 3 cose:
#    A. Superare orario chiusura? Se si --> non prenotabile
#    B. Entra nella pausa pranzo? Se si --> non prenotabile
#    C. Collide con prenotazioni esistenti? Se si --> non prenotabile
#     - In questo caso devo verificare: start < existing_end AND end > existing_start

from datetime import datetime, timedelta, date
from app.config import (OPENING_TIME, CLOSING_TIME, LUNCH_START, LUNCH_END, SLOT_DURATION, CLOSED_DAYS)
from app.database import get_bookings_by_date, get_treatment_by_id, execute_query

# controlla se il salone è aperto in una determinata data
def is_business_open(booking_date):
    selected_date = datetime.strptime(booking_date, "%Y-%m-%d")
    # blocco date passate
    if selected_date.date() < date.today():
        return False
    # blocco le date che vanno nei giorni di chisura
    if selected_date.weekday() in CLOSED_DAYS:   # weekday(): 0 = lunedì, 6 = domenica
        return False
    return True


# genera tutti gli slot teorici della giornata (senza considerare prenotazioni o durata trattamenti)
def generate_daily_slots():
    slots = []

    start = datetime.strptime(OPENING_TIME, "%H:%M")
    end = datetime.strptime(CLOSING_TIME, "%H:%M")

    current = start

    while current + timedelta(minutes=SLOT_DURATION) <= end:  # continua finché il prossimo slot NON supera l’orario di chiusura
        slots.append(current.strftime("%H:%M"))  # aggiungi l’orario alla lista
        current += timedelta(minutes=SLOT_DURATION)  # vai avanti di 30 minuti
    return slots


# controlla se un orario cade nella pausa pranzo
def lunch_break(booking_time):
    time = datetime.strptime(booking_time, "%H:%M").time()
    lunch_start = datetime.strptime(LUNCH_START, "%H:%M").time()
    lunch_end = datetime.strptime(LUNCH_END, "%H:%M").time()
    return lunch_start <= time < lunch_end


# recupera la durata del trattamento dal database
def get_treatment_duration(treatment_id):
    treatment = get_treatment_by_id(treatment_id)
    # se il trattamento esiste ritorna la durata, altrimenti 0
    return treatment["duration_min"] if treatment else 0


# Verifica se uno slot è valido per un certo trattamento. Controlla:
    # - non supera orario di chiusura
    # - non si sovrappone alla pausa pranzo
def is_slot_valid(slot_time, duration):
    slot_start = datetime.strptime(slot_time, "%H:%M")
    end_time = slot_start + timedelta(minutes=duration)

    lunch_start = datetime.strptime(LUNCH_START, "%H:%M")
    lunch_end = datetime.strptime(LUNCH_END, "%H:%M")

    closing_time = datetime.strptime(CLOSING_TIME, "%H:%M")

    # 1. supera chiusura
    if end_time > closing_time:
        return False
    
    # 2. entra nella pausa pranzo
    if slot_start < lunch_end and end_time > lunch_start:
        return False
    return True


# funzione overlap per evitare sovrapposizioni con orari già prenotati
def overlap_conflict(slot_start, slot_end, bookings):
    slot_start = datetime.strptime(slot_start, "%H:%M")
    slot_end = datetime.strptime(slot_end, "%H:%M")

    for b in bookings:
        b_start = datetime.strptime(b["booking_time"], "%H:%M")

        # ricavo la durata del trattamento
        duration = get_treatment_duration(b["treatment_id"])
        b_end = b_start + timedelta(minutes=duration)

        # overlap check
        if slot_start < b_end and slot_end > b_start:
            return True
        
    return False
    

# Genera tutti gli slot disponibili per una data e trattamento (filtra giorni chiusi e slot non validi)
def get_available_slots(booking_date, treatment_id):

        # funzione per verificare che le date non siano passate al giorno presente
    def is_past_date(booking_date):
        selected_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
        today = datetime.today().date()
        return selected_date < today

    # se il salone è chiuso → nessuno slot disponibile
    if not is_business_open(booking_date):
        return []

    # durata del trattamento selezionato
    duration = get_treatment_duration(treatment_id)
    bookings = get_bookings_by_date(booking_date)

    # tutti gli slot teorici della giornata
    slots = generate_daily_slots()
    valid_slots = []

    # filtra solo gli slot validi
    for slot in slots:

        slot_start = datetime.strptime(slot, "%H:%M")
        slot_end = slot_start + timedelta(minutes=duration)

        # regola base
        if not is_slot_valid(slot, duration):
            continue

        # conflitti DB
        if overlap_conflict(slot, slot_end.strftime("%H:%M"), bookings):
            continue
            
        valid_slots.append(slot)

    return valid_slots


def get_filtered_bookings(filters):
    query = """
        SELECT
            bookings.id,
            bookings.user_id,
            bookings.booking_date,
            bookings.booking_time,
            bookings.treatment_id,
            bookings.interaction_level,
            users.name,
            users.surname,
            users.email
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN treatments ON bookings.treatment_id = treatments.id
        WHERE 1=1"""

    params = []

    # 1. Data specifica
    if filters.get('order_by_specific_date'):
        query += " AND bookings.booking_date = ?"
        params.append(filters['order_by_specific_date'])

    # 2. Questa settimana
    if filters.get('order_for_this_week'):
        query += " AND strftime('%Y-%W', bookings.booking_date) = strftime('%Y-%W', 'now')"

    # 3. Questo mese
    if filters.get('order_for_this_month'):
        query += " AND strftime('%Y-%m', bookings.booking_date) = strftime('%Y-%m', 'now')"

    # 4. Date range
    if filters.get('order_from_range'):
        query += " AND bookings.booking_date BETWEEN ? AND ?"
        params.append(filters['order_from_range'][0])
        params.append(filters['order_from_range'][1])

    # 5. Filtro per trattamento
    if filters.get('filter_by_treatment'):
        query += " AND bookings.treatment_id = ?"
        params.append(filters['filter_by_treatment'])

    # 6. Ordinamento più recente
    if filters.get('order_from_most_recent'):
        query += " ORDER BY bookings.booking_date DESC"

    return execute_query(query, params)