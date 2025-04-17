#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title SmartBet Arbitrage
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 💸
# @raycast.packageName Betting Tools

# Documentation:
# @raycast.description Run SmartBet with bankroll + filters
# @raycast.author Blas Aramburu

# Raycast arguments
# @raycast.argument1 { "type": "text", "placeholder": "Bankroll", "optional": true }
# @raycast.argument2 { "type": "text", "placeholder": "Num Picks", "optional": true }
# @raycast.argument3 { "type": "text", "placeholder": "Sport (basketball_nba)", "optional": true }

import sys
from config import FOLDER_PATH
sys.path.append(FOLDER_PATH)

from core import get_odds_for_sport, find_arbitrage, SPORTS

# Read args from Raycast
args = sys.argv

# Defaults
bankroll = 100
top_n = 5
chosen_sport = None

# Safe parsing
try:
    if len(args) > 1 and args[1].strip():
        bankroll = float(args[1])
except ValueError:
    pass

try:
    if len(args) > 2 and args[2].strip():
        top_n = int(args[2])
except ValueError:
    pass

if len(args) > 3 and args[3].strip():
    chosen_sport = args[3].strip()

# Run arbitrage logic
all_opps = []
sports_to_check = [chosen_sport] if chosen_sport else SPORTS

for sport in sports_to_check:
    print(f"📦 {sport}")
    data = get_odds_for_sport(sport)
    opps = find_arbitrage(
        data,
        sport,
        verbose=False,
        show_skips=False,
        bankroll=bankroll  # no more min_profit
    )
    all_opps.extend(opps)

if not all_opps:
    print("\n🧊 No arbitrage opportunities found.")
else:
    sorted_opps = sorted(all_opps, key=lambda x: x["profit"], reverse=True)[:top_n]
    print(f"\n🔥 Top {len(sorted_opps)} Arbitrage Opportunities:\n")
    for opp in sorted_opps:
        print(f"🎯 {opp['desc']}")
        print(f"📌 {opp['team1']} @ {opp['book1']} (odds {opp['odds1']}) → Stake ${opp['stake1']}")
        print(f"📌 {opp['team2']} @ {opp['book2']} (odds {opp['odds2']}) → Stake ${opp['stake2']}")
        print(f"💰 Profit: ${opp['profit']:.2f} | Implied Prob: {opp['prob']:.2%}\n")
