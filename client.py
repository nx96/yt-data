from typing import Optional
from dotenv import load_dotenv

import requests
import os

# load env
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

def get_ID_YT_from_username(username: str) -> Optional[str]:
    url = f"{API_BASE_URL}/search"
    headers = {
        "accept": "application/json",
    }
    params = {
        "key": f"{API_KEY}",
        "q": username,
        "type": "channel",
        "part": "id",
        "maxResults": "1",
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if items:
            return items[0]["id"]["channelId"]
    else:
        return None

def get_data_from_id_channel(id: str) -> Optional[str]:
    url = f"{API_BASE_URL}/channels"
    headers = {
        "accept": "application/json",
    }
    params = {
        "key": f"{API_KEY}",
        "part": "contentDetails,statistics",
        "id": id,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        if items:
            playlistUploadId = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
            viewCount = items[0]["statistics"]["viewCount"]
            subscriberCount = items[0]["statistics"]["subscriberCount"]
            return playlistUploadId, viewCount, subscriberCount
    else:
        return None

def get_videos_from_id_playlist(playlistUploadId: str, pageToken: str) -> Optional[str]:

    url = f"{API_BASE_URL}/playlistItems"
    headers = {
        "accept": "application/json",
    }
    params = {
        "key": f"{API_KEY}",
        "part": "snippet",
        "playlistId": playlistUploadId,
        "maxResults": 50,
        "pageToken": pageToken
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        pageToken = data.get("nextPageToken", None)
        items = data.get("items", [])
        return pageToken, items
    else:
        return None

def get_list_videos_from_id_playlist(playlistUploadId: str) -> Optional[str]:
    pageToken = None
    responseList = []
    response = {}

    while True:
        pageToken, items = get_videos_from_id_playlist(playlistUploadId, pageToken)
        
        if items:
            for item in items:
                response['publishedAt'] = item["snippet"]["publishedAt"]
                response['title'] = item["snippet"]["title"]
                response['videoId'] = item["snippet"]["resourceId"]["videoId"]
                responseList.append(response.copy())
    
        if not pageToken:
            break
    
    return responseList

def get_detail_videos_from_id(videoId: str) -> Optional[str]:

    url = f"{API_BASE_URL}/videos"
    headers = {
        "accept": "application/json",
    }
    params = {
        "key": f"{API_KEY}",
        "part": "contentDetails,statistics",
        "id": videoId,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_detail_videos(listVideos: str) -> Optional[str]:
    maxResults = 50
    response_list = []
    response = {}
    for i in range(0, len(listVideos), maxResults):
        part_list = listVideos[i:i + maxResults]
        ids = [str(item["videoId"]) for item in part_list]
        id_string = ",".join(ids)
        data = get_detail_videos_from_id(id_string)
        items = data.get("items", [])
        if items:
            for item in items:
                response['videoId'] = item["id"]
                response['duration'] = item["contentDetails"]["duration"]
                response['viewCount'] = item["statistics"]["viewCount"]
                response['likeCount'] = item["statistics"]["likeCount"]
                response['favoriteCount'] = item["statistics"]["favoriteCount"]
                response['commentCount'] = item["statistics"]["commentCount"]
                response_list.append(response.copy())
    
    return response_list

def get_data_from_YT_channel(username: str) -> Optional[str]:
    id = get_ID_YT_from_username(username)
    playlistUploadId, viewCount, subscriberCount = get_data_from_id_channel(id)
    list_videos = get_list_videos_from_id_playlist(playlistUploadId)
    list_videos_detail = get_detail_videos(list_videos)
    return list_videos, list_videos_detail, viewCount, subscriberCount

#"SUERTE-TV"