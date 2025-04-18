Here are the Pydantic models based on the entities:

```
from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int
    name: str
    role: str

class Leave(BaseModel):
    id: int
    start_date: date
    end_date: date
    reason: str
    status: str

class Pod(BaseModel):
    id: int
    name: str
    members: list[int]

class PodMember(BaseModel):
    pod_id: int
    user_id: int
```