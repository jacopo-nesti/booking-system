# BOOKING SYSTEM – WEB APP PER PRENOTAZIONI

- L’app è un sistema di prenotazione appuntamenti per un’attività.
L’utente sceglie il trattamento, poi seleziona da un calendario una data e un orario disponibili (con durata variabile in base al servizio). Inserisce nome, cognome ed email per ricevere la conferma dell’appuntamento.

- È prevista anche un’area admin, accessibile solo al gestore, dove può vedere tutte le prenotazioni con i dettagli per organizzare il lavoro.

- Upgrade previsto:
Aggiunta di registrazione e login, così gli utenti possono accedere più velocemente senza reinserire ogni volta i dati.

---

## PAGINE

1. **index.html** --> Pagina pubblica per i clienti.
Funzionalità:
- visualizzazione trattamenti disponibili 
- selezione trattamento
- selezione giorno
- selezione orario disponibile
- inserimento:
    - nome
    - cognome 
    - email
- conferma prenotazione
- invio email di conferma 

2. **admin.html**--> Pagina riservata al gestore.
Funzionalità:
- visualizzare tutte le prenotazioni
- visualizzare:
    - nome cliente
    - cognome cliente
    - email cliente
    - trattamento scelto
    - data
    - orario
    - durata
- ordinamento per data e ora

Volendo, in una seconda fase:
- eliminare prenotazioni
- modificare prenotazioni

### Upgrade futuro pagine
3. Login.html (accesso utenti registrati)
4. Register.html (registrazione utenti)
5. dashboard.html (area personale clienti)

---

## Database

**Tabella trattamenti (servizi offerti)**

| Campo  | Tipo       |      
| ------ | ---------- |
| id     | INTEGER PK |
| nome   | TEXT       |
| durata | INTEGER    |         

Esempio

| id | nome        | durata |
| -- | ----------- | ------ |
| 1  | Taglio uomo | 30     |
| 2  | Consulenza  | 60     |
| 3  | Colorazione | 120    |

**Tabella prenotazioni (tabella principale del progetto)**

| Campo          | Tipo       |
| -------------- | ---------- |
| id             | INTEGER PK |
| nome           | TEXT       |
| cognome        | TEXT       |
| email          | TEXT       |
| data           | DATE       |
| ora            | TIME       |
| trattamento_id | INTEGER FK |

Esempio

| id | nome  | cognome | email                                   | data       | ora   | trattamento_id |
| -- | ----- | ------- | --------------------------------------- | ---------- | ----- | -------------- |
| 1  | Mario | Rossi   | [mario@email.it](mailto:mario@email.it) | 2026-06-15 | 09:00 | 3              |

### Upgrade futuro database
Tabella utenti (da fare quando implemento login e registrazione con Flask-Login)

| Campo         | Tipo        |
| ------------- | ----------- |
| id            | INTEGER PK  |
| nome          | TEXT        |
| cognome       | TEXT        |
| email         | TEXT UNIQUE |
| password_hash | TEXT        |

---

## Regole del sistema (importanti per gestione prenotazioni)

- Apertura: 09:00 - 18:00
- Pausa pranzo: 13:00 - 14:00
- Chiuso: domenica e lunedì
- Ogni trattamento ha una durata
- Un appuntamento occupa il tempo necessario alla sua durata

---

## Gestione prenotazioni

Algoritmo semplificato:
1. Provo uno start_time (es. 09:00)
2. Calcolo: end_time = start_time + durata
3. Controllo 3 cose:
   A. Superare orario chiusura? Se si --> non prenotabile
   B. Entra nella pausa pranzo? Se si --> non prenotabile
   C. Collide con prenotazioni esistenti? Se si --> non prenotabile
    - In questo caso devo verificare: start < existing_end AND end > existing_start

---

## Problema della sovrapposizione

Definizione di slot valido:
- controllo che non si sovrapponga a prenotazioni esistenti
- rispetto durata trattamento
- rispetto pausa pranzo
- rispetto orario apertura/chiusura

* Ogni prenotazione deve essere vista come start_time --> end_time (intervallo di tempo è fondamentale per evitare sovrapposizioni). end_time = start_time + durata trattamento.

---

## Time slot

Uso slot dinamici
- utente sceglie un orario
- il backend verifica se la durata entra

---

## Note importanti

