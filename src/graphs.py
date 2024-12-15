import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from src.channel import DEFAULT_SHOW, SHOWS, DEFAULT_COLOR
import pandas as pd
from typing import List, Optional
from src.utils import delete_emojis

def seconds_to_time(seconds: int):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}H:{minutes:02}M:{secs:02}S"
    
FONT = {
    'family': 'Arial',
    'color': DEFAULT_COLOR,
    'weight': 'bold',
    'size': 16
}

FONT_TAGS = {
    'family': 'Arial',
    'color': '#000000',
    'size': 11
}

PROGRAM_COLOR_MAP = {show["name"]: show["color"] for show in SHOWS}
PROGRAM_COLOR_MAP["Otros"] = DEFAULT_COLOR

def format_value(val):
    return "{:,}".format(int(val))

def plot_text(df: pd.DataFrame):

    fig = plt.figure(figsize=(4,2))
    fig.patch.set_facecolor("black")

    # Agregar textos
    val = format_value(df['subscriber_count'][0])
    text = f'SUSCRIPTORES: {val}'
    plt.text(x=0.2, y=0.6, s=text, ha='center', fontdict=FONT)
    val = format_value(df['view_total_count'][0])
    text = f'VISTAS: {val}'
    plt.text(x=0.2, y=0.3, s=text, ha='center', fontdict=FONT)

    plt.axis('off')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.4)

    plt.show()

def plot_longest_video(df: pd.DataFrame):
    longest_video = df[~df['show_id'].isin([DEFAULT_SHOW])].sort_values(by='duration_seconds', ascending=False)
    
    fig = plt.figure(figsize=(4,4))
    fig.patch.set_facecolor("black")

    # Agregar textos
    text = delete_emojis(longest_video.iloc[0]["title"])
    text = f'TITULO: {text}'
    plt.text(x=0.2, y=0.9, s=text, fontdict=FONT)
    
    text = f'LIKES: {longest_video.iloc[0]["like_count"]}'
    plt.text(x=0.2, y=0.6, s=text, fontdict=FONT)
    
    text = f'DURACIÓN: {seconds_to_time(longest_video.iloc[0]["duration_seconds"])}'
    plt.text(x=0.2, y=0.3, s=text, fontdict=FONT)

    plt.axis('off')
    plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.4)

    plt.show()


def plot_base(df: pd.DataFrame, colum: str, ylabel : str, limit_height: Optional[bool] = True, print_legends: Optional[bool] = True, format_time: Optional[bool] = False):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        df["show"], 
        df[colum], 
        color=[PROGRAM_COLOR_MAP[show] for show in df["show"]]
    )

    plt.xlabel("Programa", fontdict=FONT_TAGS)
    plt.ylabel(ylabel, fontdict=FONT_TAGS)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="-", alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.text(
            x=bar.get_x() + bar.get_width() / 2,
            y= height if not limit_height else height - 100,
            s= format_value(height) if not format_time else seconds_to_time(height),
            ha='center', va='bottom', fontsize=10
        )

    if print_legends:
        legend_elements = []
        for _, row in df.iterrows():
            color = PROGRAM_COLOR_MAP[row["show"]]
            label = f"{delete_emojis(row['title'])}"
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, color=color, label=label))
        
        plt.legend(
            handles=legend_elements,
            loc='center',
            fontsize=9,
            title_fontsize=10,
            frameon=True,
            bbox_to_anchor=(0.5, 1.15),
            ncol=2
        )

    plt.tight_layout()
    plt.show()

def plot_evolution(df: pd.DataFrame, color: str, colum: str, ylabel: str, format_legends: Optional[bool] = False):
    df['published_at'] = pd.to_datetime(df['published_at'])
    plt.figure(figsize=(10, 6))
    plt.plot(
        df['published_at'], 
        df[colum], 
        color=color, 
        linewidth=2, 
        marker='.', 
        markerfacecolor='black'
    )

    if format_legends:
        formatter = FuncFormatter(lambda x, _: seconds_to_time(seconds=int(x)))
        plt.gca().yaxis.set_major_formatter(formatter)

    plt.xlabel("Fecha", fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle=":", alpha=0.8)

    plt.tight_layout()
    plt.show()

def plot_show_by_view_count(df: pd.DataFrame):
    most_viewed_by_show = df.loc[df.groupby('show_id')['view_count'].idxmax()].sort_values(by='view_count', ascending=True)

    plot_base(df=most_viewed_by_show, colum="view_count", ylabel="Reproducciones")

def plot_show_by_like_count(df: pd.DataFrame):
    most_liked_by_show = df.loc[df.groupby('show_id')['like_count'].idxmax()].sort_values(by='like_count', ascending=True)

    plot_base(df=most_liked_by_show, colum="like_count", ylabel="Likes")

def plot_show_by_comment_count(df: pd.DataFrame):
    most_comment_show = df.loc[df.groupby('show_id')['comment_count'].idxmax()].sort_values(by='comment_count', ascending=True)

    plot_base(df=most_comment_show, colum="comment_count", ylabel="Comentarios")

def plot_evolution_by_view(df: pd.DataFrame, program : str):
    evolution_program = df[df['show'] == program].sort_values(by='published_at')
    color=PROGRAM_COLOR_MAP[program]

    plot_evolution(df=evolution_program, color=color, colum="view_count")

def plot_evolution_by_like(df: pd.DataFrame, program : str):
    evolution_program = df[df['show'] == program].sort_values(by='published_at')
    color=PROGRAM_COLOR_MAP[program]

    plot_evolution(df=evolution_program, color=color, colum="like_count", ylabel='Likes')

def plot_evolution_by_popularity(df: pd.DataFrame, program : str):
    evolution_program = df[df['show'] == program].sort_values(by='published_at')
    color=PROGRAM_COLOR_MAP[program]

    plot_evolution(df=evolution_program, color=color, colum="like_view", ylabel='Popularidad')

def plot_evolution_by_duration(df: pd.DataFrame, program : str):
    evolution_program = df[df['show'] == program].sort_values(by="published_at")
    color=PROGRAM_COLOR_MAP[program]

    plot_evolution(df=evolution_program, color=color, colum="duration_seconds", ylabel='Tiempo', format_legends=True)

def plot_chapters_by_show(df: pd.DataFrame):
    df_count = df[~df['show_id'].isin([DEFAULT_SHOW])].groupby(['show']).agg({'title': 'count'}).sort_values(by='title', ascending=True).reset_index()
    plot_base(df=df_count, colum="title", ylabel="Capítulos", limit_height=False, print_legends=False)

def plot_duration_by_show(df: pd.DataFrame):
    df_duration = df[~df['show_id'].isin([DEFAULT_SHOW])].groupby(['show']).agg({'duration_seconds': 'sum'}).sort_values(by='duration_seconds', ascending=True).reset_index()
    plot_base(df=df_duration, colum="duration_seconds", ylabel="Duración", limit_height=True, print_legends=False, format_time=True)
