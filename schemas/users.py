from fastapi import FastAPI, Path, Query
# import uvicorn
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

# app = FastAPI()

class Gender(str, Enum):
    male = "male"
    female = "female"

class Address(BaseModel):
    # default value(example value) 有 3 種寫法，一種是 examples=[""]，第二種則是 model_config = {}，第三種是寫在 Body 中
    # 優先順序依序為: Body(..., examples=[{}]) > model_config = {} > Field(..., examples=[])
    address: str = Field(..., examples=["2 Queen Street"])
    postcode: int = Field(..., examples=[5])

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [{
    #             "address": "3 Queen Street",
    #             "postcode": 10
    #         }]
    #     }
    # }

class UserModel(BaseModel):
    username: str
    description: Optional[str] = Field(None, max_length=10)
    gender: Gender
    address: Address

class ItemModel(BaseModel):
    name: str = Field(..., min_length=3)
    length: int
    features: List[str]
    # features: list