from fastapi import FastAPI
from .database import engine
from . import models
from .routers import societies, events, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# societies = [
#             {"name": "ABC1", "college_level": "True", "convenor": "qwerty1","gen_sec": "asdf1"},
#             {"name": "ABC2", "college_level": "False", "convenor": "qwerty2","gen_sec": "asdf2"},
#             {"name": "ABC3", "college_level": "True", "convenor": "qwerty3","gen_sec": "asdf3"}
# ]
    

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(societies.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(auth.router)