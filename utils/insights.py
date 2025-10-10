import streamlit as st
import pandas as pd

def generate_netflix_insights(df):
    st.subheader("BI-Powered Recommendations 🧠")
    with st.expander("Show Strategic Insights", expanded=True):
        
        # Insight 1: Content Mix
        movie_percent = (df[df['type'] == 'Movie'].shape[0] / df.shape[0]) * 100
        st.markdown(f"""
        - **Content Mix Analysis:** Movies constitute **{movie_percent:.1f}%** of the selected content. A balanced portfolio is key.
          - _Recommendation:_ If heavily skewed, consider diversifying acquisitions to cater to varied audience preferences.
        """)

        # Insight 2: Genre Dominance
        if not df['listed_in'].dropna().empty:
            top_genre = df['listed_in'].str.split(', ').explode().mode()[0]
            st.markdown(f"""
        - **Genre Focus:** **'{top_genre}'** is the most frequent genre. This indicates a strong brand identity in this category.
          - _Recommendation:_ While leveraging this strength, explore niche, high-growth genres to capture new market segments.
        """)

        # Insight 3: Content Freshness
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        avg_age = pd.Timestamp.now().year - df['release_year'].mean()
        st.markdown(f"""
        - **Library Age:** The average age of content is **{avg_age:.1f} years**. A mix of classic and recent titles is crucial.
          - _Recommendation:_ A high average age may suggest a need to invest in more recent, trending content to stay competitive.
        """)

        st.markdown('</div>', unsafe_allow_html=True)


def generate_prime_insights(df):
    st.subheader("BI-Powered Recommendations 🧠")
    with st.expander("Show Strategic Insights", expanded=True):
        
        st.markdown(f"""
        - **Movie Dominance:** Prime Video's library is heavily dominated by movies. This strategy can attract film enthusiasts but may overlook the binge-watching TV show audience.
        - **Genre Opportunity:** While 'Drama' and 'Comedy' are prevalent, there's a significant opportunity to grow in niche but popular genres like 'Sci-Fi' and 'Horror' to challenge competitors.
        - **Release Cadence:** The platform shows a strong back-catalog focus. A strategic push for more recent "Originals" released in the last 2 years could significantly boost user acquisition and retention.
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)


def generate_disney_insights(df):
    st.subheader("BI-Powered Recommendations 🧠")
    with st.expander("Show Strategic Insights", expanded=True):

        st.markdown(f"""
        - **Family-Centric Core:** The content is heavily skewed towards 'Family' and 'Animation', which is a core brand strength. The dominance of 'G', 'TV-G', and 'TV-Y' ratings confirms this strategy.
        - **Seasonal Content Spikes:** Content additions peak in Q4 (Oct-Dec), likely aligning with holiday seasons and major blockbuster releases on the platform. This is a strong and effective seasonal strategy.
        - **Geographic Concentration:** A vast majority of content originates from the United States. To drive international growth, Disney+ should invest in localized content from other key markets.
        - **Expansion Potential:** To grow its subscriber base beyond families, Disney+ could strategically acquire or produce more content in the 'Action-Adventure' and 'Comedy' genres rated 'PG-13' or 'TV-14', targeting a broader audience.
        """)

        st.markdown('</div>', unsafe_allow_html=True)


def generate_hulu_insights(df):
    st.subheader("BI-Powered Recommendations 🧠")
    with st.expander("Show Strategic Insights"):
        
        # Insight 1: Content Lag
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df['year_added'] = df['date_added'].dt.year
        df['lag_years'] = df['year_added'] - df['release_year']
        avg_lag = df[df['lag_years'] >= 0]['lag_years'].mean()
        st.markdown(f"""
        - **Licensed Content Focus:** With an average content lag of **{avg_lag:.1f} years**, Hulu's strategy relies heavily on a deep back-catalog of licensed shows and movies. This is a cost-effective model for content volume.
        - **TV Show Powerhouse:** Hulu's strength lies in its vast and timely TV Show library, often featuring episodes shortly after they air. This is a major competitive advantage for retaining subscribers who follow current broadcast schedules.
        - **Mature Audience:** A high concentration of 'TV-MA' and 'R' rated content shows that Hulu successfully caters to an adult demographic, a key differentiator from platforms like Disney+. This creates a strong market position.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

