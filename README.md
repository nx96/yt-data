# YouTube Channel Data Analysis

This project allows you to extract, analyze, and visualize data from a YouTube channel using the YouTube Data API. The application processes channel information and generates CSV, Excel files, and various graphs, which are presented in a Jupyter Notebook.

---

## Features

1. **Data Extraction:**
   - Fetches detailed information about a YouTube channel, including videos, views, likes, comments, and more.

2. **Data Processing:**
   - Uses `pandas` to manipulate and organize the extracted data.
   - Generates CSV and Excel files with the following columns:
     - `video_id`, `show`, `show_id`, `title`, `view_count`, `like_count`, `like_view`, `favorite_count`, `comment_count`, `duration`, `duration_seconds`, `published_at`, `url`, `view_total_count`, `subscriber_count`.

3. **Data Visualization:**
   - Creates insightful graphs using `matplotlib` to analyze the channel's performance.

4. **Results Presentation:**
   - Outputs are compiled in a comprehensive Jupyter Notebook (`Resultados.ipynb`).

---

## Getting Started

Follow these steps to set up and use the project:

### Prerequisites

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/nx96/yt-data.git
   cd yt-data
   ```

2. **Set Up Python Environment & Install Dependencies:**
   - Use the provided `install.sh` script:
     ```bash
     sh install.sh
     ```
   - Alternatively, you can create a virtual environment & install dependencies:
     ```bash
     python -m venv venv
     source venv/Scripts/activate
     ```
     ```bash
     pip install -r requirements.txt
     ```

### Configuration

1. **API Credentials:**
   - Create a `.env` file in the root directory.
   - Use `.env.example` as a template and fill in your YouTube API credentials:
     ```
     API_KEY=your_api_key
     API_BASE_URL=https://www.googleapis.com/youtube/v3
     ```

2. **Channel Settings:**
   - Edit the `src/channel.py` file:
     - Set the `USERNAME` variable to the desired YouTube channel name.
     - Update the `SHOWS` dictionary with program IDs, names, and color codes for graphs.

### Execution

1. **Extract Data:**
   - Open and run the `GetDataFromYTChannel.ipynb` notebook.
   - This notebook fetches the channel data and generates the required CSV and Excel files.

2. **Analyze Results:**
   - View the processed data and graphs in the `Resultados.ipynb` notebook.

---

## Project Structure

```
.
|-- outputs
|   |-- data.example.csv         # Example of the generated CSV file
|-- src
|   |-- __init__.py              # Package initializer
|   |-- channel.py               # Channel-specific settings
|   |-- data.py                  # Data processing logic
|   |-- graphs.py                # Graph generation
|   |-- services.py              # API interaction
|   |-- utils.py                 # Utility functions
|-- .env.example                 # Example environment variables
|-- .gitignore                   # Git ignore file
|-- GetDataFromYTChannel.ipynb   # Notebook for data extraction
|-- install.sh                   # Setup script
|-- README.md                    # Project documentation
|-- requirements.txt             # Python dependencies
|-- Resultados.ipynb             # Notebook with results and visualizations
```

---

## Graphs and Visualizations

- Bar charts representing the most viewed videos by program.
- Line charts showing the evolution of metrics over time.
- Customizable color-coded graphs based on the `SHOWS` dictionary.

---

## Example Usage

1. Clone the repository and configure your `.env` file.
2. Set up the channel details in `channel.py`.
3. Run `GetDataFromYTChannel.ipynb` to fetch and process data.
4. Explore the results in `Resultados.ipynb`.

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

