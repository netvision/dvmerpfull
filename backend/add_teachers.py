"""
Add or update teacher user accounts.

Usage:
  cd backend
  venv\Scripts\python add_teachers.py

This script is idempotent: running it multiple times will keep the same users
and reset their password to the configured common password.
"""

import os
import sys
from pathlib import Path

import bcrypt as _bcrypt
from dotenv import load_dotenv

# Ensure imports resolve relative to this file's directory
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from models import User, UserRole


COMMON_PASSWORD = "dvm1234"
DOMAIN = "dalmiatrusts.in"

TEACHER_USERNAMES = [
    "sarika.saxena",
    "ravita.sharma",
    "sheela.nunia",
    "kamal.singh",
    "karan.singh",
    "monika.gill",
    "anil.jha",
    "babulal.jangir",
    "sunita.boran",
    "sonam.baloda",
    "sikandar.pandey",
    "vinita.choudhary",
    "dharmendra.tiwari",
    "ranjeet.tiwari",
]


def _hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt()).decode()


def _title_name_from_username(username: str) -> str:
    # e.g. "sarika.saxena" -> "Sarika Saxena"
    return " ".join(part.capitalize() for part in username.split("."))


def main() -> None:
    # Load backend/.env if present so DATABASE_URL is picked up.
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

    db = SessionLocal()
    created = 0
    updated = 0
    try:
        for username in TEACHER_USERNAMES:
            email = f"{username}@{DOMAIN}".lower()
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                user = User(
                    name=_title_name_from_username(username),
                    email=email,
                    hashed_password=_hash_password(COMMON_PASSWORD),
                    role=UserRole.teacher,
                    is_active=True,
                )
                db.add(user)
                created += 1
            else:
                user.name = _title_name_from_username(username)
                user.role = UserRole.teacher
                user.is_active = True
                user.hashed_password = _hash_password(COMMON_PASSWORD)
                updated += 1

        db.commit()

        print("Teacher user upsert completed.")
        print(f"Created: {created}")
        print(f"Updated: {updated}")
        print(f"Password set for all listed users: {COMMON_PASSWORD}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
