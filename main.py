"""
main.py
-------
CoinGecko Crypto & PKR Pulse — Interactive CLI Application

This program fetches live cryptocurrency prices from the CoinGecko free API
and displays them in a formatted terminal table. It also supports custom coin
lookups, a PKR/USD converter, and saving timestamped price snapshots locally.

Usage:
    python main.py

Requirements:
    - Python 3.10+
    - requests library (install via: pip install -r requirements.txt)
"""

import os
from api_client import fetch_prices
from storage import load_snapshots, save_snapshot

# ── Default coins shown on the Live Market Dashboard ──────────────────────────
DEFAULT_COINS = ["bitcoin", "ethereum", "solana", "tether", "binancecoin"]

# ── Friendly display names for the dashboard table ────────────────────────────
COIN_DISPLAY_NAMES = {
    "bitcoin":     "Bitcoin      (BTC)",
    "ethereum":    "Ethereum     (ETH)",
    "solana":      "Solana       (SOL)",
    "tether":      "Tether       (USDT)",
    "binancecoin": "BNB          (BNB)",
}

# ─────────────────────────────────────────────────────────────────────────────
# FORMATTING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fmt_usd(amount: float) -> str:
    """Format a number as USD with commas and 2 decimal places. e.g. $88,120.00"""
    return f"${amount:,.2f}"


def fmt_pkr(amount: float) -> str:
    """Format a number as PKR with commas and 2 decimal places. e.g. Rs 24,500,120.50"""
    return f"Rs {amount:,.2f}"


def fmt_change(change: float | None) -> str:
    """
    Format a 24h % change value with a +/- indicator and colour hint arrow.
    Returns '  N/A' if the value is None.
    """
    if change is None:
        return "  N/A "
    sign = "+" if change >= 0 else ""
    arrow = "▲" if change >= 0 else "▼"
    return f"{arrow} {sign}{change:.2f}%"


def separator(char: str = "─", width: int = 78) -> str:
    """Return a horizontal separator line."""
    return char * width


# ─────────────────────────────────────────────────────────────────────────────
# OPTION 1 — LIVE MARKET DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def display_price_table(prices: dict) -> None:
    """
    Print a formatted table of live crypto prices.

    Parameters:
        prices : Dictionary returned by fetch_prices(), keyed by coin ID.
    """
    print("\n" + separator("═"))
    print(f"{'  💹  LIVE CRYPTO MARKET DASHBOARD':^78}")
    print(separator("═"))
    print(f"  {'COIN':<22}{'USD PRICE':>16}{'PKR PRICE':>22}{'24H CHANGE':>14}")
    print(separator())

    for coin_id, data in prices.items():
        # Retrieve display name (fallback to raw ID if not in our map)
        name = COIN_DISPLAY_NAMES.get(coin_id, coin_id.capitalize())

        usd_price  = data.get("usd", 0)
        pkr_price  = data.get("pkr", 0)
        change_24h = data.get("usd_24h_change")

        print(
            f"  {name:<22}"
            f"{fmt_usd(usd_price):>16}"
            f"{fmt_pkr(pkr_price):>22}"
            f"{fmt_change(change_24h):>14}"
        )

    print(separator("═"))


def option_live_dashboard() -> dict | None:
    """Fetch and display the live market dashboard for default coins."""
    print("\n⏳  Fetching live prices from CoinGecko…")
    prices = fetch_prices(DEFAULT_COINS)

    if prices is None:
        print("❌  Could not fetch market data. Please try again.")
        return None

    display_price_table(prices)
    return prices   # Return so Option 4 can save it without re-fetching


# ─────────────────────────────────────────────────────────────────────────────
# OPTION 2 — CUSTOM COIN LOOKUP
# ─────────────────────────────────────────────────────────────────────────────

