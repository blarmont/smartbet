# 💸 SmartBet Arbitrage Finder

![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Streamlit](https://img.shields.io/badge/built%20with-streamlit-red?logo=streamlit)
![Status](https://img.shields.io/badge/status-actively--maintained-brightgreen)

**By Blas Aramburu (2025)**

SmartBet is a Python-based arbitrage betting assistant that analyzes real-time odds from various sportsbooks using The Odds API to identify guaranteed profit opportunities. It calculates optimal stake distributions to lock in profits and includes both a CLI and GUI, along with a Raycast script for one-click top picks.

* Disclaimer: SmartBet is currently not connected to any betting accounts and data are samples. Please be aware that arbitrage betting may be subject to legal restrictions in your jurisdiction. It is your responsibility to ensure compliance with local laws and regulations regarding betting and gambling.

---

## 🎥 Demo

| CLI Mode                            | GUI Mode via Streamlit                   |
|------------------------------------|------------------------------------------|
| ![CLI Demo](https://raw.githubusercontent.com/YOUR_USERNAME/smartbet/main/demo/cli.gif) | ![GUI Demo](https://raw.githubusercontent.com/YOUR_USERNAME/smartbet/main/demo/gui.gif) |

> 🎬 You can generate these by screen recording and converting to GIF using [ezgif](https://ezgif.com/video-to-gif) or [Kap](https://getkap.co).

---

## 🚀 Features

- ✅ Scans sportsbook odds for arbitrage
- 🧠 Calculates mathematically guaranteed profits
- 💰 Optimizes bet sizing by bankroll
- 📦 Logs arbitrage to CSV for analysis
- 🖥️ Streamlit GUI with filtering and diagrams
- ⚡ Raycast script for daily one-click top picks

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/smartbet.git
cd smartbet
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --break-system-packages
```

Then rename the config file and add your API key:

```bash
cp config_template.py config.py
```

```python
# config.py
ODDS_API_KEY = "your_api_key_here"
```

---

## 🧪 CLI Usage

```bash
python core.py
```

Or with options:

```bash
python core.py --top 10 --bankroll 200 --sport soccer_epl --verbose
```

### 🏷️ CLI Flags

| Flag             | Description                                           | Default     |
|------------------|-------------------------------------------------------|-------------|
| `--top N`        | Show top N arbitrage picks                            | `5`         |
| `--bankroll AMT` | Total money to distribute across bets                 | `100`       |
| `--sport KEY`    | Limit results to one sport (e.g. `basketball_nba`)    | All sports  |
| `--verbose`      | Show extra math (implied probabilities, payouts)      | `False`     |
| `--show-skips`   | Print why a game was skipped                          | `False`     |

---

## 🖼️ GUI with Streamlit

Launch the visual interface:

```bash
streamlit run app.py
```

### GUI Features

- Selectable sport filter
- Adjustable bankroll and pick count
- 📊 Visual “How Arbitrage Works” tab with diagrams and explanations
- ⬇️ Automatically logs picks

---

## ⚡ Raycast Integration

Use `smartbet-raycast.py` inside [Raycast](https://raycast.com) to fetch daily arbitrage picks directly from your menu bar or hotkey.

### Setup Instructions

1. Place the script in your Raycast Scripts directory.
2. Edit this line to match your local project path:
   ```python
   sys.path.append("/Users/YOURNAME/Desktop/Codes/SmartBet")
   ```
3. Make it executable:
   ```bash
   chmod +x smartbet-raycast.py
   ```

### Optional Inputs (space-separated):

```bash
100 10 basketball_nba
```

- `100` = bankroll
- `10` = number of picks to show
- `basketball_nba` = sport key to limit to

---

## 📁 Project Structure

```
SmartBet/
├── core.py                   # CLI logic
├── app.py                    # Streamlit GUI
├── smartbet-raycast.py       # Raycast script
├── config.py                 # Your API key (ignored by Git)
├── config_template.py        # Placeholder config
├── arbitrage_log.csv         # Logs of all found arbitrages
├── requirements.txt          # Python dependencies
├── demo/                     # (Optional) CLI/GUI GIFs for README
│   ├── cli.gif
│   └── gui.gif
└── README.md
```

**.gitignore**
```bash
config.py
__pycache__/
*.pyc
arbitrage_log.csv
.env
```

---

## 🧼 Before Uploading to GitHub

- ❌ Remove or hide your real API key in `config.py`
- ✅ Use `config_template.py` in your repo
- ❌ Exclude logs containing personal betting info
- ✅ Replace local file paths with relative paths or placeholders

---

## 📬 Contact

Made with ☕ and math by **Blas Aramburu**

Have questions or want to collaborate?  
Reach out via GitHub or LinkedIn — I'm always down to talk about AI, betting algorithms, or pizza 🍕

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
