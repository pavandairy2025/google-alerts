import feedparser
import hashlib
import os
from datetime import datetime, timezone

# 1) PUT YOUR GOOGLE ALERTS RSS LINK HERE
# Example: https://www.google.com/alerts/feeds/12345678901234567890/abcdefghijklmno
GOOGLE_ALERTS_FEED_URL = os.getenv("GOOGLE_ALERTS_FEED_URL")

STATE_FILE = "seen_ids.txt"


def load_seen_ids():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())


def save_seen_ids(ids):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        for _id in ids:
            f.write(_id + "\n")


def entry_id(entry):
    # Create a stable ID based on title + link
    raw = (entry.get("title", "") + entry.get("link", "")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main():
    if not GOOGLE_ALERTS_FEED_URL:
        raise ValueError("GOOGLE_ALERTS_FEED_URL is not set. Set it as an environment variable or GitHub Secret.")

    print(f"[{datetime.now(timezone.utc).isoformat()}] Fetching Google Alerts...")
    feed = feedparser.parse(GOOGLE_ALERTS_FEED_URL)

    if feed.bozo:
        print("Error parsing feed:", feed.bozo_exception)
        return

    seen = load_seen_ids()
    new_seen = set(seen)

    new_items = []

    for entry in feed.entries:
        eid = entry_id(entry)
        if eid not in seen:
            new_items.append(entry)
            new_seen.add(eid)

    if not new_items:
        print("No new alerts.")
    else:
        print(f"Found {len(new_items)} new alerts:\n")
        for e in new_items:
            print("Title:", e.get("title"))
            print("Link:", e.get("link"))
            print("Published:", e.get("published", "N/A"))
            print("-" * 60)

    # Save updated seen IDs so we don't repeat alerts
    save_seen_ids(new_seen)
    print("Done.")


if __name__ == "__main__":
    main()
