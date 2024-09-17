# backend/app/seed.py

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User, Base, Role

# Create tables
Base.metadata.create_all(bind=engine)

# Create initial users
def seed_data(db: Session):
    tenant_user = User(
        username="tenant_user",
        email="tenant@example.com",
        hashed_password=User.hash_password("password123"),
        role=Role.tenant
    )

    caretaker_user = User(
        username="caretaker_user",
        email="caretaker@example.com",
        hashed_password=User.hash_password("password123"),
        role=Role.care_taker
    )

    admin_user = User(
        username="admin_user",
        email="admin@example.com",
        hashed_password=User.hash_password("password123"),
        role=Role.admin
    )

    db.add(tenant_user)
    db.add(caretaker_user)
    db.add(admin_user)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()
