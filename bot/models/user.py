from typing import Optional
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: Optional[int] = None
    tg_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    language: str = "uz"
    data: dict = {}

    model_config = ConfigDict(from_attributes=True)