* admin.html è protetta da password: login admin tramite sessione flask, logout
* Conflitto possibile --> due utenti prenotato lo stesso slot contemporaneamente (soluzione --> controllo disponibilità prima del salvataggio);
* Validazione input --> email valida, campi non vuoti, data futura (no prenotazione nel passato), orari validi (non 03:00 di notte);
* UX calendario --> utente sceglie trattamento, backend calcola gli slot disponibili nel giorno selezionato, frontend mostra solo slot validi;

---

## Struttura backend

- Flask per le routes
- Logic per il calcolo disponibilità
- Database access

---

## Flusso di prenotazione

1. Utente seleziona un trattamento
2. Il sistema recupera la durata del trattamento dal database
3. Il sistema mostra il calendario
4. L'utente seleziona un giorno
5. Il sistema recupera tutte le prenotazioni già presenti per quel giorno
6. Il sistema genera tutti i possibili orari prenotabili rispettando:
   - apertura 09:00-18:00
   - pausa 13:00-14:00
   - durata del trattamento
   - nessuna sovrapposizione con prenotazioni esistenti
7. Il sistema mostra soltanto gli orari validi.
8. L'utente seleziona un orario.
9. Il sistema esegue un ultimo controllo di disponibilità.
10. Se l'orario è ancora libero:
    - salva la prenotazione nel database
    - invia l'email di conferma

---

## Funzionalità MVP

### Trattamenti

| ID | Servizio                  | Categoria | Durata (min) |
| -- | ------------------------- | --------- | -----------: |
| 1  | Taglio Uomo               | Uomo      |           30 |
| 2  | Taglio Uomo + Shampoo     | Uomo      |           45 |
| 3  | Taglio Donna              | Donna     |           45 |
| 4  | Taglio Donna + Piega      | Donna     |           75 |
| 5  | Piega                     | Donna     |           45 |
| 6  | Shampoo                   | Unisex    |           15 |
| 7  | Barba                     | Uomo      |           15 |
| 8  | Colore Ricrescita         | Donna     |           60 |
| 9  | Colore Completo           | Donna     |           90 |
| 10 | Tonalizzazione            | Donna     |           30 |
| 11 | Meches                    | Donna     |          120 |
| 12 | Trattamento Ricostruzione | Unisex    |           45 |
| 13 | Cheratina                 | Unisex    |          180 |
| 14 | Acconciatura Cerimonia    | Donna     |          120 |

### Salvataggio prenotazioni

Le prenotazioni sono salvate con:
- id
- nome
- cognome
- email
- data
- ora
- trattamento_id

### Route Flask

| Metodo | Route               | Descrizione                                                                       |
| ------ | ------------------- | --------------------------------------------------------------------------------- |
| GET    | `/homepage`         | Visualizza la homepage con la lista dei trattamenti e il form di prenotazione     |
| GET    | `/trattamenti`      | Recupera tutti i trattamenti disponibili dal database                             |
| GET    | `/slot-disponibili` | Recupera gli slot/orari disponibili per una determinata data e trattamento        |
| POST   | `/prenotazione`     | Crea una nuova prenotazione e la salva nel database                               |
| GET    | `/login`            | Visualizza il form di login dell'amministratore                                   |
| POST   | `/login`            | Verifica le credenziali e avvia la sessione amministratore                        |
| GET    | `/dashboard-admin`  | Visualizza la dashboard con l'elenco delle prenotazioni e le funzioni di gestione |
| GET    | `/logout`           | Termina la sessione amministratore e reindirizza al login o alla homepage         |

---

## Sviluppo

1. Database SQLite
2. Connessione Flask con SQLite
3. Tabella trattamenti
4. Calcolo prenotazione
5. Calcolo slot disponibili
6. Dashboard admin
7. Login admin con sessione
8. Invio email
9. Frontend moderno

---

## Struttura

booking_system/
│
├── app/
│   ├── __init__.py        # crea app
│   ├── routes.py          # endpoint
│   ├── models.py          # logica database
│   ├── config.py          # configurazioni (DB, secret key, etc.)
│   ├── services.py        # logica business slot, prenotazioni
│   ├── database.py        # connessione SQLite
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── admin.html
│   │   ├── login.html
│   │   └── dashboard.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   │
│   └── utils/
│       └── helpers.py    # per funzioni generiche e riutilizzabili
│
├── database/
│   └── app.db
│
├── requirements.txt
├── run.py                 # avvio server
├── .env                   # variabili segrete (password DB, ecc.)
├── README.md
└── roadmap.md