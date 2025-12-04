


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

## Setup

### 1. Get your TikTok Research API credentials:

- `CLIENT_KEY`  
- `CLIENT_SECRET`  

### 2. Open the script and fill in the credentials:

```python
CLIENT_KEY = "your_client_key_here"
CLIENT_SECRET = "your_client_secret_here"
```

### 3. Add TikTok usernames to scrape:

```python
USERNAMES = ["redditdailyvid", "storytime_confessions", "exampleuser"]
```
### 4. Adjust the date range:

```python
from datetime import date

start_date = date(2025, 11, 1)
end_date = date(2025, 11, 9)
```


### Usage

Run the script from your terminal:

```python
python transcripts_generation.py
```

For each username, the script will:

Authenticate with TikTok API
Query videos in the specified date range
Retrieve transcripts (if available)
Append results to the CSV file

You will see progress printed in the console:
```python
Access token obtained.
Retrieved 12 videos for 'redditdailyvid'
Retrieved 9 videos for 'storytime_confessions'
Captions + transcripts saved to tiktok_user_videos_and_transcripts.csv
```

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
