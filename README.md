**DataFlix: The OTT Intelligence Dashboard** 🔮

A comprehensive, multi-page Business Intelligence dashboard built in Python that analyzes and compares the content strategies of the world's top streaming platforms: Netflix, Prime Video, Disney+, and Hulu.

This app transforms raw, siloed datasets into a high-performance, interactive tool for strategic analysis, complete with a "glassmorphism" UI, animated visualizations, and a live API connection to The Movie Database (TMDb).

✨ Core Features

This dashboard is a comprehensive BI tool that provides insights at both a macro (global market) and micro (platform-specific) level.

🌎 Global Market Overview: A high-level home page with aggregated KPIs (Total Titles, Top Genres) and an interactive market share chart.

🥊 Platform Head-to-Head: A dynamic comparison tool that lets you select any two platforms and see a side-by-side breakdown of their library size, content mix, and top genres.

🔴🔵✨🟢 Deep-Dive Dashboards: Four dedicated, multi-tab dashboards with 10-12 unique visualizations each, analyzing the specific content strategies of Netflix, Prime Video, Disney+, and Hulu.

📊 40+ Interactive Visualizations: A complete suite of animated charts built with Plotly, including:

Choropleth World Maps (Geographic Footprint)

Time-Series Area Charts (Content Growth)

Histograms (Movie Runtimes vs. TV Seasons)

Donut & Pie Charts (Content Mix)

Bar Charts (Top 10 Genres, Directors)

Treemaps & Funnel Charts (Rating Analysis)

Polar (Radar) Charts (Seasonal Trends)

🧠 Automated BI Insights Engine: An "AI-powered" recommendations panel on each dashboard that provides automated, data-driven strategic insights based on the visualized data.

📡 Live API Integration: A "Title Intelligence Terminal" powered by the TMDb API that allows you to:

Search for any movie or TV show to get its poster, overview, and rating.

Fetch current user reviews for any searched title.

View a live, auto-updating feed of the Top 10 Trending Movies.

🎶 Aesthetic UI/UX: A stunning custom-built "glassmorphism" dark theme, animated Lottie icons for KPIs, and a functional ambient music player in the sidebar.

🚀 How to Run Locally

Follow these steps to get the project running on your local machine.

1. Clone the Repository

git clone [https://github.com/](https://github.com/)[YourGitHubUsername]/DataFlix.git
cd DataFlix


2. Create and Activate a Virtual Environment

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\\venv\\Scripts\\activate


3. Install Dependencies

All required libraries are listed in the requirements.txt file.

pip install -r requirements.txt


4. Set Up Your API Key (CRITICAL)

This project requires a free API key from The Movie Database (TMDb) to power the search and trending features.

Go to themoviedb.org and create a free account.

Navigate to your account Settings → API.

Copy your API Key (v3 auth).

Create a new folder in the project's root directory named .streamlit.

Inside that .streamlit folder, create a new file named secrets.toml.

Add your key to that file like this:

TMDB_API_KEY = "your_actual_api_key_goes_here"


5. Run the App!

You're all set. Run the following command in your terminal:

streamlit run app.py


Your browser should open automatically to http://localhost:8501.

🛠️ Technology Stack

Core Language: Python 3

Dashboard Framework: Streamlit

Data Manipulation: Pandas

Data Visualization: Plotly

Animations: streamlit-lottie (for Lottie JSON animations)

API Communication: Requests (for TMDb API)

Styling: Custom CSS (injected via st.markdown)

📸 Dashboard Screenshots

(I highly recommend adding screenshots of each dashboard page here. They will make your README look incredibly professional.)

1. Home Page (Global Overview & Title Intelligence)

[Insert Screenshot of your Home Page here]

2. Netflix Dashboard (Global Strategy)

[Insert Screenshot of your Netflix Dashboard here]

3. Disney+ Dashboard (Seasonal & Brand Focus)

[Insert Screenshot of your Disney+ Dashboard here]

4. Hulu Dashboard (Licensed Content Analysis)

[Insert Screenshot of your Hulu Dashboard here]

📂 Project Structure

DataFlix/
│
├── .streamlit/
│   └── secrets.toml          # Stores API keys
│
├── assets/
│   └── loading_animation.json # Lottie animation file
│
├── components/
│   ├── home_page.py
│   ├── netflix_dashboard.py
│   ├── prime_dashboard.py
│   ├── disney_dashboard.py
│   └── hulu_dashboard.py
│
├── data/
│   ├── netflix_titles.csv
│   ├── amazon_prime_titles.csv
│   ├── disney_plus_titles.csv
│   └── hulu_titles.csv
│
├── utils/
│   ├── api_utils.py          # Functions for TMDb API calls
│   ├── data_loader.py        # Caching & loading data
│   └── insights.py           # BI recommendations engine
│
├── app.py                    # Main application file to run
├── requirements.txt          # Project dependencies
└── style.css                 # Custom CSS for styling
