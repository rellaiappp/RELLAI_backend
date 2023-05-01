from pydantic import BaseModel
from typing import Union
from typing import List

class Invite(BaseModel):
    sender_id: str
    project_id: str
    receiver_mail: str
    user_role: str
    accepted: bool