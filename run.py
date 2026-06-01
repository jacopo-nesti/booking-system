from app import create_app
from app.database import init_db
from app.seed import seed_treatments

if __name__ == "__main__":
    init_db()
    seed_treatments()
    app = create_app()
    app.run(debug=True)