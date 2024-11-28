import pandas as pd
from typing import Optional

from services import get_data_from_YT_channel

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

generate_csv("SUERTE-TV")