from typing import  Optional
from pydantic import BaseModel
from fastapi import FastAPI, Body, Query, Path

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

# Validate query parameters

@app.get('/person/detail')
def person_detail(
    name: Optional[str] = Query(
        default=None, min_length=1, max_length=50, 
        title='Person Nam',
        description="This is a person name."
        ),
    age: int = Query(..., title="Person Age", description="This a person age.")
    ):
    return {name: age}

# Validate path parameter

@app.get('/person/detail/{person_id}')
def person_detail(
    person_id: int = Path(..., gt=0, 
        title="Person ID", 
        description="This is the person ID."
    )):
    return {person_id: "Success"}