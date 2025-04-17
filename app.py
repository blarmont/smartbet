import streamlit as st
from core import get_odds_for_sport, find_arbitrage, SPORTS

# Emoji-labeled sport names
SPORTS_MAP = {
    "basketball_nba": "🏀 NBA",
    "americanfootball_nfl": "🏈 NFL",
    "soccer_epl": "⚽ EPL",
    "baseball_mlb": "⚾ MLB",
    "mma_mixed_martial_arts": "🥋 MMA",
    "basketball_ncaab": "🏀 NCAAB"
}

# Reverse lookup
SPORTS_NAMES = list(SPORTS_MAP.values())
SPORT_KEY_FROM_NAME = {v: k for k, v in SPORTS_MAP.items()}

st.set_page_config(page_title="SmartBet Arbitrage", layout="wide")

# Tabs for function and info
tab1, tab2 = st.tabs(["📈 Arbitrage Finder", "📘 How Arbitrage Works"])

with tab1:
    st.title("💸 SmartBet Arbitrage Finder")
    st.markdown("Find real-time arbitrage opportunities between sportsbooks.")

    # Sidebar
    st.sidebar.header("Settings")
    bankroll = st.sidebar.number_input("💰 Bankroll", min_value=10.0, value=100.0, step=10.0)
    top_n = st.sidebar.slider("📊 Top N Picks", min_value=1, max_value=50, value=5)
    sport_display = st.sidebar.selectbox("🎯 Sport", ["All"] + SPORTS_NAMES)
    verbose_mode = st.sidebar.checkbox("🔍 Show Detailed Math")
    show_skips = st.sidebar.checkbox("⚠️ Show Skipped Games")

    # Translate display name to key
    sport_key = SPORT_KEY_FROM_NAME.get(sport_display)

    all_opps = []
    sports_to_check = [sport_key] if sport_key else SPORTS



    for sport in sports_to_check:
        st.subheader(f"📦 Odds from: `{SPORTS_MAP.get(sport, sport)}`")
        data = get_odds_for_sport(sport)
        opps = find_arbitrage(
            data,
            sport,
            verbose=False,
            show_skips=show_skips,
            bankroll=bankroll,
            min_profit=0
        )
        all_opps.extend(opps)

    if not all_opps:
        st.warning("🧊 No arbitrage opportunities found.")
    else:
        sorted_opps = sorted(all_opps, key=lambda x: x["profit"], reverse=True)[:top_n]
        st.success(f"✅ Found {len(sorted_opps)} arbitrage opportunities")

        for i, opp in enumerate(sorted_opps, 1):
            st.markdown(f"---\n### {i}. {opp['desc']}")
            st.markdown(f"**{opp['team1']}** @ {opp['book1']} (odds `{opp['odds1']}`) → Bet: `${opp['stake1']}`")
            st.markdown(f"**{opp['team2']}** @ {opp['book2']} (odds `{opp['odds2']}`) → Bet: `${opp['stake2']}`")
            st.markdown(f"💰 **Profit**: `${opp['profit']}` | 🧮 Total Implied Probability: `{opp['prob']:.2%}`")

            if verbose_mode or st.toggle(f"🔬 Show Math for {opp['team1']} vs {opp['team2']}", key=opp['desc']):
                prob1 = 1 / opp['odds1']
                prob2 = 1 / opp['odds2']
                payout1 = opp['stake1'] * opp['odds1']
                payout2 = opp['stake2'] * opp['odds2']
                total_prob = prob1 + prob2

                st.markdown("#### 📐 Math Breakdown")
                st.markdown(f"- **{opp['team1']}** → Implied: `{prob1:.4f}` → Payout: `${payout1:.2f}`")
                st.progress(min(prob1, 1.0), text=f"{opp['team1']}: {prob1:.2%}")
                st.markdown(f"- **{opp['team2']}** → Implied: `{prob2:.4f}` → Payout: `${payout2:.2f}`")
                st.progress(min(prob2, 1.0), text=f"{opp['team2']}: {prob2:.2%}")
                st.markdown(f"- 📊 Combined: `{total_prob:.4f}` → `{total_prob:.2%}`")

with tab2:
    st.title("📘 How Arbitrage Betting Works")
    st.markdown("""
    **Arbitrage betting** (also called "sure betting") is a risk-free betting strategy that guarantees a profit regardless of the outcome by exploiting differences in odds offered by different bookmakers.

    ---
    ### 🔢 Example
    Suppose two sportsbooks offer the following odds for a match:
    - Book A: Team A at 2.10
    - Book B: Team B at 2.10

    You bet:
    - `$47.62` on Team A
    - `$47.62` on Team B

    Total bet: `$95.24`  
    Guaranteed return: `$100.00`  
    **Profit:** `$4.76`

    ---
    ### 🎯 Math Behind It
    - Implied Probability = `1 / odds`
    - If the sum of probabilities across outcomes `< 1`, an arbitrage opportunity exists.
    
    - Example:  
      `1/2.10 + 1/2.10 = 0.476 + 0.476 = 0.952 (< 1.00)`

    ---
    """)
