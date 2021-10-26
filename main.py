from typing import  Optional
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Body, Query, Path
from enum import Enum

app = FastAPI()

# Models

class HairColor(Enum):
    white = "White"
    brown = "Brown"
    black = "Black"
    red = "Red"

class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=130)
    height: float = Field(..., gt=0, le=250)
    hair_color: Optional[HairColor] = Field(defaul=None)
    is_married: Optional[bool] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)

class Location(BaseModel):
    city: str
    country: str
    state: str


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

# Validate request body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ..., gt=0, 
        title="Person ID", 
        description="This is the person ID."
    ),
    person: Person = Body(...), 
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict()) 
    return results