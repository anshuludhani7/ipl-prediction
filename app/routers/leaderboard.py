from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter()


@router.get("/leaderboard")
def leaderboard(
    request: Request,
    db: Session = Depends(get_db),
):
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
        },
    )

