from pydantic import BaseModel, ConfigDict

class TableBase(BaseModel):
    name: str
    seats: int
    location: str

class TableCreate(TableBase):
    pass

class TableDelete(BaseModel):
    id: int

class Table(TableBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
