# 🪙 CoinGecko Crypto & PKR Pulse

A beginner-friendly Python CLI application that fetches **live cryptocurrency prices in USD and PKR** (Pakistani Rupee), along with 24-hour percentage changes — all powered by the free [CoinGecko REST API](https://www.coingecko.com/en/api) (no API key needed).

---

## ✨ Features

| Feature | Description |
|---|---|
| **Live Market Dashboard** | View real-time USD & PKR prices + 24h % change for 5 major coins |
| **Custom Coin Lookup** | Search any coin by its CoinGecko ID (e.g. `dogecoin`, `cardano`) |
| **Crypto ↔ PKR/USD Converter** | Convert coin amounts to PKR/USD, or a PKR budget to crypto |
| **Snapshot & History** | Save timestamped price snapshots locally and view past records |
| **Graceful Error Handling** | 429 rate-limit messages, timeout handling, no crashes on network errors |

---

## 🗂 Project Structure

```
coin-gecko/
├── .env.example       # Configuration template (copy to .env to customise)
├── .gitignore         # Ignores .venv/, __pycache__/, .env, *.pyc, watchlist.json
├── requirements.txt   # Python dependencies
├── api_client.py      # CoinGecko API calls with timeout & error handling
├── storage.py         # JSON snapshot load/save
├── main.py            # Interactive CLI menu
└── README.md          # This file
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/zaynabhassan567/coin-gecko.git
cd coin-gecko
```

### 2. Create and activate a virtual environment
```bash
# Create the virtual environment
python3 -m venv .venv

# Activate it (macOS / Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure default coins
```bash
cp .env.example .env
# Then edit .env to change DEFAULT_COINS or VS_CURRENCIES if desired
```

### 5. Run the application
```bash
python main.py
```

---

## 🖥 Sample Terminal Output

### Main Menu
```
══════════════════════════════════════════════════════════════════════════════
              🪙  CoinGecko Crypto & PKR Pulse
           Live prices powered by CoinGecko Free API
══════════════════════════════════════════════════════════════════════════════

  MAIN MENU
  ──────────────────────────────
  1  →  Live Market Dashboard
  2  →  Custom Coin Lookup
  3  →  Crypto ↔ PKR / USD Converter
  4  →  Save Snapshot / View History
  5  →  Exit
  ──────────────────────────────

  Enter your choice (1–5): 1
```

### Live Market Dashboard (Option 1)
```
⏳  Fetching live prices from CoinGecko…

══════════════════════════════════════════════════════════════════════════════
              💹  LIVE CRYPTO MARKET DASHBOARD
══════════════════════════════════════════════════════════════════════════════
  COIN                        USD PRICE             PKR PRICE      24H CHANGE
──────────────────────────────────────────────────────────────────────────────
  Bitcoin      (BTC)         $88,245.00    Rs 24,620,440.00    ▲ +1.84%
  Ethereum     (ETH)          $3,120.50       Rs 870,699.50    ▲ +0.92%
  Solana       (SOL)            $198.30        Rs 55,345.80    ▼ -0.45%
  Tether       (USDT)            $1.00           Rs 279.12    ▲ +0.01%
  BNB          (BNB)            $612.00       Rs 170,829.60    ▲ +2.11%
══════════════════════════════════════════════════════════════════════════════
```

### Crypto → PKR Converter (Option 3)
```
  Your input: 0.25 bitcoin

⏳  Fetching live price for 'bitcoin'…

  ──────────────────────────────────────────────────
  Amount      : 0.25 BITCOIN
  = USD       : $22,061.25
  = PKR       : Rs 6,155,110.00
  ──────────────────────────────────────────────────
```

### PKR → Crypto Converter (Option 3)
```
  Your input: 100000 pkr dogecoin

⏳  Fetching live price for 'dogecoin'…

  ──────────────────────────────────────────────────
  Budget      : Rs 100,000.00
  Coin        : DOGECOIN
  You can buy : 2535.65480000 DOGECOIN
  ≈ USD value : $358.52
  ──────────────────────────────────────────────────
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `requests` | 2.32.3 | HTTP requests to CoinGecko API |
| `python-dotenv` | 1.0.1 | Load optional `.env` configuration |

---

## 📄 License

This project is for educational purposes.
