from typing import Optional
from dotenv import load_dotenv

import requests
import os

# load env
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

def get_ID_YT_from_username(username: str) -> Optional[str]:
    """
    Gets the channel ID by username.
    Search for a username and get the first result, filtered by channel.
    ``YouTube Data API <https://developers.google.com/youtube/v3/docs/search/list>``

    Args:
        username (str)

    Returns:
        id
    """
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
    """
    Gets the channel data.
    Search a channel and gets the ID of the uploaded video list, view counter and subscriber counter.
    ``YouTube Data API <https://developers.google.com/youtube/v3/docs/channels/list>``

    Args:
        id (str)

    Returns:
        playlist_upload_id
        view_count
        subscriber_count
    """
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
            playlist_upload_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
            view_count = items[0]["statistics"]["viewCount"]
            subscriber_count = items[0]["statistics"]["subscriberCount"]
            return playlist_upload_id, view_count, subscriber_count
    else:
        return None

def get_videos_from_id_playlist(playlist_id: str, page_token: str) -> Optional[str]:
    """
    Gets the videos list by playlist id.
    Return the videos list and page token for the next search
    ``YouTube Data API <https://developers.google.com/youtube/v3/docs/playlistItems/list>``

    Args:
        playlist_id (str),
        page_token (str)

    Returns:
        playlist_upload_id
        view_count
        subscriber_count
    """
    url = f"{API_BASE_URL}/playlistItems"
    headers = {
        "accept": "application/json",
    }
    params = {
        "key": f"{API_KEY}",
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "pageToken": page_token
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        page_token = data.get("nextPageToken", None)
        items = data.get("items", [])
        return page_token, items
    else:
        return None

def get_list_videos_from_id_playlist(playlist_upload_id: str) -> Optional[str]:
    """
    Make a list with all data from the videos by a playlist ID.
    Use ``get_videos_from_id_playlist`` function.
    
    Args:
        playlist_upload_id (str)

    Returns:
        response_list
    """
    page_token = None
    response_list = []
    response = {}

    while True:
        page_token, items = get_videos_from_id_playlist(playlist_upload_id, page_token)
        
        if items:
            for item in items:
                response['published_at'] = item["snippet"]["publishedAt"]
                response['title'] = item["snippet"]["title"]
                response['video_id'] = item["snippet"]["resourceId"]["videoId"]
                response_list.append(response.copy())
    
        if not page_token:
            break
    
    return response_list

def get_detail_videos_from_id(video_id: str) -> Optional[str]:
    """
    Get videos detail from a ID list separate by comma. 
    ``YouTube Data API <https://developers.google.com/youtube/v3/docs/videos/list>``
    
    Args:
        video_id (str)

    Returns:
        response
    """

    url = f"{API_BASE_URL}/videos"
    headers = {
        "accept": "application/json",
    }
    params = {
        "key": f"{API_KEY}",
        "part": "contentDetails,statistics",
        "id": video_id,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_detail_videos(list_videos: str) -> Optional[str]:
    """
    Make a list with all data from the videos by a list.
    Use ``get_detail_videos_from_id`` function.
    
    Args:
        list_videos (str)

    Returns:
        response_list
    """

    max_results = 50
    response_list = []
    response = {}
    for i in range(0, len(list_videos), max_results):
        part_list = list_videos[i:i + max_results]
        ids = [str(item["video_id"]) for item in part_list]
        id_string = ",".join(ids)
        data = get_detail_videos_from_id(id_string)
        items = data.get("items", [])
        if items:
            for item in items:
                response['video_id'] = item["id"]
                response['view_count'] = item["statistics"]["viewCount"]
                response['like_count'] = item["statistics"]["likeCount"]
                response['favorite_count'] = item["statistics"]["favoriteCount"]
                response['comment_count'] = item["statistics"]["commentCount"]
                
                # when video is not live
                response['duration'] = item["contentDetails"].get("duration", None)
                
                response_list.append(response.copy())
    
    return response_list

def get_data_from_YT_channel(username: str) -> Optional[str]:
    """
    Return channel data by username.
    Use  ``get_ID_YT_from_username``, ``get_data_from_id_channel``,
    ``get_list_videos_from_id_playlist``, ``get_detail_videos``
    
    Args:
        username (str)

    Returns:
        list_videos
        list_videos_detail
        view_count
        subscriber_count
    """

    id = get_ID_YT_from_username(username)
    playlist_upload_id, view_count, subscriber_count = get_data_from_id_channel(id)
    list_videos = get_list_videos_from_id_playlist(playlist_upload_id)
    list_videos_detail = get_detail_videos(list_videos)
    return list_videos, list_videos_detail, view_count, subscriber_count