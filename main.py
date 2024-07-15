from fastapi import FastAPI, Path, Query, Body
import uvicorn
# from enum import Enum
from typing import Optional
# from pydantic import BaseModel
from schemas.users import Gender, UserModel, ItemModel

app = FastAPI()

# class Gender(str, Enum):
#     male = "male"
#     female = "female"

# class UserModel(BaseModel):
#     username: str
#     description: Optional[str] = "default"
#     gender: Gender


@app.get("/")
async def index():
    return {"context":  "Hello World"}
@app.get("/helloworld")
async def helloworld():
    return {"context": "Hi"}
@app.get("/users/current")
async def get_current_user():
    return {'user': 'This is the current user!'}


# 1.1 path params (路徑參數): 直接將參數輸入成網址
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {'user': f'This user is {user_id}'}
@app.get("/students/{gender}")
async def get_students_gender(gender: Gender):
    return {'student': f'This student is {gender.value}'}
# 1.2 param validation (路徑參數驗證)
@app.get("/users/{user_id}")
# ge: greater equal (">=")  le: less equal ("<=")  gt: greater than (">")
async def user_id(user_id: int = Path(..., title="user id", ge=0, le=1000)):
    return {"user": f"This is {user_id} user!"}
@app.get("/books/{book_name}")
async def book_name(book_name: str = Path(..., title="Books Name", min_length=3, max_length=10)):
    return {"book name": f"The book name is {book_name}"}


# 2.1 query params (查詢參數): 在網址後面接上 "?page_size=10&page_index=10" 即稱之
@app.get("/pages")
async def get_page_info(page_size: int, page_index: Optional[int] = 20):
    return {'page info': f'The page size is {page_size} and the page index is {page_index}'}
# 2.2 query validation (路徑查詢驗證)，和 params validation 之間的差別就是 query 可以有預設值，而 params 則只有 "..."
@app.get("/user")
# alias: 別名參數
async def user_id(user_id: int = Query(1, alias="user-id", title="user id", ge=1, le=1000)):
    return {"user": f"This is the {user_id} user!!!"}


# path params + query params
@app.get("/user/{user_id}")
async def get_user_friends_info(user_id: int, friend_age: Optional[int] = 21):
    return {'friend info': f'The user {user_id} friend age is {friend_age}'}


# 3. request body (請求體): 使用到 pydantic 中的任何 model 即稱之
@app.post("/createUser")
async def create_user(user_model: UserModel):
    print(user_model.username)
    user_dict = user_model.model_dump()
    return user_dict
@app.put("/updateUser/{user_id}")
async def update_user(user_id: int, user_model: UserModel):
    print(user_model.username)
    user_dict = user_model.model_dump()
    user_dict.update({ 'id': user_id })
    return user_dict
@app.put("/carts/{cart_id}")
async def update_cart(*, cart_id: int, user: UserModel = Body(..., examples=[{"username": "Wayne"}]), item: ItemModel, count: int = Body(..., ge=1, le=10)):
    print(user.username)
    print(item.name)
    result_dict = {
        "cartid": cart_id,
        "username": user.username,
        "itemname": item.name
    }
    return result_dict

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)