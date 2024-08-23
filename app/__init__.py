from app.db import init_db
from app.models import User

init_db()
print("Database initialized." * 10)
