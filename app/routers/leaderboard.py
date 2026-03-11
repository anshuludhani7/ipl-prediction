from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from .matches import get_current_user

router = APIRouter()


@router.get("/leaderboard")
def leaderboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/login", status_code=303)

    users = (
        db.query(models.User)
        .order_by(models.User.bankroll.desc(), models.User.username.asc())
        .all()
    )
    return request.app.state.templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "users": users,
            "user": user,
        },
    )

