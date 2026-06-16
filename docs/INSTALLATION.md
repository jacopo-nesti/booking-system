# Installation and Setup

## 1. Clone the repository
```bash
git clone https://github.com/jacopo-nesti/booking-system.git
cd booking-system
```

## 2. Create a virtual environment
```bash
python -m venv venv
```
Activate it:

- Windows
```bash
venv\Scripts\activate
```
- Mac/Linux
```bash
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure environment variables
Copy the example file and fill in your values:
```bash
copy .env.example .env
```
Open `.env` and set:
```
SECRET_KEY=your_secret_key
ADMIN_EMAIL=your@email.com
ADMIN_PASSWORD=your_password
```

To generate a secure `SECRET_KEY` you can run:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 5. Run the application
```bash
python run.py
```

## 5. Open in browser
Open your browser and navigate to:  

👉 http://127.0.0.1:5000/

## Note

The SQLite database is automatically created on the first run of the application.
