import os
import sys
import pandas as pd
import math
from datetime import datetime

# Add backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
from dotenv import load_dotenv
load_dotenv(os.path.join(backend_dir, '.env'))

sys.path.insert(0, backend_dir)

from database import SessionLocal
from models import User, UserRole, Class, Section, Student, Guardian, StudentGuardian, AcademicYear, StaffProfile, StudentProfile

from auth import hash_password

def clean_val(val):
    if pd.isna(val) or val == 'nan':
        return None
    v = str(val).strip()
    # Strip trailing .0 that pandas adds to integer-like floats (e.g. phone numbers)
    if v.endswith('.0') and v[:-2].lstrip('-').isdigit():
        v = v[:-2]
    return v if v else None

def parse_date(date_str):
    if not date_str: return None
    try:
        # Expected format like "23-03-1976" or similar
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    except:
        return None

def run_import():
    db = SessionLocal()
    
    staff_file = os.path.join(backend_dir, "..", "stafflist.xls")
    student_file = os.path.join(backend_dir, "..", "studentlist.xls")

    if not os.path.exists(staff_file) or not os.path.exists(student_file):
        print("XLS files not found in root.")
        return

    print("Importing Staff...")
    # Dynamically find header row
    df_temp_staff = pd.read_excel(staff_file, header=None)
    staff_header_row = df_temp_staff[df_temp_staff.eq('Sr No.').any(axis=1)].index[0]
    df_staff = pd.read_excel(staff_file, header=staff_header_row)
    default_password = hash_password("Welcome@123")
    
    staff_count = 0
    for _, row in df_staff.iterrows():
        name = clean_val(row.get('Name'))
        if not name: continue
        
        staff_code = clean_val(row.get('Staff Code')) or "UNKNOWN"
        official_email = clean_val(row.get('Official Email Id'))
        personal_email = clean_val(row.get('Personal Email Id'))
        
        email = official_email or personal_email or f"{staff_code.lower()}@dvm.local"
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        user = existing_user
        if not existing_user:
            user = User(
                name=name,
                email=email,
                hashed_password=default_password,
                role=UserRole.teacher,
                is_active=True
            )
            db.add(user)
            staff_count += 1
            
        # Create profile if it doesn't exist
        if not db.query(StaffProfile).filter(StaffProfile.user_id == user.id).first():
            profile = StaffProfile(
                staff_code=staff_code,
                date_of_birth=parse_date(clean_val(row.get('Date of Birth'))),
                gender=clean_val(row.get('Gender')),
                blood_group=clean_val(row.get('Blood Group')),
                marital_status=clean_val(row.get('Marital Status')),
                department=clean_val(row.get('Department')),
                designation=clean_val(row.get('Designation')),
                joining_date=parse_date(clean_val(row.get('Joining Date'))),
                address=clean_val(row.get('Address')),
                city=clean_val(row.get('City')),
                state=clean_val(row.get('State')),
                nationality=clean_val(row.get('Nationality')),
                qualification=clean_val(row.get('Qualification')),
                bank_name=clean_val(row.get('Bank')),
                account_no=clean_val(row.get('Account No.')),
                ifsc_code=clean_val(row.get('Ifsc Code')),
                pan_no=clean_val(row.get('Pan No')),
                aadhaar_no=clean_val(row.get('Aadhaar No.')),
                pf_no=clean_val(row.get('PF No.')),
                esi_no=clean_val(row.get('ESI No.'))
            )
            user.profile = profile
            # Only add to session if it's a new user or we just created the profile
            if existing_user:
                db.add(profile)
            
        if not existing_user:
            pass # count was incremented above
            
    db.commit()
    print(f"Added {staff_count} new staff members.")

    print("Importing Students...")
    # Dynamically find header row
    df_temp_student = pd.read_excel(student_file, header=None)
    student_header_row = df_temp_student[df_temp_student.eq('Sr No.').any(axis=1)].index[0]
    df_student = pd.read_excel(student_file, header=student_header_row)
    
    # Ensure Current Academic Year exists
    ac_year_str = "2026-27"
    ac_year = db.query(AcademicYear).filter(AcademicYear.name == ac_year_str).first()
    if not ac_year:
        ac_year = AcademicYear(name=ac_year_str, start_date=datetime(2026,4,1).date(), end_date=datetime(2027,3,31).date(), is_active=True)
        db.add(ac_year)
        db.commit()
        db.refresh(ac_year)
    
    student_count = 0
    guardian_count = 0
    for _, row in df_student.iterrows():
        adm_no = clean_val(row.get('Admission Number'))
        first_name = clean_val(row.get('First Name'))
        if not adm_no or not first_name: continue
        
        last_name = clean_val(row.get('Last Name'))
        dob = parse_date(clean_val(row.get('Date of Birth')))
        gender = clean_val(row.get('Gender'))
        phone = clean_val(row.get('Primary Mobile Number')) or clean_val(row.get('Residential Phone Number'))
        email = clean_val(row.get('Primary Email ID'))
        address = clean_val(row.get('Address'))
        
        class_section = clean_val(row.get('Class & Section'))
        class_name = "UNKNOWN"
        section_name = "A"
        if class_section and "-" in class_section:
            parts = class_section.split("-", 1)
            raw_class_name = parts[0].strip()
            section_name = parts[1].strip()
            
            # Map Roman numerals to Class X
            roman_to_num = {
                'I': 'Class 1',
                'II': 'Class 2',
                'III': 'Class 3',
                'IV': 'Class 4',
                'V': 'Class 5',
                'VI': 'Class 6',
                'VII': 'Class 7',
                'VIII': 'Class 8',
                'IX': 'Class 9',
                'X': 'Class 10',
                'XI': 'Class 11',
                'XII': 'Class 12',
            }
            class_name = roman_to_num.get(raw_class_name, raw_class_name)
        
        # Get or create Class
        cls = db.query(Class).filter(Class.name == class_name).first()
        if not cls:
            cls = Class(name=class_name)
            db.add(cls)
            db.commit()
            db.refresh(cls)
            
        # Get or create Section
        sec = db.query(Section).filter(Section.name == section_name, Section.class_id == cls.id).first()
        if not sec:
            sec = Section(name=section_name, class_id=cls.id)
            db.add(sec)
            db.commit()
            db.refresh(sec)
            
        student = db.query(Student).filter(Student.admission_no == str(adm_no)).first()
        is_new_student = False
        if not student:
            is_new_student = True
            student = Student(
                admission_no=str(adm_no),
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender,
                phone=phone,
                email=email,
                address=address,
                class_id=cls.id,
                section_id=sec.id,
                academic_year_id=ac_year.id,
            )
            db.add(student)
            db.commit() # Commit to get student.id for guardian linking
            student_count += 1
            
        if not db.query(StudentProfile).filter(StudentProfile.student_id == student.id).first():
            profile = StudentProfile(
                student_id=student.id,
                blood_group=clean_val(row.get('Blood Group')),
                category=clean_val(row.get('Category')),
                religion=clean_val(row.get('Religion')),
                nationality=clean_val(row.get('Nationality')),
                mother_tongue=clean_val(row.get('Mother Tongue')),
                previous_school=clean_val(row.get('Previous School Name')),
                height=float(clean_val(row.get('Height'))) if clean_val(row.get('Height')) else None,
                weight=float(clean_val(row.get('Weight'))) if clean_val(row.get('Weight')) else None,
                vision=clean_val(row.get('Vision')),
                is_transport=clean_val(row.get('Is Transport')) == 'Yes',
                pickup_route=clean_val(row.get('Pick-up Route')),
                drop_route=clean_val(row.get('Drop-off Route')),
                bank_name=clean_val(row.get('Bank Name')),
                account_no=clean_val(row.get('Account No')),
                ifsc_code=clean_val(row.get('IFSC')),
                aadhaar_no=clean_val(row.get('Aadhaar Number')),
                pen_no=clean_val(row.get('Permanent Education Number(PEN)')),
                apaar_id=clean_val(row.get('APAAR ID'))
            )
            db.add(profile)
            
        if is_new_student:
            # Guardians (only add for new students to avoid duplicate processing)
            father_name = clean_val(row.get('Father Name'))
            mother_name = clean_val(row.get('Mother Name'))
            father_phone = clean_val(row.get("Father's Primary Contact Number"))
            mother_phone = clean_val(row.get("Mother's Primary Contact Number"))
            
            added_guardians = set()
            
            if father_name:
                g_father = db.query(Guardian).filter(Guardian.name == father_name, Guardian.phone == father_phone).first()
                if not g_father:
                    g_father = Guardian(name=father_name, relation="Father", phone=father_phone)
                    db.add(g_father)
                    db.commit()
                    db.refresh(g_father)
                    guardian_count += 1
                if g_father.id not in added_guardians:
                    db.add(StudentGuardian(student_id=student.id, guardian_id=g_father.id, is_primary=True))
                    added_guardians.add(g_father.id)
                
            if mother_name:
                g_mother = db.query(Guardian).filter(Guardian.name == mother_name, Guardian.phone == mother_phone).first()
                if not g_mother:
                    g_mother = Guardian(name=mother_name, relation="Mother", phone=mother_phone)
                    db.add(g_mother)
                    db.commit()
                    db.refresh(g_mother)
                    guardian_count += 1
                if g_mother.id not in added_guardians:
                    db.add(StudentGuardian(student_id=student.id, guardian_id=g_mother.id, is_primary=False))
                    added_guardians.add(g_mother.id)

    db.commit()
    print(f"Added {student_count} new students and {guardian_count} new guardians.")

if __name__ == "__main__":
    run_import()
