from fastapi import FastAPI, Request, status, HTTPException, Path, Body, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from Jinja_2 import templates

# Подготовка:
#     Используйте код из предыдущей задачи.
#     Скачайте заготовленные шаблоны для их дополнения.
#     Шаблоны оставьте в папке templates у себя в проекте.
#     Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.

app = FastAPI(debug=True)
templates = Jinja2Templates(directory='templates')

users = []

class User(BaseModel):
    id: int
    username: str
    age: int


#Измените и дополните ранее описанные CRUD запросы:

# Напишите новый запрос по маршруту '/':
#     Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
#     TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
#     а также передавать в него request и список users. Ключи в словаре для
#     передачи определите самостоятельно в соответствии с шаблоном.

@app.get('/')
async def det_all_message(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request":request, "users": users})


# Измените get запрос по маршруту '/user' на '/user/{user_id}':
#
#     Функция по этому запросу теперь принимает аргумент request и user_id.
#     Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
#     TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
#     а также передавать в него request и одного из пользователей - user.
#     Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.

@app.get('/user/{user_id}')
async def get_massages(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User not found')

# post запрос по маршруту '/user/{username}/{age}', теперь:
#     Добавляет в список users объект User.
#     id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
#     Все остальные параметры объекта User - переданные в функцию username и age соответственно.
#     В конце возвращает созданного пользователя.

@app.post('/user/{username}/{age}')
async def create_message(username: Annotated[str, Path(min_length=5,
                                             max_length=20,
                                             description='Enter username',
                                             example='UrbanUser')] ,
                        age: Annotated[int, Path(ge=18,
                                      le=120,
                                      description='Enter age',
                                      example='24'
                                      )]) -> User:

    if users:
        new_user = User(id=users[-1].id + 1, username=username, age=age)
    else:
        new_user = User(id=1, username=username, age=age)

    users.append(new_user)
    return new_user


# put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
#     Обновляет username и age пользователя, если пользователь с таким user_id
#     есть в списке users и возвращает его.
#     В случае отсутствия пользователя выбрасывается исключение HTTPException с
#     описанием "User was not found" и кодом 404.

@app.put('/user/{user_id}/{username}/{age}')
async def update_message(user_id: Annotated[int, Path(ge=1,
                                                      le=150,
                                                      description='Enter user_id',
                                                      example=1)],
                         age: Annotated[int, Path(ge=18,
                                                  le=120,
                                                  description='Enter age',
                                                  example='24'
                                                  )],
                         username_: Annotated[str, Body(min_length=5,
                                                        max_length=20,
                                                        description='Enter username',
                                                        example='UrbanUser')
                         ]) -> User:
    try:
        edit_user = users[user_id - 1]
        edit_user.age = age
        edit_user.username = username_
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

# delete запрос по маршруту '/user/{user_id}', теперь:
#     Удаляет пользователя, если пользователь с таким user_id
#     есть в списке users и возвращает его.
#     В случае отсутствия пользователя выбрасывается исключение
#     HTTPException с описанием "User was not found" и кодом 404.

@app.delete('/user/{user_id}')
async def delete_message(user_id: Annotated[int, Path(ge=1,
                                                      le=150,
                                                      description='Enter user_id',
                                                      example=1)]) -> User:
    try:
        edit_user = users[user_id - 1]
        users.pop(user_id - 1)
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')