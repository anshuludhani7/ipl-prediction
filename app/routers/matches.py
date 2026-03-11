from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..utils import calculate_pools, calculate_multipliers

router = APIRouter()


def get_current_user(request: Request, db: Session) -> models.User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()


@router.get("/matches")
def list_matches(
    request: Request,
    db: Session = Depends(get_db),
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    matches = db.query(models.Match).order_by(models.Match.id.asc()).all()
    return request.app.state.templates.TemplateResponse(
        "matches.html",
        {
            "request": request,
            "matches": matches,
            "user": user,
        },
    )


@router.get("/matches/{match_id}")
def match_detail(
    match_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    bets = (
        db.query(models.Bet)
        .filter(models.Bet.match_id == match_id)
        .all()
    )
    pools = calculate_pools(bets)
    multipliers = calculate_multipliers(pools["W_A"], pools["W_B"])
    # Use naive UTC datetimes to match what's stored in SQLite
    now = datetime.utcnow()
    closed = match.prediction_deadline <= now

    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return request.app.state.templates.TemplateResponse(
        "match_detail.html",
        {
            "request": request,
            "match": match,
            "user": user,
            "bets": bets,
            "pools": pools,
            "multipliers": multipliers,
            "closed": closed,
        },
    )


@router.post("/matches/{match_id}/bet")
def place_bet(
    match_id: int,
    request: Request,
    team: str = Form(...),
    weight: int = Form(...),
    db: Session = Depends(get_db),
):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    # Use naive UTC datetimes to match what's stored in SQLite
    now = datetime.utcnow()
    if match.prediction_deadline <= now:
        return request.app.state.templates.TemplateResponse(
            "match_detail.html",
            {
                "request": request,
                "match": match,
                "user": user,
                "bets": match.bets,
                "pools": calculate_pools(match.bets),
                "multipliers": calculate_multipliers(
                    *calculate_pools(match.bets).values()
                ),
                "closed": True,
                "error": "Prediction window is closed.",
            },
            status_code=400,
        )

    team = team.upper()
    if team not in ("A", "B"):
        raise HTTPException(status_code=400, detail="Invalid team")

    if weight < 200 or weight > 2000:
        return request.app.state.templates.TemplateResponse(
            "match_detail.html",
            {
                "request": request,
                "match": match,
                "user": user,
                "bets": match.bets,
                "pools": calculate_pools(match.bets),
                "multipliers": calculate_multipliers(
                    *calculate_pools(match.bets).values()
                ),
                "closed": False,
                "error": "Bet weight must be between 200 and 2000.",
            },
            status_code=400,
        )

    # Check if there is an existing bet for this user and match
    existing_bet = (
        db.query(models.Bet)
        .filter(
            models.Bet.user_id == user.id,
            models.Bet.match_id == match.id,
        )
        .first()
    )

    if existing_bet:
        previous_weight = existing_bet.weight
        net_change = weight - previous_weight

        if net_change > 0 and user.bankroll < net_change:
            return request.app.state.templates.TemplateResponse(
                "match_detail.html",
                {
                    "request": request,
                    "match": match,
                    "user": user,
                    "bets": match.bets,
                    "pools": calculate_pools(match.bets),
                    "multipliers": calculate_multipliers(
                        *calculate_pools(match.bets).values()
                    ),
                    "closed": False,
                    "error": "Insufficient bankroll for updating bet.",
                },
                status_code=400,
            )

        existing_bet.team = team
        existing_bet.weight = weight

        # Adjust bankroll by the difference between new and previous weight
        if net_change > 0:
            user.bankroll -= net_change
        elif net_change < 0:
            user.bankroll += -net_change

        db.add(existing_bet)
    else:
        # New bet: require full bankroll coverage
        if user.bankroll < weight:
            return request.app.state.templates.TemplateResponse(
                "match_detail.html",
                {
                    "request": request,
                    "match": match,
                    "user": user,
                    "bets": match.bets,
                    "pools": calculate_pools(match.bets),
                    "multipliers": calculate_multipliers(
                        *calculate_pools(match.bets).values()
                    ),
                    "closed": False,
                    "error": "Insufficient bankroll.",
                },
                status_code=400,
            )

        bet = models.Bet(
            user_id=user.id,
            match_id=match.id,
            team=team,
            weight=weight,
        )
        user.bankroll -= weight
        db.add(bet)

    db.add(user)
    db.commit()

    return RedirectResponse(
        url=f"/matches/{match_id}",
        status_code=303,
    )

