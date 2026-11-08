from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict


app=FastAPI()


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int

class UpdateUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: Optional[str] = None
    age: Optional[int] = None


users = {
    1: {
        "name":"Denis",
        "age":19
    }
}


UserIdPath = Annotated[int, Path(ge=1, le=100, description="User ID (1-100)")]


# HOME
@app.get("/")
def root():
    return {"message":"Hello!"}

# GET USER
@app.get("/user/{user_id}")
def get_user(user_id: UserIdPath):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

# CREATE USER
@app.post("/user/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id: UserIdPath , user: User):
    if user_id in users:
        raise HTTPException(status_code=409, detail="Users already exists!")
    users[user_id] = user.model_dump()
    return user

# UPDATE USER
@app.put("/user/{user_id}")
def update_user(user_id: UserIdPath, user: UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User is not here!")
    users[user_id].update(user.model_dump(exclude_unset=True))
    return users[user_id]

# DELETE USER
@app.delete("/user/{user_id}")
def delete_user(user_id: UserIdPath):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User is not here!")
    deleted_user = users.pop(user_id)
    return deleted_user

# SEARCH USER
@app.get("/user/search/")
def search_by_name(name: Optional[str] = None):
    if name == None:
        return {"message": "Name parameter is required!"}
    for user in users.values():
        if user["name"] == name:
            return name
    raise HTTPException(status_code=404, detail="User not found!") 