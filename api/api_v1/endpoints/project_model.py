from pydantic import BaseModel

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
    id: int | None = None
    name: str
    type: str
    description: str
    unit_of_measure: str
    quantity: int
    unit_price: float

class Quote(BaseModel):
    id: int | None = None
    title: str
    type: str
    items: list[Item]

class Project(BaseModel):
    creator_id: str
    status: str
    general_info: GeneralInformation
    client_info: Client
    client_mail: str
