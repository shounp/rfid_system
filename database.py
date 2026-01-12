from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Ajuste conforme seu container MySQL
DB_USER = "rfid_user"
DB_PASSWORD = "rfid123"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "rfid"

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
