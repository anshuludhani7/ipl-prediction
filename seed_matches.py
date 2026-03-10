from datetime import datetime, timedelta, timezone

from app.database import SessionLocal, engine
from app.models import Match
from app.database import Base


def create_sample_matches():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        if session.query(Match).count() >= 10:
            print("Matches already seeded, skipping.")
            return

        base_date = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

        fixtures = [
            ("Chennai Super Kings", "Mumbai Indians"),
            ("Royal Challengers Bengaluru", "Kolkata Knight Riders"),
            ("Rajasthan Royals", "Sunrisers Hyderabad"),
            ("Punjab Kings", "Delhi Capitals"),
            ("Lucknow Super Giants", "Gujarat Titans"),
            ("Mumbai Indians", "Royal Challengers Bengaluru"),
            ("Kolkata Knight Riders", "Chennai Super Kings"),
            ("Sunrisers Hyderabad", "Punjab Kings"),
            ("Delhi Capitals", "Rajasthan Royals"),
            ("Gujarat Titans", "Lucknow Super Giants"),
        ]

        matches: list[Match] = []
        for i, (team_a, team_b) in enumerate(fixtures):
            start_time = base_date + timedelta(hours=24 * (i + 1))
            prediction_deadline = start_time - timedelta(hours=2)
            matches.append(
                Match(
                    team_a=team_a,
                    team_b=team_b,
                    start_time=start_time,
                    prediction_deadline=prediction_deadline,
                )
            )

        session.add_all(matches)
        session.commit()
        print(f"Inserted {len(matches)} sample matches.")
    finally:
        session.close()


if __name__ == "__main__":
    create_sample_matches()

