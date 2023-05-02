from pydantic import BaseModel
from typing import Union, List

class User(BaseModel):
    id: Union[int, None] = None
    name: str
    surname: str
    email: str
    isProfessional: bool
    business_type: Union[str, None] = None
    phone_number: Union[str, None] = None
    profile_picture: Union[str, None] = None
    company_name: Union[str, None] = None
    address: Union[str, None] = None
    city: Union[str, None] = None
    cap: Union[str, None] = None
    nation: Union[str, None] = None