from pydantic import BaseModel


class SongResponse(BaseModel):
    id: int
    title: str
    filename: str
    filepath: str

    class Config:
        from_attributes = True