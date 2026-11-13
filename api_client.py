"""
api_client.py
-------------
Handles all communication with the CoinGecko REST API.

Responsibilities:
- Build the request URL and parameters
- Send HTTP GET requests with a polite User-Agent header and a timeout
- Handle HTTP errors (including 429 rate limits) gracefully
- Return parsed price data as a dictionary, or None on failure
"""

import requests

# Base URL for CoinGecko simple price endpoint (no API key required)
BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

# Headers to identify our app politely to the CoinGecko server
HEADERS = {
    "User-Agent": "CoinGecko-PKR-Tracker/1.0",
    "Accept": "application/json",
}


def fetch_prices(coin_ids: list[str], currencies: list[str] = ["usd", "pkr"]) -> dict | None:
    """
    Fetch live prices for the given coin IDs in the specified currencies.

    Parameters:
        coin_ids   : List of CoinGecko coin IDs, e.g. ['bitcoin', 'ethereum']
        currencies : List of currency codes, e.g. ['usd', 'pkr']

    Returns:
        A dictionary of prices on success, e.g.:
            {
                "bitcoin": {"usd": 65000, "pkr": 18000000, "usd_24h_change": 1.23},
                ...
            }
        Returns None if the request fails for any reason.
    """

    # Build query parameters for the API
    params = {
        "ids": ",".join(coin_ids),          # e.g. "bitcoin,ethereum,solana"
        "vs_currencies": ",".join(currencies),  # e.g. "usd,pkr"
        "include_24hr_change": "true",       # also fetch 24-hour % change
    }

    try:
        # Make the GET request with a 10-second timeout so we never hang forever
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)

        # Handle HTTP 429 — CoinGecko rate limit (free tier allows ~10–30 req/min)
        if response.status_code == 429:
            print("\n⚠️  Rate limit reached. Please wait a few seconds and try again.")
            return None

        # Handle any other non-200 HTTP status code
        if response.status_code != 200:
            print(f"\n❌  Unexpected HTTP error: {response.status_code} — {response.reason}")
            return None

        # Parse and return JSON data
        data = response.json()

        # Validate that the API returned actual data
        if not data:
            print("\n⚠️  API returned an empty response. Check the coin IDs and try again.")
            return None

        return data

    except requests.ConnectionError:
        # No internet connection or DNS failure
        print("\n❌  Connection error. Please check your internet connection.")
        return None

    except requests.Timeout:
        # Request took longer than 10 seconds
        print("\n❌  Request timed out after 10 seconds. Try again shortly.")
        return None

    except requests.RequestException as e:
        # Catch-all for any other requests-related error
        print(f"\n❌  Network error: {e}")
        return None
