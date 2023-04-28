from pydantic import BaseModel
from typing import Union
from typing import List

class Client(BaseModel):
      nome: str
      email: str
      numero_cellulare: str

class GeneralInformation(BaseModel):
      nome_progetto: str
      tipologia_abitazione: str
      eta_edificio: str
      metri_quadrati: str
      tipo_intervento: str

class Item(BaseModel):
    id: Union[int, None] = None
    name: str
    type: str
    description: str
    unit_of_measure: str
    quantity: int
    unit_price: float


class Quote(BaseModel):
    id: Union[int, None] = None
    title: str
    type: str
    items: List[Item]

class Project(BaseModel):
    creator_id: str
    status: str
    general_info: GeneralInformation
    client_info: Client
    client_mail: str
