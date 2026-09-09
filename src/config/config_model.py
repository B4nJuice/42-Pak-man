from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    seed: int = Field(default=0)