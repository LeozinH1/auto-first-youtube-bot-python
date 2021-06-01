from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests


from src.log import Log

log = Log()


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']



def AuthUser():

    creds = None

    # IF: file token.json exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)


    # IF: Credentials not exists 
    # OR: is invalid
    if not creds or not creds.valid:
        # IF: credentials exists 
        # AND: expired 
        # AND: has refresh token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # IF: crendetials not exist 
            # OR: not expired 
            # OR: not has refresh token
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=3000)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def CommentVideo(video_id, text) -> dict:
    creds = AuthUser()
    youtube = build('youtube', 'v3', credentials=creds)
 
    try:    
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": text
                        }
                    }
                }
            }
        )

        response = request.execute()

        return { 
            "text" : response["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
            "author" : response["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
            "created_at" : response["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        }

    except Exception as e:
        log.error(f"{e}")


def AccessTokenValidate(token):
    try:
        request = requests.get("https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + token)
        response = request.json()

        print(response)

    except:
        log.error("Error on validate access token")






