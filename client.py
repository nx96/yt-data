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

# def get_data_from_id_channel(id: str) -> Optional[str]:
#     url = f"{API_BASE_URL}/channels"
#     headers = {
#         "accept": "application/json",
#     }
#     params = {
#         "key": f"{API_KEY}",
#         "part": "contentDetails,statistics",
#         "id": id,
#     }

#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         items = response.get("items", [])
#         if items:
#             uploads = items.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads", "")
#             return uploads
#     else:
#         return None


id = get_ID_YT_from_username("SUERTE-TV")
print(id)
# uploads = get_data_from_id_channel(id)
# print(uploads)