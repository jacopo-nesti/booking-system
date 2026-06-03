# Project Structure

```text
booking-system/
│
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── config.py            # Configuration (DB path, secret key, etc.)
│   ├── routes.py            # HTTP endpoints
│   ├── services.py          # Business logic (booking system)
│   ├── models.py            # Entity definitions (conceptual / SQL helpers)
│   ├── database.py          # DB connection, queries, and initialization
│   ├── helpers.py           # Reusable helper functions
│   ├── seed.py              # Database seeding / initial data setup
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── book.html
│   │   ├── availability.html
│   │   ├── success.html
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
│   ├── docs/
│       ├── roadmap.md
│       ├── STRUCTURE.md
│       ├── INSTALLATION.md  # Setup and installation guide
│
├── run.py                   # Application entry point
├── requirements.txt         # Project dependencies
├── LICENSE.md               # Project license
├── .gitignore
├── .env
└── README.md
```