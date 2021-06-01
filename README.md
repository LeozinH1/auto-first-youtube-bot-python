# Auto First Youtube Bot

[**DEMO**](https://youtu.be/IRIcIMC1bMQ "DEMO")

This bot checks if a predefined YouTube channel has uploaded a new video, if a recent upload is detected, a comment is created on the uploaded video.

# Requirements

[Python3](https://www.python.org) installed on the computer

# Usage

1. Setup new application and download your credentials from the [Google API](https://console.developers.google.com "Google API") website 
- Scopes: `https://www.googleapis.com/auth/youtube.force-ssl`
- Authorized redirect URIs: `http://localhost:3000` 
- Authorized JavaScript sources: `http://localhost:3000`
2. Rename you credentials file to `credentials.json` and put in bot root folder.
3. Setup `config.py` (Read before **How to get the Playlist Id**)
4. Install all necessary project dependencies
5. Open folder with cmd and run `python3 src/main.py`
6. If, for the first time, a page will open to login
7. After login, the bot will start to work!

Any problem with access, delete the file `token.json` and restart the bot

# How to get the Playlist Id
1. Access the channel you want to comment on
2. Click on **Videos** section and after that **Play All**
3. Copy the id (in url) that is in **&list=**

**Example**: https://www.youtube.com/watch?v=IRIcIMC1bMQ&list=UUrfluf17A1AsyOEZWpFzK2w&index=2.
The ID is **UUrfluf17A1AsyOEZWpFzK2w**
