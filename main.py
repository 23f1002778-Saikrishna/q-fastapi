from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_PATH = Path(__file__).parent / "q-fastapi.csv"

def load_students():
    students = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({"studentId": int(row["studentId"]), "class": row["class"]})
    return students

STUDENTS = load_students()

@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(default=None, alias="class")):
    if class_:
        class_set = set(class_)
        result = [s for s in STUDENTS if s["class"] in class_set]
    else:
        result = STUDENTS
    return {"students": result}
