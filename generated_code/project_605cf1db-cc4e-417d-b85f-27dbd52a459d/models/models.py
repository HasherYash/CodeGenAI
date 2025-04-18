Here are the Pydantic models based on the entities:

```
from pydantic import BaseModel
from datetime import date

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

class User(BaseModel):
    id: int
    name: str
    role: str

class Token(BaseModel):
    token: str
    user: User

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(Token):
    pass

class DashboardResponse(BaseModel):
    tiles: list[dict]

class LeaveApplyRequest(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveApplyResponse(BaseModel):
    message: str
    status: str

class LeaveApproveRequest(BaseModel):
    status: str

class PodDetailsResponse(BaseModel):
    pod_id: int
    pod_name: str
    members: list[int]

class PodRecommendationRequest(BaseModel):
    recommended_user_id: int

class PodRecommendationResponse(BaseModel):
    message: str
```