import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.database import init_db
from app.seed import seed_treatments, seed_admin

if __name__ == "__main__":
    app = create_app()
    app.secret_key = os.getenv("SECRET_KEY")

    init_db()
    seed_treatments()
    seed_admin()

    app.run(debug=True)