import matplotlib.pyplot as plt
from src.channel import SHOWS, DEFAULT_COLOR

FONT = {
    'family': 'Arial',
    'color': DEFAULT_COLOR,
    'weight': 'bold',
    'size': 16
}

def format_value(val):
    return "{:,}".format(int(val))

def plot_text(df):

    fig = plt.figure(figsize=(4,2))
    fig.patch.set_facecolor("#282424")

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


def plot_show(df):
    program_color_map = {show["name"]: show["color"] for show in SHOWS}
    program_color_map["Otros"] = DEFAULT_COLOR


    most_viewed_by_show = df.loc[df.groupby('show_id')['view_count'].idxmax()]
    for _, row in most_viewed_by_show.iterrows():
        label = f"{row['show']} =>\t {row['title']} ({row['view_count']} vistas)"
        print(label)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        most_viewed_by_show["show"], 
        most_viewed_by_show["view_count"], 
        color=[program_color_map[show] for show in most_viewed_by_show["show"]]
    )

    # Personalizar el gráfico
    plt.title("Video más reproducido por programa", fontsize=15)
    plt.xlabel("Programa", fontsize=11)
    plt.ylabel("Reproducciones", fontsize=11)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle=":", alpha=0.7)
    for bar in bars:
        height = bar.get_height()
        plt.text(
            x=bar.get_x() + bar.get_width() / 2,
            y=height - 100,
            s=format_value(height),
            ha='center', va='bottom', fontsize=10
        )
    plt.tight_layout()
    plt.show()

