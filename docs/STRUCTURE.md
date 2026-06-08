# Project Structure

```text
booking-system/
│
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── config.py                # Configuration (DB path, secret key, etc.)
│   ├── routes.py                # HTTP routes (Blueprint)
│   ├── services.py              # Business logic (availability, booking rules)
│   ├── models.py                # Data models (conceptual / SQL helpers)
│   ├── database.py             # DB connection, queries, initialization
│   ├── helpers.py              # Utility functions and decorators
│   ├── seed.py                 # Database seeding / initial data setup
│   ├── auth.py                 # Authentication and security logic
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── book.html
│   │   ├── selection.html
│   │   ├── availability.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── success.html
│   │   ├── dashboard.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_treatments.html
│   │   ├── create_treatment.html
│   │   ├── edit_treatment.html
│   │   └── contacts.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │
│   │   └── images/
│   │
│   └── docs/
│       ├── roadmap.md
│       ├── STRUCTURE.md
│       └──  INSTALLATION.md  # Setup and installation guide
│
├── run.py                   # Application entry point
├── requirements.txt         # Project dependencies
├── .gitignore
└── README.md
```