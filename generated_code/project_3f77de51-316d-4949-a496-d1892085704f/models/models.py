```
from pydantic import BaseModel

class Leave(BaseModel):
    id: int
    start_date: str
    end_date: str
    reason: str
    status: str

class Pod(BaseModel):
    id: int
    name: str
    members: list[int]

class User(BaseModel):
    id: int
    name: str
    role: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    token: str
    user: User

class CurrentUser(BaseModel):
    id: int
    name: str
    role: str
```