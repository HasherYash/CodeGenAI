Here is the service layer code based on the provided requirements:

```
from typing import List
from sqlalchemy.orm import Session
from .models import Leave, Pod, User
from .schemas import LeaveApplyRequest, LeaveApproveRequest, PodRecommendationRequest

class LeaveService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def apply_for_leave(self, leave_apply_request: LeaveApplyRequest) -> dict:
        leave = Leave(start_date=leave_apply_request.start_date, end_date=leave_apply_request.end_date, reason=leave_apply_request.reason, status='pending')
        self.db_session.add(leave)
        self.db_session.commit()
        return {"message": "Leave applied successfully", "status": "pending"}

    def approve_leave(self, leave_id: int, leave_approve_request: LeaveApproveRequest) -> dict:
        leave = self.db_session.query(Leave).filter(Leave.id == leave_id).first()
        if leave:
            leave.status = leave_approve_request.status
            self.db_session.commit()
            return {"message": "Leave approved successfully", "status": "approved"}
        else:
            raise HTTPException(status_code=404, detail="Leave not found")

class PodService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_pod_details(self, pod_id: int) -> dict:
        pod = self.db_session.query(Pod).filter(Pod.id == pod_id).first()
        if pod:
            return {"pod_id": pod_id, "pod_name": pod.name, "members": pod.members}
        else:
            raise HTTPException(status_code=404, detail="Pod not found")

    def recommend_employee(self, pod_id: int, pod_recommendation_request: PodRecommendationRequest) -> dict:
        # Recommend employee logic
        return {"message": "Employee recommended successfully"}

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_current_user(self, token: str) -> dict:
        # Fetch current user details logic
        return {"id": 1, "name": "", "role": "general_user"}
```