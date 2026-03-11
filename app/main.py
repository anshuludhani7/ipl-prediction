from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from .database import Base, engine, get_db
from .routers import bets, leaderboard, matches, users


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key="replace-with-random-secret",
    max_age=60 * 60 * 24 * 7,
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.state.templates = templates

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(users.router)
app.include_router(matches.router)
app.include_router(bets.router)
app.include_router(leaderboard.router)


@app.get("/", include_in_schema=False)
def root(request: Request, db=Depends(get_db)):
    if request.session.get("user_id"):
        return RedirectResponse(url="/matches", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

