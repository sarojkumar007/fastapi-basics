from email.policy import default
from enum import Enum
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


# =============== Required Objects ========


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


items = [
    {'id': 1, 'name': 'John'},
    {'id': 2, 'name': 'Will'},
    {'id': 3, 'name': 'Sarah'},
    {'id': 4, 'name': 'Brad'},
]


class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None


#
class Image(BaseModel):
    caption: str
    # url: str = Field(...,pattern=r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*")
    url: HttpUrl


class NewItem(Item):
    tags: set[str] = set()  # behaves as is
    image: Image | None = None


# =========================================


@app.get('/')
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post():
    return {"message": "Hello World"}


#
# @app.get("/user")
# async def list_user():
#     return {
#         "message": "users",
#         "user": [1, 2, 3, 4]
#     }
#
#
# @app.get("/user/me")
# async def get_profile():
#     return {"msg": "This is my profile"}
#
#
# # with same endpoint having dynamic values, ( /user/me,/user/{id} ),
# # the custom comes first, then the dynamic route
#
# @app.get("/user/{user_id}")
# async def get_user(user_id: int):
#     return {"user_id": user_id}
#
#
# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     match food_name:
#         case FoodEnum.fruits:
#             return {"msg": "You are Healthy"}
#         case FoodEnum.vegetables:
#             return {"msg": "You are Organic"}
#         case FoodEnum.dairy:
#             return {"msg": "You are a Drink"}
#
#
# # Query Params
# @app.get("/items")
# async def get_items(skip: int = 0, limit: int = 10):
#     return items[skip: skip + limit]
#
#
# # Path and Query Params
# @app.get("/items/{item_id}")
# async def get_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {'item_id': item_id}
#     if q:
#         item.update({'q': q})
#     if not short:
#         item.update({'description': 'this is a very long paragraph with some long description'})
#     return item
#
# # item: is passed in Body, as it inherits from the BaseModel (pydantic)
# @app.post('/items/create')
# async def create_item(item: Item):
#     return item
#
#
# # String Validation and Query Params
# @app.get("/q")
# async def query_param(
#         q: str | None = Query(None, min_length=3, max_length=10),
#         required_query: str = Query(..., min_length=3, alias='rq', description='Required Query Example')
# ):
#     item = {'val': "Some Placeholder again for Testing", 'req': required_query}
#     if q:
#         item.update({"q": q})
#     return item
#
#
# # Hidden Query
# @app.get('/q/hidden')
# async def hidden_query_param(hq: str | None = Query(None, include_in_schema=False)):
#     if hq:
#         return {'hq': hq}
#     return {'msg': "No hidden query"}
#
#
# # Path Validation
# @app.get('/path/{path_id}')
# async def path_validation(
#         *,
#         path_id: int = Path(..., title="Path ID", gt=0),
#         q: str | None = Query(None, min_length=3),
#         rq: str  # ERR: if declared here, unless we use * as first argument i.e. make other params kwargs
# ):
#     res = {'path_id': path_id}
#     if q:
#         res.update({'q': q})
#     if rq:
#         res.update({'rq': rq})
#     return res


#

@app.put('/items/{item_id}')
async def update_item(
        *,
        item_id: int = Path(..., title='ID of the Item', ge=0),
        query: str | None = None,
        item: NewItem | None = Body(..., embed=True)
        # embedded, requires body to be passed by its key, embedded:true {item: {}}, embedded:false, {}
):
    res: list = [i for i in items if i['id'] == item_id]
    if query:
        res.append({'q': query})
    if item:
        res.append(item)
    return res


class ExtraItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    # class Config:
    #     schema_extra = {
    #         "example":
    #     }


@app.put('/extra/{item_id}')
async def extra_item(item_id: int, item: ExtraItem = Body(..., example={
    "name": "Foo",
    "description": "Example Description",
    "price": 123.45,
    "tax": 18.0
})):
    res = {"item_id": item_id, "item": item}
    return res