def option_custom_coin() -> None:
    """Let the user look up any coin by its CoinGecko ID."""
    print("\n" + separator())
    print("  🔍  CUSTOM COIN LOOKUP")
    print(separator())
    print("  Enter the CoinGecko coin ID (e.g. dogecoin, cardano, ripple, polkadot)")
    coin_id = input("  Coin ID: ").strip().lower()

    if not coin_id:
        print("  ⚠️  No coin ID entered. Returning to menu.")
        return

    print(f"\n⏳  Fetching data for '{coin_id}'…")
    prices = fetch_prices([coin_id])

    if prices is None:
        return   # Error message already printed in api_client.py

    if coin_id not in prices:
        print(f"\n⚠️  '{coin_id}' was not found. Check the spelling and try again.")
        print("    Tip: Use the exact CoinGecko ID (e.g. 'shiba-inu', not 'shib').")
        return

    data = prices[coin_id]
    usd  = data.get("usd", 0)
    pkr  = data.get("pkr", 0)
    chg  = data.get("usd_24h_change")

    print(f"\n  {'─'*40}")
    print(f"  Coin    : {coin_id.upper()}")
    print(f"  USD     : {fmt_usd(usd)}")
    print(f"  PKR     : {fmt_pkr(pkr)}")
    print(f"  24h Chg : {fmt_change(chg)}")
    print(f"  {'─'*40}")


# ─────────────────────────────────────────────────────────────────────────────
# OPTION 3 — CRYPTO ↔ PKR / USD CONVERTER
# ─────────────────────────────────────────────────────────────────────────────

def convert_currency() -> None:
    """
    Interactive converter:
      • Coin amount → PKR and USD  (e.g. '0.25 bitcoin')
      • PKR budget  → how much crypto it buys  (e.g. '100000 PKR dogecoin')
    """
    print("\n" + separator())
    print("  💱  CRYPTO ↔ PKR / USD CONVERTER")
    print(separator())
    print("  Mode A — Coin → PKR/USD  : Enter coin amount and ID")
    print("           Example: 0.25 bitcoin")
    print("  Mode B — PKR → Crypto    : Enter PKR amount, then coin ID")
    print("           Example: 100000 PKR dogecoin")
    print()

    raw = input("  Your input: ").strip().lower()
    parts = raw.split()

    # ── Mode B: "100000 pkr dogecoin" ──────────────────────────────────────
    if len(parts) == 3 and parts[1] == "pkr":
        try:
            pkr_budget = float(parts[0].replace(",", ""))
        except ValueError:
            print("  ❌  Invalid PKR amount. Please enter a number.")
            return

        coin_id = parts[2]
        print(f"\n⏳  Fetching live price for '{coin_id}'…")
        prices = fetch_prices([coin_id])

        if prices is None or coin_id not in prices:
            print(f"  ❌  Could not find data for '{coin_id}'.")
            return

        pkr_price = prices[coin_id].get("pkr", 0)
        usd_price = prices[coin_id].get("usd", 0)

        if pkr_price == 0:
            print("  ❌  PKR price is zero — cannot convert.")
            return

        crypto_amount = pkr_budget / pkr_price
        equivalent_usd = crypto_amount * usd_price

        print(f"\n  {'─'*50}")
        print(f"  Budget      : {fmt_pkr(pkr_budget)}")
        print(f"  Coin        : {coin_id.upper()}")
        print(f"  You can buy : {crypto_amount:.8f} {coin_id.upper()}")
        print(f"  ≈ USD value : {fmt_usd(equivalent_usd)}")
        print(f"  {'─'*50}")

    # ── Mode A: "0.25 bitcoin" ─────────────────────────────────────────────
    elif len(parts) == 2:
        try:
            amount = float(parts[0].replace(",", ""))
        except ValueError:
            print("  ❌  Invalid amount. Please enter a number followed by a coin ID.")
            return

        coin_id = parts[1]
        print(f"\n⏳  Fetching live price for '{coin_id}'…")
        prices = fetch_prices([coin_id])

        if prices is None or coin_id not in prices:
            print(f"  ❌  Could not find data for '{coin_id}'.")
            return

        usd_price = prices[coin_id].get("usd", 0)
        pkr_price = prices[coin_id].get("pkr", 0)

        total_usd = amount * usd_price
        total_pkr = amount * pkr_price

        print(f"\n  {'─'*50}")
        print(f"  Amount      : {amount} {coin_id.upper()}")
        print(f"  = USD       : {fmt_usd(total_usd)}")
        print(f"  = PKR       : {fmt_pkr(total_pkr)}")
        print(f"  {'─'*50}")

    else:
        print("  ❌  Unrecognised format. Try '0.5 bitcoin' or '50000 pkr ethereum'.")


