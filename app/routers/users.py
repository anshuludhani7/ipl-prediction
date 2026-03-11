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
        {
            "request": request,
        },
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    pin: str = Form(...),
    db: Session = Depends(get_db),
):
    username_normalized = username.lower().strip()
    pin = pin.strip()

    if not username_normalized:
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Username is required.",
            },
            status_code=400,
        )

    if not (len(pin) == 4 and pin.isdigit()):
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "PIN must be exactly 4 digits.",
            },
            status_code=400,
        )

    user = (
        db.query(models.User)
        .filter(models.User.username == username_normalized)
        .first()
    )
    if user is None:
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "User not registered.",
            },
            status_code=400,
        )

    if user.pin != pin:
        return request.app.state.templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid PIN.",
            },
            status_code=400,
        )

    request.session["user_id"] = user.id

    return RedirectResponse(url="/matches", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

