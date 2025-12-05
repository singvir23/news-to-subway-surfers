


# TikTok Transcript Scraper

To build a dataset of 500+ videos, we wrote transcripts_generation.py. It gathers video metadata such as video IDs, usernames, captions, like counts, and view counts while also extracting TikTok’s built-in voice_to_text transcripts when available. The scraper compiles all results into a CSV file, making it a practical resource for researchers and developers working on content analysis, speech-to-text datasets, or engagement studies.

This script uses the **TikTok Research API** to fetch video metadata and transcripts from preselected TikTok accounts, specifically creators posting **Reddit-style gameplay or storytelling videos**.  

It collects:

- Video IDs  
- Usernames  
- Captions / descriptions  
- Like counts  
- View counts  
- **TikTok's built-in `voice_to_text` transcripts** (when available)  

All results are saved to a CSV file for further analysis.

---

## Built-in Modules Used

- `csv`  
- `datetime`  
- `time`  

---

## Functions 
### 1. get_access_token() (Line 52)

This function handles authentication with the TikTok Research API.
It sends your client_key and client_secret to TikTok’s OAuth token endpoint using the client credentials grant type. If the credentials are valid, TikTok returns a temporary access token. That token is required for all other API calls. If authentication fails, the function prints the error and stops the program so you don’t continue with invalid credentials.

### 2. query_videos_by_username(token, username, max_count) (Line 82)

This function retrieves videos posted by a specific TikTok user.
1. It builds a request that filters videos by:
- username
- region (US)
- a date range for when the videos were posted
2. It includes the token from get_access_token() in the request headers so the API recognizes the call as authorized.
3. It sends the request to TikTok’s Video Query API, asking for fields such as caption, like count, view count, and TikTok’s auto-generated transcript (voice_to_text).
4. If TikTok returns an error, it prints the response so you can see what went wrong and returns an empty list.
5. If the request succeeds, it extracts the list of videos from the JSON response and returns it.

### 3. save_to_csv(videos, filename) (Line 149)
This function takes the list of videos returned from the API and stores them in a CSV file.

1. It opens the CSV file in append mode, creating it if it doesn’t exist.
2. If the file is new, it writes the header row first.
3. For each video, it writes a row containing:
- video ID
- username
- caption/description
- like count
- view count
- transcript (TikTok’s voice_to_text output)
4. Each video becomes its own row, allowing you to later analyze all the text and metadata.

### 4. main() (Line 189)
The main() function runs the whole script in order. It gets an access token from TikTok, then goes through each username in the list. For each one, it pulls their videos using the API and saves the results to the CSV file if anything is returned. It waits briefly between each request to avoid rate limits, and when all usernames are finished, it prints a message saying everything has been saved.

---

## Setup

### 1. Get your TikTok Research API credentials:

- `CLIENT_KEY`  
- `CLIENT_SECRET`  

### 2. Open the script and fill in the credentials (Line 20-21):

```python
CLIENT_KEY = "your_client_key_here"
CLIENT_SECRET = "your_client_secret_here"
```

### 3. Add TikTok usernames to scrape (Line 38):

```python
USERNAMES = ["redditdailyvid", "storytime_confessions", "exampleuser"]
```
### 4. Adjust the date range (Line 105-106):

```python
from datetime import date

start_date = date(2025, 11, 1)
end_date = date(2025, 11, 9)
```
---

### Usage

Run the script from your terminal:

```python
python3 transcripts_generation.py
```

For each username, the script will:

1. Authenticate with TikTok API
2. Query videos in the specified date range
3. Retrieve transcripts (if available)
4. Append results to the CSV file

You will see progress printed in the console:
```python
Access token obtained.
Retrieved 12 videos for 'redditdailyvid'
Retrieved 9 videos for 'storytime_confessions'
Captions + transcripts saved to tiktok_user_videos_and_transcripts.csv
```
---
### Output

The CSV file contains:

```python
id: 1234567890
username: exampleuser	
caption: “Am I the jerk for…”
Like_count: 15400
View_count: 102300
transcript: "So this story begins when…"
```