# ─────────────────────────────────────────────────────────────────────────────
# OPTION 4 — SAVE SNAPSHOT & VIEW HISTORY
# ─────────────────────────────────────────────────────────────────────────────

def option_snapshot(last_prices: dict | None) -> None:
    """
    Save the most recently fetched prices to watchlist.json,
    then offer to show saved snapshot history.

    Parameters:
        last_prices : The price dict from the last dashboard fetch, or None.
    """
    print("\n" + separator())
    print("  💾  SNAPSHOT & HISTORY")
    print(separator())

    # ── Save ────────────────────────────────────────────────────────────────
    if last_prices:
        save_snapshot(last_prices)
    else:
        print("  ℹ️  No prices loaded yet. Fetching dashboard prices to save…")
        last_prices = fetch_prices(DEFAULT_COINS)
        if last_prices:
            save_snapshot(last_prices)
        else:
            print("  ❌  Could not fetch prices. Snapshot not saved.")

    # ── View History ────────────────────────────────────────────────────────
    print()
    view = input("  View saved snapshot history? (y/n): ").strip().lower()
    if view != "y":
        return

    snapshots = load_snapshots()
    if not snapshots:
        print("  ℹ️  No snapshots saved yet.")
        return

    print(f"\n  Found {len(snapshots)} saved snapshot(s):\n")
    for i, snap in enumerate(snapshots, start=1):
        ts = snap.get("timestamp", "unknown time")
        print(f"  ── Snapshot #{i}  [{ts}] ──")
        for coin, data in snap.get("prices", {}).items():
            usd = data.get("usd", 0)
            pkr = data.get("pkr", 0)
            print(f"     {coin.upper():<15} {fmt_usd(usd):>14}  {fmt_pkr(pkr):>22}")
        print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main_menu() -> None:
    """
    Display the interactive main menu and dispatch to the chosen option.
    Keeps looping until the user selects Option 5 (Exit).
    """
    # Store the last-fetched prices so Option 4 can save without re-fetching
    last_prices: dict | None = None

    print("\n" + separator("═"))
    print(f"{'  🪙  CoinGecko Crypto & PKR Pulse':^78}")
    print(f"{'  Live prices powered by CoinGecko Free API':^78}")
    print(separator("═"))

    while True:
        print("\n  MAIN MENU")
        print("  " + "─" * 30)
        print("  1  →  Live Market Dashboard")
        print("  2  →  Custom Coin Lookup")
        print("  3  →  Crypto ↔ PKR / USD Converter")
        print("  4  →  Save Snapshot / View History")
        print("  5  →  Exit")
        print("  " + "─" * 30)

        choice = input("\n  Enter your choice (1–5): ").strip()

        if choice == "1":
            fetched = option_live_dashboard()
            if fetched:
                last_prices = fetched   # Remember for snapshot saving

        elif choice == "2":
            option_custom_coin()

        elif choice == "3":
            convert_currency()

        elif choice == "4":
            option_snapshot(last_prices)

        elif choice == "5":
            print("\n  👋  Thank you for using CoinGecko PKR Pulse. Goodbye!\n")
            break

        else:
            print("  ⚠️  Invalid choice. Please enter a number between 1 and 5.")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main_menu()
