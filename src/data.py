import pandas as pd
from typing import Optional

from .channel import DEFAULT_SHOW, SHOWS
from .services import get_data_from_YT_channel
from .utils import apply_all_format, parse_duration_to_seconds

DIR_OUTPUT = 'outputs'

def get_df_(username: str) -> Optional[str]:
    # call services
    list_videos, list_videos_detail, view_count, subscriber_count = get_data_from_YT_channel(username)
    # generate df
    df = pd.DataFrame(list_videos)
    df_detail = pd.DataFrame(list_videos_detail)
    # merge df
    df = pd.merge(df, df_detail, on='video_id', how='left')
    df['view_total_count'] = view_count
    df['subscriber_count'] = subscriber_count
    df["url"] = "https://www.youtube.com/watch?v=" + df["video_id"]
    df["duration_seconds"] = df["duration"].apply(parse_duration_to_seconds)
    return df

def generate_csv(username: str) -> Optional[str]:
    df = get_df_(username)
    path = f'./{DIR_OUTPUT}/data_{username}.csv'
    df.to_csv(path, index=False)
    print(f"File created at {path}")
    return df

def generate_excel_by_csv(username: str) -> Optional[str]:
    path = f"./{DIR_OUTPUT}/data_{username}.csv"
    df = pd.read_csv(path)
    path = f'./{DIR_OUTPUT}/data_{username}.xlsx'
    df.to_excel(path, index=False, sheet_name="data")
    print(f"File created at {path}")

def max_len_shows():
    max_len = 0
    for show in SHOWS:
        if len(show['id']) > max_len:
            max_len = len(show['id'])
    return max_len
 
def add_column_show(username: str) -> Optional[str]:
    path = f"./{DIR_OUTPUT}/data_{username}.csv"
    df = pd.read_csv(path)
    max_len = max_len_shows()
    df["show"] = ""
    for index in df.index:
        title = df.at[index, "title"]
        title = apply_all_format(title)
        title = title[:max_len]
        df.at[index, "show"] = DEFAULT_SHOW
        for show in SHOWS:
            if title.find(show['id']) != -1:
                df.at[index, "show"] = show['name']
                break
    df = df.loc[:, ['video_id', 'show', 'title', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 'duration', 'duration_seconds', 'publishedAt', 'url', 'view_total_count', 'subscriber_count']]
    df.to_csv(path, index=False)
