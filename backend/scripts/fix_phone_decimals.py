"""One-time cleanup: strip trailing .0 from phone numbers and numeric string fields in DB."""
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
from dotenv import load_dotenv
load_dotenv(os.path.join(backend_dir, '.env'))
sys.path.insert(0, backend_dir)

from database import SessionLocal
from models import Student, Guardian, StaffProfile, StudentProfile

db = SessionLocal()

def fix(v):
    if v and isinstance(v, str) and v.endswith('.0') and v[:-2].lstrip('-').isdigit():
        return v[:-2]
    return v

# Students
changed = 0
for s in db.query(Student).all():
    new_phone = fix(s.phone)
    new_email = fix(s.email)
    if new_phone != s.phone or new_email != s.email:
        s.phone = new_phone
        s.email = new_email
        changed += 1
print(f"Fixed {changed} student phone/email fields")

# Guardians
changed = 0
for g in db.query(Guardian).all():
    new_phone = fix(g.phone)
    if new_phone != g.phone:
        g.phone = new_phone
        changed += 1
print(f"Fixed {changed} guardian phone fields")

# StaffProfile
changed = 0
for p in db.query(StaffProfile).all():
    for field in ['account_no', 'pan_no', 'aadhaar_no', 'pf_no', 'esi_no']:
        val = getattr(p, field)
        new_val = fix(val)
        if new_val != val:
            setattr(p, field, new_val)
            changed += 1
print(f"Fixed {changed} staff profile numeric fields")

# StudentProfile
changed = 0
for p in db.query(StudentProfile).all():
    for field in ['account_no', 'aadhaar_no', 'pen_no', 'apaar_id']:
        val = getattr(p, field)
        new_val = fix(val)
        if new_val != val:
            setattr(p, field, new_val)
            changed += 1
print(f"Fixed {changed} student profile numeric fields")

db.commit()
print("Done.")
