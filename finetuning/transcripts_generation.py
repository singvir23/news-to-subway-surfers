import requests
import csv
import time
from datetime import datetime, timedelta, date

# ============================================================
# TikTok Video Transcript Scraper for Preselected Accounts
# ------------------------------------------------------------
# This script uses the TikTok Research API to:
#   1. Authenticate via client_credentials OAuth
#   2. Query specified TikTok usernames for videos posted
#   3. Request TikTok’s built-in "voice_to_text" transcript field
#   4. Save video metadata + transcripts into a CSV file
#
# The purpose is to gather transcripts from Reddit-style gameplay
# storytelling accounts to analyze content patterns.
# ===========================================================

# === TikTok API credentials (client credentials) ===
CLIENT_KEY = "awngsf2tw4uzr0fk"
CLIENT_SECRET = "Gvbz9rvgTzVKDR8wbKalrLkVcQI3xgHP"

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

# === List of TikTok usernames to scrape transcripts from ===
# These are creators posting Reddit-style gameplay/story videos
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
    # ------------------------------------------------------------
    # Request an OAuth "client_credentials" access token.
    # This token is needed for all subsequent API requests.
    # ------------------------------------------------------------

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
        # Prints error details if authentication fails
        print("Error getting token:", resp.status_code)
        print("Response body:", resp.text)
        raise

    token = resp.json()["access_token"]
    print("Access token obtained.")
    return token


def query_videos_by_username(token, username, max_count=MAX_RESULTS_PER_QUERY):
    # ------------------------------------------------------------
    # Queries TikTok’s Research API for videos posted by a specific
    # username within a specific date range.
    #
    # We also request TikTok’s auto-generated transcript field:
    #   - voice_to_text
    #
    # Returns a list of videos with metadata + transcripts.
    # ------------------------------------------------------------
    """
    Query TikTok Research API for videos posted by a specific username,
    and request TikTok's voice_to_text transcript field.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    
    # Date window for filtering videos (adjustable)
    # These dates currently sample a 1-week range, due to common 500 errors

    start_date = date(2025, 11, 1)
    end_date = date(2025, 11, 9)

    payload = {
        "query": {
            "and": [
                # Filter results by TikTok username
                {
                    "operation": "EQ",
                    "field_name": "username",
                    "field_values": [username],
                },
                {
                     # Optional: Force results to US region accounts only
                    "operation": "IN",
                    "field_name": "region_code",
                    "field_values": ["US"],
                },
            ]
        },
        # TikTok Research API requires YYYYMMDD date formatting
        "start_date": start_date.strftime("%Y%m%d"),
        "end_date": end_date.strftime("%Y%m%d"),
        "max_count": max_count,
    }

    resp = requests.post(VIDEO_QUERY_URL, headers=headers, json=payload)

    if resp.status_code != 200:
        # Print any errors so we know which account failed
        print(f"Failed for username '{username}': {resp.status_code}")
        try:
            print("Response JSON:", resp.json())
        except ValueError:
            print("Response body:", resp.text)
        return []

    data = resp.json()
    # Extract list of videos (empty list if none found)
    videos = data.get("data", {}).get("videos", [])
    print(f"Retrieved {len(videos)} videos for '{username}'")
    return videos


def save_to_csv(videos, filename=CSV_FILE):
    # ------------------------------------------------------------
    # Saves the extracted video information and transcripts to a
    # CSV file. Appends new results without overwriting existing
    # data.
    #
    # CSV columns:
    # id, username, caption, like_count, view_count, transcript
    # ------------------------------------------------------------
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

        # Each API video object becomes one CSV row
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
    # ------------------------------------------------------------
    # Main function:
    #   1. Authenticate with TikTok API
    #   2. Loop through each selected username
    #   3. Fetch their videos + transcripts
    #   4. Save all data to CSV
    # ------------------------------------------------------------
    token = get_access_token()

    for username in USERNAMES:
        videos = query_videos_by_username(token, username)
        if videos:
            save_to_csv(videos)
        # Delay helps prevent hitting TikTok API rate limits
        time.sleep(DELAY_BETWEEN_QUERIES)
        

    print(f"Captions + transcripts saved to {CSV_FILE}")


if __name__ == "__main__":
    # Call main
    main()
