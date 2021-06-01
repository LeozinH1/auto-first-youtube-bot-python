from time import sleep as delay
from config import *
from log import Log
import requests
import json
from google_auth import CommentVideo
log = Log()




def GetLastVideoId(playlist_id) -> dict:
    try:
        request = requests.get(f"https://www.youtube.com/oembed?url=www.youtube.com/playlist?list={playlist_id}&format=json")
        response = request.json()

        video_id = response["thumbnail_url"].split("/")[4]
        author_name = response["author_name"]

        if video_id and author_name:
            return {"video_id" : video_id, "author_name" : author_name}
    except:
        log.error("Unable to get playlist information!")


def RunBot():
    last_video = None
    log.info("Bot started sucessfully!")
    while True:
        try:
            log.warn(f"Trying to get last video id...")
            video_id = GetLastVideoId(PLAYLIST_ID)
            log.info(f"ID of the last video taken successfully!")
            if video_id["video_id"] != None:
                if last_video == None:
                    last_video = video_id["video_id"]
                elif last_video != video_id["video_id"]:
                    log.warn(f"Trying to comment the video...")
                    CommentVideo(video_id["video_id"], TEXT_COMMENT)
                    last_video = video_id["video_id"]
                    log.info(f"Comment sended successfully!")
                elif last_video == video_id["video_id"]:
                    log.warn(f"No new videos found or the comment already been sended!")
            else:
                raise TypeError("Video id was not found!")
        except Exception as e:
            log.error(f"{e}")

        delay(REFRESH_TIME)




RunBot()