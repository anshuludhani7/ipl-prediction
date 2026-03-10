from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter(include_in_schema=False)


@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    db: Session = Depends(get_db),
):
    username = username.strip()
    if not username:
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Username is required.",
            },
            status_code=400,
        )

    user = (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )
    if user is None:
        user = models.User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

    request.session["user_id"] = user.id

    return RedirectResponse(url="/matches", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

