from typing import  Optional
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Header
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie
from fastapi import UploadFile, File
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

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Julian",
                "last_name": "Martinez Villarreal",
                "age": 21,
                "height": 181,
                "hair_color": "Black",
                "is_married": False,
                "email": "julian@martinez.com"
            }
        }

class Location(BaseModel):
    city: str
    country: str
    state: str

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='jumar98')
    message: str = Field(default="User logged with success!!")

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
        description="This is a person name.",
        example="Alba"
        ),
    age: int = Query(
        ..., 
        title="Person Age", 
        description="This a person age.",
        example=25
        )
    ):
    return {name: age}

# Validate path parameter

@app.get('/person/detail/{person_id}')
def person_detail(
    person_id: int = Path(..., gt=0, 
        title="Person ID", 
        description="This is the person ID.", 
        example=154548
    )):
    return {person_id: "Success"}

# Validate request body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ..., gt=0, 
        title="Person ID", 
        description="This is the person ID.",
        example=123,
    ),
    person: Person = Body(...), 
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict()) 
    return person

# Forms

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


# Cookies and headers parameters

@app.post(
    path="/contact", 
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# Uploading files

@app.post(
    path='/post-image'
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        'filename': image.filename,
        'format': image.content_type,
        'size': round(len(image.file.read()) / 1024, 2)
    }