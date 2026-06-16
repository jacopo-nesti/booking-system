# Project Structure

```text
booking-system/
│
├── app/
│   ├── __init__.py                # Flask application factory
│   ├── auth.py                    # Authentication and security logic
│   ├── config.py                  # Configuration (DB path, secret key, etc.)
│   ├── database.py                # DB connection, queries, initialization
│   ├── helpers.py                 # Utility functions and decorators
│   ├── models.py                  # Data models (conceptual / SQL helpers)
│   ├── routes.py                  # HTTP routes (Blueprint)
│   ├── seed.py                    # Database seeding / initial data setup
│   ├── services.py                # Business logic (availability, booking rules)
│   │
│   ├── docs/
│   │   ├── INSTALLATION.md        # Setup and installation guide
│   │   ├── ROADMAP.md             # Project roadmap and future steps
│   │   └── STRUCTURE.md           # Detailed architecture notes
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── admin.css
│   │   │   ├── base.css
│   │   │   ├── booking.css
│   │   │   ├── dashboard.css
│   │   │   ├── forms.css
│   │   │   ├── home.css
│   │   │   ├── main.css
│   │   │   ├── navbar.css
│   │   │   └── responsive.css
│   │   │  
│   │   ├── js/
│   │   │   
│   │   └── images/
│   │       │
│   │       └── screenshots/
│   │           ├── preview.gif
│   │           ├── admin_dashboard.png
│   │           ├── edit_delete_treatment.png
│   │           └── new_treatment.png
│   │
│   └── templates/
│       ├── admin_dashboard.html
│       ├── admin_treatments.html
│       ├── availability.html
│       ├── base.html
│       ├── book.html
│       ├── contacts.html
│       ├── create_treatment.html
│       ├── dashboard.html
│       ├── edit_treatment.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── selection.html
│       └── success.html
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py                         # Application entry point
```