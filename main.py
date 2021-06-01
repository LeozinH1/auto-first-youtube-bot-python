from time import sleep as delay
from src.config import *
from src.log import Log
import requests
import json
from src.google_auth import CommentVideo, AuthUser
from datetime import datetime

log = Log()

from win10toast import ToastNotifier

toaster = ToastNotifier()
t_duration = 5
t_icon = "icon.ico"

def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)



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
    AuthUser()
    last_video = None
    log.info("Bot started sucessfully!")
    toaster.show_toast("Auto First","Bot started sucessfully!", icon_path=t_icon, duration=t_duration)
    while True:
        try:
            #log.warn(f"Trying to get last video id...")
            video_id = GetLastVideoId(PLAYLIST_ID)
            #log.info(f"ID of the last video taken successfully!")
            if video_id["video_id"] != None:
                if last_video == None:
                    last_video = video_id["video_id"]
                elif last_video != video_id["video_id"]:
                    log.warn(f"[ {video_id['author_name']} ] Trying to comment the video...")
                    CommentVideo(video_id["video_id"], TEXT_COMMENT)
                    last_video = video_id["video_id"]
                    log.info(f"[ {video_id['author_name']} ] Comment sended successfully! Comment: {TEXT_COMMENT}")
                    time = datetime.now().time().strftime("%H:%M:%S")
                    append_new_line("log.txt", f"{time} | Comment Published | Channel: {video_id['author_name']} | Video ID: {video_id['video_id']} | Comment: {TEXT_COMMENT}")
                    toaster.show_toast("Comment sended",f"You posted a new comment in the last video of the channel {video_id['author_name']}!", icon_path=t_icon, duration=t_duration)
                elif last_video == video_id["video_id"]:
                    log.warn(f"[ {video_id['author_name']} ] No new videos found or the comment already been sended!")
            else:
                raise TypeError("Video id was not found!")
        except Exception as e:
            log.error(f"{e}")

        delay(REFRESH_TIME)




RunBot()