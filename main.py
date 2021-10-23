from typing import  Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    height: float
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get('/')
def home():
    return {'message': "Hello world!!"}

# Request and response body

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person
