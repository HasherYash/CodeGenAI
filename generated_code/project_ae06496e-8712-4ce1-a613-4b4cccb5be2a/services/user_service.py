Here is the service layer code based on the provided requirements:
```
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User, Leave, Pod, PodMember
from .database import SessionLocal

class LeaveService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def apply_for_leave(self, start_date: date, end_date: date, reason: str, user_id: int) -> dict:
        leave = Leave(start_date=start_date, end_date=end_date, reason=reason, user_id=user_id)
        self.db_session.add(leave)
        self.db_session.commit()
        return {"message": "Leave request submitted successfully", "status": "pending"}

    def approve_leave(self, leave_id: int, status: str) -> dict:
        leave = self.db_session.query(Leave).filter(Leave.id == leave_id).first()
        if leave is None:
            raise HTTPException(status_code=404, detail="Leave not found")
        leave.status = status
        self.db_session.commit()
        return {"message": "Leave request approved", "status": "approved"}

class PodService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_pod_details(self, pod_id: int) -> dict:
        pod = self.db_session.query(Pod).filter(Pod.id == pod_id).first()
        if pod is None:
            raise HTTPException(status_code=404, detail="Pod not found")
        return {"pod_id": pod.id, "pod_name": pod.name, "members": [user.id for user in pod.members]}

    def recommend_employee(self, pod_id: int, recommended_user_id: int) -> dict:
        pod = self.db_session.query(Pod).filter(Pod.id == pod_id).first()
        if pod is None:
            raise HTTPException(status_code=404, detail="Pod not found")
        pod.members.append(self.db_session.query(User).filter(User.id == recommended_user_id).first())
        self.db_session.commit()
        return {"message": "Recommendation sent successfully"}

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_current_user(self, user_id: int) -> dict:
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": user.id, "name": user.name, "role": user.role}

class DashboardService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_dashboard_tiles(self) -> List[dict]:
        # TO DO: implement get dashboard tiles logic
        return []
```
Note that this code assumes that the `SessionLocal` class is defined in the `database` module, which is not provided in the original code. You will need to define this class to create a session maker for your database.