from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from .matches import get_current_user

router = APIRouter()


@router.get("/bets")
def bet_history(
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(url="/login", status_code=303)

    bets = (
        db.query(models.Bet)
        .filter(models.Bet.user_id == user.id)
        .order_by(models.Bet.id.desc())
        .all()
    )

    ist = ZoneInfo("Asia/Kolkata")
    for bet in bets:
        if bet.created_at:
            bet.created_at_ist = bet.created_at.astimezone(ist)

    return request.app.state.templates.TemplateResponse(
        "bet_history.html",
        {
            "request": request,
            "user": user,
            "bets": bets,
        },
    )

