from fastapi import FastAPI
from .database import engine
from . import models
from .routers import societies, events, users, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static",
          html=True, follow_symlink=True), name="static")


@app.get("/")
def root():
    redirect_url = "http://localhost:8000/static"
    return RedirectResponse(redirect_url, status_code=303)


app.include_router(societies.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(auth.router)