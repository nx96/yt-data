import pandas as pd
from typing import Optional

from channel import DEFAULT_SHOW, SHOWS
from services import get_data_from_YT_channel
from utils import apply_all_format

DIR_OUTPUT = 'outputs'
def get_df_(username: str) -> Optional[str]:
    # call services
    list_videos, list_videos_detail, viewCount, subscriberCount = get_data_from_YT_channel(username)
    # generate df
    df = pd.DataFrame(list_videos)
    df_detail = pd.DataFrame(list_videos_detail)
    # merge df
    df = pd.merge(df, df_detail, on='videoId', how='left')
    df['viewTotalCount'] = viewCount
    df['subscriberCount'] = subscriberCount
    return df

def generate_csv(username: str) -> Optional[str]:
    df = get_df_(username)
    df.to_csv(f'./{DIR_OUTPUT}/data_{username}.csv', index=False)

def generate_exce_by_csv(csv_file: str) -> Optional[str]:
    df = pd.read_csv(csv_file)
    df.to_excel(f'./{DIR_OUTPUT}/data_{csv_file}.xlsx', index=False)


def max_len_shows():
    max_len = 0
    for show in SHOWS:
        if len(show['id']) > max_len:
            max_len = len(show['id'])
    return max_len
 
def add_column_show(csv_file: str) -> Optional[str]:
    df = pd.read_csv(csv_file)
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
    df = df.loc[:, ['videoId', 'show', 'title', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 'duration', 'publishedAt', 'viewTotalCount', 'subscriberCount']]
    df.to_csv(csv_file, index=False)

# add_column_show(f"./{DIR_OUTPUT}/data_SUERTE-TV.csv")