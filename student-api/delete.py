from fastapi import FastAPI
app = FastAPI()
students = [
      {"id": 1, "name": "Ravi",  "age": 20},
    {"id": 2, "name": "Priya", "age": 21},
    {"id": 3, "name": "Kiran", "age": 19},
]
@app.delete("/students/{student_id}")
def delete_student(Student_id: int):
    for i,s in enumerate(Students):
        if s["id"] == student_id:
            deleted = students.pop(i)
            return{"message": f"student '{deleted['name']}'deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Student {student_id} not found")