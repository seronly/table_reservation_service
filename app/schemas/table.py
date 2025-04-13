from pydantic import BaseModel, ConfigDict, Field

class TableBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    seats: int = Field(ge=1)
    location: str = Field(min_length=1, max_length=200)

class TableCreate(TableBase):
    pass

class TableDelete(BaseModel):
    id: int

class Table(TableBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
