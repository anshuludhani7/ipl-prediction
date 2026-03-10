Build a mobile-friendly web app for an IPL prediction game. 

Technology stack: 
- Python 
- FastAPI 
- SQLite database 
- Jinja2 HTML templates 

Players: 
- Around 10 players 
- Each player starts with bankroll = 20000 

Matches: 
- IPL matches stored in database with prediction deadline 
- Predictions close before the deadline 

Betting rules: 
- Player chooses a team 
- Bet weight between 200 and 2000 
- Bet amount deducted from bankroll 

Market model: 
Pari-mutuel pool 

Definitions: 
W_A = total weight on Team A 
W_B = total weight on Team B 
Pool = W_A + W_B 

Multipliers: 
multiplier_A = Pool / W_A 
multiplier_B = Pool / W_B 

Payout: payout = bet_weight × multiplier 

Features required: 
- Match list page 
- Prediction page 
- Live odds display 
- Leaderboard page 
- Bet history page UI must be simple and mobile friendly.