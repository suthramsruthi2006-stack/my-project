from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "sruthi", "age": 19, "city": "kuppam"},
    {"id": 2, "name": "swathi", "age": 20, "city": "ramakuppam"}
]

class StudentUpdate(BaseModel):
    name: str
    age: int
    city: str

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students[i] = {
                "id": student_id,
                "name": student.name,
                "age": student.age,
                "city": student.city
            }
            return students[i]

    raise HTTPException(status_code=404, detail=f"Student {student_id} not found")




































    class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/register", status_code=201)
def register(user: UserRegister):
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="username already taken")

    hashed = hash_password(user.password)

    new_user = {
        "id": len(users_db) + 1,
        "username": user.username,
        "hashed_password": hashed
    }

    users_db.append(new_user)

    return {"message": f"Account created for {user.username}"}


@app.post("/login")
def login(user: UserLogin):
    print("Incoming login:", user)
    print("Current DB:", users_db)

    found_user = None

    for u in users_db:
        print("Checking user:", u["username"])
        if u["username"] == user.username:
            found_user = u
            break

    if not found_user:
        print("User not found")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    print("Stored hash:", found_user["hashed_password"])

    if not verify_password(user.password, found_user["hashed_password"]):
        print("Password mismatch")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    print("Login success")
    return {"message": "login successful", "username": user.username}