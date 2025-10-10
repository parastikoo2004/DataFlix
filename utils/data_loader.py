import streamlit as st
import pandas as pd
import os

PLATFORM_FILES = {
    "Netflix": "netflix_titles.csv",
    "Prime Video": "amazon_prime_titles.csv",
    "Disney+": "disney_plus_titles.csv",
    "Hulu": "hulu_titles.csv",
}

@st.cache_data
def load_data(platform):
    """Loads data for a single specified platform."""
    filename = PLATFORM_FILES.get(platform)
    if not filename:
        st.error(f"Internal error: No filepath defined for '{platform}'.")
        return None
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    filepath = os.path.join(data_dir, filename)
    
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"Dataset for {platform} not found. Please check the `data` folder for `{filename}`.")
        return None

@st.cache_data
def load_all_data():
    """Loads and combines data from all platforms."""
    all_dfs = []
    for platform, filename in PLATFORM_FILES.items():
        # Re-use the single load_data logic but suppress errors for combo view
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
        filepath = os.path.join(data_dir, filename)
        
        try:
            df = pd.read_csv(filepath)
            df['platform'] = platform
            all_dfs.append(df)
        except FileNotFoundError:
            # Silently skip if a file is missing for the combined view
            pass
            
    if not all_dfs:
        st.error("No datasets could be loaded. Please check the `data` folder.")
        return pd.DataFrame()
        
    combined_df = pd.concat(all_dfs, ignore_index=True)
    # Basic cleaning
    combined_df['date_added'] = pd.to_datetime(combined_df['date_added'], errors='coerce')
    return combined_df

