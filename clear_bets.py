from app.database import SessionLocal, engine, Base
from app.models import Bet, User


def clear_bets():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        deleted = session.query(Bet).delete()
        reset = session.query(User).update({User.bankroll: 20000})
        session.commit()
        print(f"Deleted {deleted} bet(s) from bets table.")
        print(f"Reset bankroll to 20000 for {reset} user(s).")
    finally:
        session.close()


if __name__ == "__main__":
    clear_bets()

