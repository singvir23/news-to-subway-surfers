import requests
import csv
import time
from datetime import datetime, timedelta, date

# === TikTok API credentials (client credentials) ===
CLIENT_KEY = ""
CLIENT_SECRET = ""

# Token endpoint (note the trailing slash)
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

# Ask TikTok for these fields for each video
# voice_to_text = TikTok's own transcript field (when available)
VIDEO_FIELDS = (
    "id,username,video_description,like_count,view_count,voice_to_text"
)

VIDEO_QUERY_URL = (
    f"https://open.tiktokapis.com/v2/research/video/query/?fields={VIDEO_FIELDS}"
)

# === List of TikTok usernames to query ===
USERNAMES = [""]
# Complete list of usernames used: ['ridiculousstories1' 'redditnarrs' 'reddit_stories1110' 'aita.queen1'
#  'storytime_confessions' 'echo.stories.1' 'ranking649' '1ndonlydnice'
#  'untap_tales' 'redditdailyvid' 'aitaconfessionss' 'chavez_crystall'
#  'storiesq2' 'yankeereads' 'story_dive' 'cravexcharmedtale' 'dill73885'
#  'full_redd1ts' 'lawerence.mi' 'jkr7227']
# Output CSV
CSV_FILE = "tiktok_user_videos_and_transcripts3.csv"

MAX_RESULTS_PER_QUERY = 100   # up to 100 allowed
DELAY_BETWEEN_QUERIES = 2    # seconds


def get_access_token():
    """Get an app access token using client credentials."""
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    resp = requests.post(TOKEN_URL, headers=headers, data=data)

    try:
        resp.raise_for_status()
    except requests.HTTPError:
        print("Error getting token:", resp.status_code)
        print("Response body:", resp.text)
        raise

    token = resp.json()["access_token"]
    print("Access token obtained.")
    return token


def query_videos_by_username(token, username, max_count=MAX_RESULTS_PER_QUERY):
    """
    Query TikTok Research API for videos posted by a specific username,
    and request TikTok's voice_to_text transcript field.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Use last 7 days (you can increase up to 30)
    start_date = date(2025, 11, 1)
    end_date = date(2025, 11, 9)

    payload = {
        "query": {
            "and": [
                {
                    "operation": "EQ",
                    "field_name": "username",
                    "field_values": [username],
                },
                {
                    # optional filter: limit to US accounts
                    "operation": "IN",
                    "field_name": "region_code",
                    "field_values": ["US"],
                },
            ]
        },
        "start_date": start_date.strftime("%Y%m%d"),
        "end_date": end_date.strftime("%Y%m%d"),
        "max_count": max_count,
    }

    resp = requests.post(VIDEO_QUERY_URL, headers=headers, json=payload)

    if resp.status_code != 200:
        print(f"Failed for username '{username}': {resp.status_code}")
        try:
            print("Response JSON:", resp.json())
        except ValueError:
            print("Response body:", resp.text)
        return []

    data = resp.json()
    videos = data.get("data", {}).get("videos", [])
    print(f"Retrieved {len(videos)} videos for '{username}'")
    return videos


def save_to_csv(videos, filename=CSV_FILE):
    """
    Append video data (including transcripts) to a CSV file.
    """
    fieldnames = [
        "id",
        "username",
        "caption",
        "like_count",
        "view_count",
        "transcript",  # <- from voice_to_text
    ]

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header once if file is empty
        if f.tell() == 0:
            writer.writeheader()

        for v in videos:
            writer.writerow({
                "id": v.get("id"),
                "username": v.get("username"),
                "caption": v.get("video_description") or v.get("description"),
                "like_count": v.get("like_count"),
                "view_count": v.get("view_count"),
                "transcript": v.get("voice_to_text"),
            })


def main():
    token = get_access_token()

    for username in USERNAMES:
        videos = query_videos_by_username(token, username)
        if videos:
            save_to_csv(videos)
        time.sleep(DELAY_BETWEEN_QUERIES)

    print(f"Captions + transcripts saved to {CSV_FILE}")


if __name__ == "__main__":
    main()
