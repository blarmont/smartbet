# ╔══════════════════════════════════════════════════════════════════╗
# ║       SmartBet Arbitrage Finder – By Blas Aramburu (2025)        ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║ Scans sports odds for arbitrage between sportsbooks using        ║
# ║ The Odds API. Calculates optimal bets to guarantee profit.       ║
# ║ Saves results to CSV and prints top picks.                       ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║ Usage:                                                           ║
# ║   python core.py                                                 ║
# ║   python core.py --top 5 --bankroll 100                          ║
# ║                                                                  ║
# ║ Options:                                                         ║
# ║   --top N            Show top N results (default: 5)             ║
# ║   --bankroll AMOUNT  Set total bankroll (default: 100)           ║
# ║   --sport KEY        Limit to a single sport (basketball_nba)     ║
# ║   --verbose          Show math for each opportunity              ║
# ║   --show-skips       Show why games were skipped                 ║
# ╚══════════════════════════════════════════════════════════════════╝


import requests
import csv
import argparse
from datetime import datetime
from config import ODDS_API_KEY

SPORTS = [
    "basketball_nba",
    "americanfootball_nfl",
    "soccer_epl",
    "baseball_mlb",
    "mma_mixed_martial_arts",
    "basketball_ncaab"
]

REGION = "us"
MARKET = "h2h"
bankroll = None  # Default total money you want to bet

def get_odds_for_sport(sport):
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        'apiKey': ODDS_API_KEY,
        'regions': REGION,
        'markets': MARKET,
        'oddsFormat': 'decimal'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        #print(f"❌ API Error for {sport}: {response.status_code} {response.text}")
        return []
    return response.json()

def calculate_bets(odds1, odds2, bankroll):
    implied1 = 1 / odds1
    implied2 = 1 / odds2
    total = implied1 + implied2
    stake1 = bankroll * (implied1 / total)
    stake2 = bankroll * (implied2 / total)
    guaranteed_return = stake1 * odds1  # or stake2 * odds2 (same)
    profit = guaranteed_return - (stake1 + stake2)
    return round(stake1, 2), round(stake2, 2), round(profit, 2), round(total, 4)

def log_to_csv(row):
    filename = "data/arbitrage_log.csv"
    header = ["timestamp", "sport", "team1", "team2", "odds1", "book1", "odds2", "book2", "stake1", "stake2", "profit", "total_prob"]
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

def find_arbitrage(odds_data, sport_name, verbose=False, show_skips=False, min_profit=0, bankroll=100):
    found = []
    for game in odds_data:
        try:
            teams = [game['home_team'], game['away_team']]
        except KeyError:
            # if show_skips:
                #print("⚠️ Skipped: missing home/away team")
            continue

        outcomes = {}
        for book in game['bookmakers']:
            if 'markets' not in book or not book['markets']:
                continue
            for outcome in book['markets'][0]['outcomes']:
                name = outcome['name']
                price = outcome['price']
                if name not in outcomes or price > outcomes[name]['price']:
                    outcomes[name] = {'price': price, 'book': book['title']}

        if len(outcomes) < 2:
        #     # if show_skips:
        #         #print(f"⚠️ Skipped: Only {len(outcomes)} outcome(s) found in {teams}")
            continue

        team1, team2 = list(outcomes.keys())[:2]
        odds1 = outcomes[team1]['price']
        odds2 = outcomes[team2]['price']
        stake1, stake2, profit, total_prob = calculate_bets(odds1, odds2, bankroll)

        if total_prob < 1 and profit >= min_profit:
            found.append({
                "sport": sport_name,
                "team1": team1, "team2": team2,
                "odds1": odds1, "odds2": odds2,
                "book1": outcomes[team1]['book'], "book2": outcomes[team2]['book'],
                "stake1": stake1, "stake2": stake2,
                "profit": profit,
                "prob": total_prob,
                "desc": f"{sport_name.upper()} — {teams[0]} vs {teams[1]}"
            })

            log_to_csv([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                sport_name,
                team1, team2,
                odds1, outcomes[team1]['book'],
                odds2, outcomes[team2]['book'],
                stake1, stake2,
                profit, total_prob
            ])
        elif verbose:
            prob1 = 1 / odds1
            prob2 = 1 / odds2
            #print(f"\n❌ {teams[0]} vs {teams[1]} — No arbitrage")
            #print(f"   - {team1} @ {odds1:.2f} → Implied prob: {prob1:.2%}")
            #print(f"   - {team2} @ {odds2:.2f} → Implied prob: {prob2:.2%}")
            #print(f"   - Combined: {prob1:.4f} + {prob2:.4f} = {prob1 + prob2:.4f} ({(prob1 + prob2):.2%})")
            # if min_profit:
            #     print(f"   - Profit < ${min_profit} (threshold)\n")

    return found

def print_results(opps, top_n, verbose):
    if not opps:
        #print("\n🧊 No arbitrage opportunities found today.")
        return

    opps.sort(key=lambda x: x["profit"], reverse=True)
    #print(f"\n🔥 Top {min(top_n, len(opps))} Arbitrage Opportunities:")
    for opp in opps[:top_n]:
        #print(f"\n🎯 {opp['desc']}")
        #print(f"📌 {opp['team1']} @ {opp['book1']} (odds {opp['odds1']}) → Bet ${opp['stake1']}")
        #print(f"📌 {opp['team2']} @ {opp['book2']} (odds {opp['odds2']}) → Bet ${opp['stake2']}")
        #print(f"💰 Profit: ${opp['profit']} | Combined Implied Probability: {opp['prob']:.2%}")
        if verbose:
            prob1 = 1 / opp['odds1']
            prob2 = 1 / opp['odds2']
            total = prob1 + prob2
            payout1 = opp['stake1'] * opp['odds1']
            payout2 = opp['stake2'] * opp['odds2']
            #print(f"🧮 Math Details:")
            #print(f"   - {opp['team1']} implied: {prob1:.4f} → payout: ${payout1:.2f}")
            #print(f"   - {opp['team2']} implied: {prob2:.4f} → payout: ${payout2:.2f}")
            #print(f"   - Total implied: {total:.4f} ({total:.2%})")

# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SmartBet Arbitrage Finder")
    parser.add_argument("--bankroll", type=float, default=100, help="Total bankroll to use for calculating stakes (default: 100)")
    parser.add_argument("--top", type=int, default=5, help="Number of top arbitrage picks to show (default: 5)")
    parser.add_argument("--verbose", action="store_true", help="Show detailed math for each opportunity")
    parser.add_argument("--show-skips", action="store_true", help="Print why games are skipped")
    parser.add_argument("--min-profit", type=float, default=0, help="Minimum profit to show arbitrage (default: 0)")

    args = parser.parse_args()
    bankroll = args.bankroll
    min_profit = args.min_profit

    all_opps = []
    for sport in SPORTS:
        #print(f"\n📦 Fetching odds for: {sport}")
        data = get_odds_for_sport(sport)
        opps = find_arbitrage(data, sport, verbose=args.verbose, show_skips=args.show_skips, min_profit=min_profit, bankroll=bankroll)
        all_opps.extend(opps)

    print_results(all_opps, top_n=args.top, verbose=args.verbose)
