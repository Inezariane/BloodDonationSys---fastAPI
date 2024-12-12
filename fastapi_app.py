from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from Donors.database import SessionLocal
from Donors.models import Donor, BloodGroup, RequestBlood, User
import bcrypt
import random
from datetime import datetime
from sqlalchemy import func

# Initialize FastAPI
app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for input validation

class DonorCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
    phone: str
    city: str
    address: str
    blood_group: str  
    gender: str
    ready_to_donate: bool
    password: str  

class BloodRequest(BaseModel):
    name: str
    email: str
    phone: str
    city: str
    address: str
    blood_group: str
    date: str

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()  
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8') 

# --- ENDPOINTS ---

# 1. **Root endpoint** (Welcome message)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Blood Donation System!"}

# 2. **Favicon endpoint** (Empty response to avoid 404)
@app.get("/favicon.ico")
def favicon():
    return JSONResponse(content={}, status_code=204)

#Generate donors
@app.post("/generate-donors/")
def generate_donors(db: Session = Depends(get_db)):
    num_rows = 500000  # Number of rows to insert
    blood_groups = db.query(BloodGroup).all()  
    
    if not blood_groups:
        return JSONResponse(status_code=400, content={"message": "No blood groups found in the database!"})

    for _ in range(num_rows):
        
        blood_group = random.choice(blood_groups) 
        
        donor = Donor(
            username=f"donor{random.randint(1000, 9999)}",  # Random username
            first_name=f"First{random.randint(1, 100)}",  # Random first name
            last_name=f"Last{random.randint(1, 100)}",  # Random last name
            email=f"donor{random.randint(1, 10000)}@example.com",  # Random email
            password="hashedpassword",  # Placeholder password
            date_of_birth=datetime.today().strftime('%Y-%m-%d'),  # Placeholder for DOB
            phone=f"{random.randint(1000000000, 9999999999)}",  # Random phone number
            city="RandomCity",  # Placeholder city
            address="Random address",  # Placeholder address
            blood_group_id=blood_group.id,
            gender=random.choice(["Male", "Female"]),  # Random gender
            ready_to_donate=True  # Set ready_to_donate as True
        )
        
        db.add(donor)  
    
    db.commit()  
    return JSONResponse(status_code=200, content={"message": f"{num_rows} donor records created successfully!"})

# 3. **Get all blood groups with donor count**
@app.get("/blood_groups/")
def list_blood_groups(db: Session = Depends(get_db)):
    blood_groups = db.query(
        BloodGroup.name,
        func.count(Donor.id).label("donor_count")  
    ).join(
        Donor, Donor.blood_group_id == BloodGroup.id, isouter=True  
    ).group_by(
        BloodGroup.id  
    ).all()  

    results = [
        {"name": group[0], "donor_count": group[1]} for group in blood_groups
    ]
    
    return results

# 4. **Get donors by blood group**
@app.get("/donors/by_group/{blood_group_name}")
def list_donors(blood_group_name: str, db: Session = Depends(get_db)):
    blood_group = db.query(BloodGroup).filter(BloodGroup.name.ilike(blood_group_name)).first()
    if not blood_group:
        raise HTTPException(status_code=404, detail=f"Blood group '{blood_group_name}' not found")
    
    donors = db.query(Donor).filter(Donor.blood_group_id == blood_group.id).all()
    return donors

@app.get("/donors/")
def get_all_donors(db: Session = Depends(get_db)):
    donors = db.query(Donor).all()  
    results = [
        {
            "username": donor.username,
            "first_name": donor.first_name,
            "last_name": donor.last_name,
            "email": donor.email,
            "phone": donor.phone,
            "city": donor.city,
            "address": donor.address,
            "blood_group": donor.blood_group.name,  
            "ready_to_donate": donor.ready_to_donate
        }
        for donor in donors
    ]
    return results

# 5. **Get donor details**
@app.get("/donors/details/{donor_id}")
def donor_details(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    return donor

# 6. **Request blood**
@app.post("/blood_requests/")
def create_blood_request(request_data: BloodRequest, db: Session = Depends(get_db)):
    blood_group = db.query(BloodGroup).filter(BloodGroup.name.ilike(request_data.blood_group)).first()
    if not blood_group:
        available_groups = [group.name for group in db.query(BloodGroup).all()]
        raise HTTPException(
            status_code=400,
            detail=f"Invalid blood group: {request_data.blood_group}. Available groups: {available_groups}"
        )

    new_request = RequestBlood(
        name=request_data.name,
        email=request_data.email,
        phone=request_data.phone,
        city=request_data.city,
        address=request_data.address,
        blood_group=blood_group,
        date=request_data.date,
    )
    db.add(new_request)
    db.commit()
    return {"message": "Blood request created successfully"}

# 7. **See all blood requests**
@app.get("/blood_requests/")
def list_blood_requests(db: Session = Depends(get_db)):
    requests = db.query(RequestBlood).all()
    return requests

# 8. **Register as donor**

@app.post("/donors/")
def create_donor(donor: DonorCreate, db: Session = Depends(get_db)):

    blood_group = db.query(BloodGroup).filter(BloodGroup.name == donor.blood_group).first()

    if not blood_group:
        raise HTTPException(status_code=404, detail="Blood group not found")

    hashed_password = hash_password(donor.password)

    new_donor = Donor(
        username=donor.username,
        first_name=donor.first_name,
        last_name=donor.last_name,
        email=donor.email,
        date_of_birth=donor.date_of_birth,
        phone=donor.phone,
        city=donor.city,
        address=donor.address,
        gender=donor.gender,
        blood_group_id=blood_group.id,  # Automatically set the blood group ID
        ready_to_donate=donor.ready_to_donate,
        password=hashed_password  # Store the hashed password
    )

    db.add(new_donor)
    db.commit()

    return {"message": "Donor created successfully", "donor_id": new_donor.id}

# 9. **Login (Mocked)**
# @app.post("/login/")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     if not user or user.password != password:  # Replace with hashed password check
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"message": "Login successful", "username": user.username}

# 10. **Edit profile**
# @app.put("/donors/edit/{donor_id}")
# def edit_donor_profile(donor_id: int, donor_data: DonorCreate, db: Session = Depends(get_db)):
#     donor = db.query(Donor).filter(Donor.id == donor_id).first()
#     if not donor:
#         raise HTTPException(status_code=404, detail="Donor not found")
    
#     donor.first_name = donor_data.first_name
#     donor.last_name = donor_data.last_name
#     donor.email = donor_data.email
#     donor.phone = donor_data.phone
#     donor.city = donor_data.city
#     donor.address = donor_data.address
#     donor.gender = donor_data.gender
#     db.commit()
#     return {"message": "Profile updated successfully"}

# 11. **Change donation status**
@app.put("/donors/status/{donor_id}")
def change_donor_status(donor_id: int, db: Session = Depends(get_db)):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    donor.ready_to_donate = not donor.ready_to_donate
    db.commit()
    return {"message": f"Ready to donate: {donor.ready_to_donate}"}
