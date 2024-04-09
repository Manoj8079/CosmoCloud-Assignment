from fastapi import FastAPI, HTTPException
from database import students_collection
from schemas import StudentCreate, StudentUpdate
from models import Student
from typing import List
from bson import ObjectId

app = FastAPI()

# insert
@app.post("/students", response_model=Student)
async def create_student(student: StudentCreate):
    result = await students_collection.insert_one(student.dict())
    created_student = await students_collection.find_one({"_id": result.inserted_id})
    # Print the specific ID of the newly created student
    print(f"New student created with ID: {result.inserted_id}")
    return created_student

@app.get("/students", response_model=List[Student])
async def list_students(country: str = None, age: int = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = await students_collection.find(query).to_list(length=100)
    return students



@app.get("/students/{id}", response_model=Student)
async def get_student(id: str):
    # Convert the string ID to an ObjectId for querying
    student_id = ObjectId(id)
    student = await students_collection.find_one({"_id": student_id})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student



# update
@app.patch("/students/{id}", response_model=Student)
async def update_student(id: str, student: StudentUpdate):
    # Convert the string ID to an ObjectId for querying
    student_id = ObjectId(id)
    result = await students_collection.update_one({"_id": student_id}, {"$set": student.dict(exclude_unset=True)})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student = await students_collection.find_one({"_id": student_id})
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found after update")
    return updated_student


from typing import Dict

@app.delete("/students/{id}", response_model=Dict[str, str])
async def delete_student(id: str):
    student_id = ObjectId(id)
    result = await students_collection.delete_one({"_id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}

