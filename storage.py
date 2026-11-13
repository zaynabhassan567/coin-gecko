"""
storage.py
----------
Handles saving and loading timestamped price snapshots to/from watchlist.json.

The file format is a JSON array of snapshot objects, e.g.:
[
    {
        "timestamp": "2024-11-13T15:00:00Z",
        "prices": {
            "bitcoin": {"usd": 65000, "pkr": 18200000, "usd_24h_change": 1.23},
            ...
        }
    },
    ...
]
"""

import json
import os
from datetime import datetime, timezone

# Path to the local watchlist file (gitignored — stays on your machine only)
WATCHLIST_FILE = "watchlist.json"


def load_snapshots() -> list:
    """
    Load all saved price snapshots from watchlist.json.

    Returns:
        A list of snapshot dictionaries.
        Returns an empty list if the file does not exist, is empty, or is corrupted.
    """
    # If the file doesn't exist yet, return an empty list (nothing saved yet)
    if not os.path.exists(WATCHLIST_FILE):
        return []

    try:
        with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # Return empty list for empty files instead of crashing
            if not content:
                return []

            data = json.loads(content)

            # Make sure the file contains a list (not a corrupted format)
            if isinstance(data, list):
                return data
            else:
                print("⚠️  watchlist.json has an unexpected format. Resetting.")
                return []

    except json.JSONDecodeError:
        # File exists but isn't valid JSON (corrupted)
        print("⚠️  watchlist.json is corrupted and could not be read. Starting fresh.")
        return []


def save_snapshot(prices: dict) -> None:
    """
    Append a new timestamped price snapshot to watchlist.json.

    Parameters:
        prices : The price dictionary returned by api_client.fetch_prices()
                 e.g. {"bitcoin": {"usd": 65000, "pkr": 18200000, ...}, ...}
    """
    # Load existing snapshots first so we can append to them
    snapshots = load_snapshots()

    # Create a new snapshot with an ISO UTC timestamp
    new_snapshot = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prices": prices,
    }

    # Append the new snapshot to the list
    snapshots.append(new_snapshot)

    # Write the updated list back to the file with pretty formatting
    with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshots, f, indent=2, ensure_ascii=False)

    print(f"\n✅  Snapshot saved at {new_snapshot['timestamp']} → {WATCHLIST_FILE}")
