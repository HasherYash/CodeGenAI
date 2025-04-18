Here is the Python code for the FastAPI routers based on the provided requirements:

```python
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Leave(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(Text)
    status = Column(Text)

class Pod(Base):
    __tablename__ = 'pods'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    members = Column(ARRAY(Integer))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)

engine = create_engine('postgresql://user:password@host:port/dbname')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.get("/api/dashboard/tiles")
async def fetch_dashboard_data(token: str = Depends(oauth2_scheme)):
    return {"tiles": []}

@router.post("/api/lms/leaves/apply")
async def apply_for_leave(leave_apply_request: LeaveApplyRequest, token: str = Depends(oauth2_scheme)):
    # Apply for leave logic
    return {"message": "Leave applied successfully", "status": "pending"}

@router.patch("/api/lms/leaves/{leave_id}/approve")
async def approve_leave(leave_approve_request: LeaveApproveRequest, leave_id: int, token: str = Depends(oauth2_scheme)):
    # Approve leave logic
    return {"message": "Leave approved successfully", "status": "approved"}

@router.get("/api/pods/{pod_id}/details")
async def get_pod_details(pod_id: int, token: str = Depends(oauth2_scheme)):
    # Get pod details logic
    return {"pod_id": pod_id, "pod_name": "", "members": []}

@router.post("/api/pods/{pod_id}/recommend")
async def recommend_employee(pod_recommendation_request: PodRecommendationRequest, pod_id: int, token: str = Depends(oauth2_scheme)):
    # Recommend employee logic
    return {"message": "Employee recommended successfully"}

@router.post("/api/auth/login")
async def login(login_request: LoginRequest):
    # Login logic
    return {"token": "", "user": {}}

@router.get("/api/auth/user")
async def fetch_current_user(token: str = Depends(oauth2_scheme)):
    # Fetch current user details logic
    return {"id": 1, "name": "", "role": "general_user"}

app.include_router(router)
```