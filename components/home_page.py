import streamlit as st
import plotly.express as px
from utils import api_utils
from utils.data_loader import load_all_data

def get_platform_kpis(df, platform_name):
    """Helper function to calculate KPIs for a given platform."""
    platform_df = df[df['platform'] == platform_name]
    if platform_df.empty:
        return {"Total Titles": 0, "Movies": 0, "TV Shows": 0, "Top Genre": "N/A"}
    
    total_titles = platform_df.shape[0]
    movies = platform_df[platform_df['type'] == 'Movie'].shape[0]
    tv_shows = platform_df[platform_df['type'] == 'TV Show'].shape[0]
    top_genre = platform_df['listed_in'].str.split(', ').explode().mode()[0] if not platform_df['listed_in'].dropna().empty else "N/A"
    return {"Total Titles": total_titles, "Movies": movies, "TV Shows": tv_shows, "Top Genre": top_genre}

def show_home_page(set_page_callback):
    # --- HEADER ---
    st.title("DataFlix: Streaming Insights Reimagined 🔮")
    st.markdown("Your central command for streaming analytics. Get a high-level market overview or select a platform for a deep dive.")
    
    # Load combined data for homepage analytics
    all_df = load_all_data()
    if all_df.empty:
        return

    # --- GLOBAL KPIS ---
    st.markdown("### Global Streaming Landscape")
    with st.container(border=True):
        total_titles = all_df.shape[0]
        total_platforms = all_df['platform'].nunique()
        top_genre_global = all_df['listed_in'].str.split(', ').explode().mode()[0]
        
        kpi_cols = st.columns(3)
        kpi_cols[0].metric(label="Total Titles Analyzed", value=f"{total_titles:,}")
        kpi_cols[1].metric(label="Platforms Monitored", value=total_platforms)
        kpi_cols[2].metric(label="Top Genre Across Platforms", value=top_genre_global)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MARKET SHARE & PLATFORM SELECTION ---
    st.markdown("### Market Overview & Platform Deep Dive")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("##### Library Size by Platform")
        platform_counts = all_df['platform'].value_counts()
        fig_pie = px.pie(platform_counts, values=platform_counts.values, names=platform_counts.index, hole=0.6,
                         color_discrete_map={
                             "Netflix": "#E50914", "Prime Video": "#00A8E1", 
                             "Disney+": "#3E82FC", "Hulu": "#3DBB3D"
                         })
        fig_pie.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend_title_text='Platform')
        fig_pie.update_traces(textinfo='percent+label', pull=[0.05, 0, 0, 0])
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("##### Select a Platform")
        
        platforms = {
            "Netflix": "https://image.tmdb.org/t/p/original/wwemzKWzjKYJFfCeiB57q3r4Bcm.svg",
            "Prime Video": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Amazon_Prime_Video_logo.svg/1280px-Amazon_Prime_Video_logo.svg.png",
            "Disney+": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg",
            "Hulu": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Hulu_logo_%282014%29.svg/2560px-Hulu_logo_%282014%29.svg.png"
        }
        
        # This structure now creates a clickable container around each logo
        for platform, logo_url in platforms.items():
            with st.container(border=True):
                st.image(logo_url)
                # The button text is now just a space, making it invisible. CSS handles the rest.
                if st.button("Click Here", key=f"btn_{platform}", use_container_width=True):
                    set_page_callback(platform)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- PLATFORM HEAD-TO-HEAD ---
    st.markdown("### Platform Head-to-Head Comparison 🥊")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        platform1 = c1.selectbox("Select Platform 1", all_df['platform'].unique(), index=0)
        platform2 = c2.selectbox("Select Platform 2", all_df['platform'].unique(), index=1)
        
        if platform1 and platform2:
            kpi1 = get_platform_kpis(all_df, platform1)
            kpi2 = get_platform_kpis(all_df, platform2)
            
            st.markdown(f"##### Comparing **{platform1}** vs. **{platform2}**")
            
            comp_cols = st.columns(2)
            with comp_cols[0]:
                for key, value in kpi1.items():
                    st.metric(label=f"{key} ({platform1})", value=value)
            with comp_cols[1]:
                for key, value in kpi2.items():
                    st.metric(label=f"{key} ({platform2})", value=value)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SEARCH & TRENDING (FULLY IMPLEMENTED WITH REVIEWS) ---
    with st.container(border=True):
        st.subheader("Title Intelligence Terminal")
        c1, c2 = st.columns([1.5, 2])
        
        with c1:
            st.write("**Search for a Movie or TV Show**")
            query = st.text_input("Enter title:", "", key="search_box", placeholder="e.g., The Haunting of Hill House")
            if st.button("Search", use_container_width=True, key="search_btn"):
                if query:
                    with st.spinner("Accessing TMDb Archives..."):
                        details = api_utils.get_movie_details(query)
                    
                    if details and details.get('poster_path'):
                        st.image(f"https://image.tmdb.org/t/p/w200{details.get('poster_path')}")
                        st.subheader(f"{details.get('title') or details.get('name')}")
                        st.write(f"**Rating:** {details.get('vote_average'):.1f}/10 ⭐")
                        st.write(f"**Overview:** {details.get('overview')}")

                        # Fetch and display reviews
                        reviews = api_utils.get_movie_reviews(details.get('id'))
                        if reviews:
                            with st.expander("See Top Reviews"):
                                for review in reviews[:2]: # Show top 2 reviews
                                    st.markdown(f"**Author:** {review.get('author')}")
                                    st.markdown(f"> {review.get('content')}")
                                    st.markdown("---")
                    else:
                        st.error("Title not found in the archives.")
        
        with c2:
            st.write("**🔥 Trending Transmissions Today**")
            trending = api_utils.get_trending_movies()
            if trending:
                with st.container(height=400):
                    trending_cols = st.columns(2)
                    for i, movie in enumerate(trending[:10]): # Show top 10
                        if movie.get('poster_path'):
                            with trending_cols[i % 2]:
                                st.image(f"https://image.tmdb.org/t/p/w200{movie.get('poster_path')}", caption=movie.get('title'), use_container_width=True)
            else:
                st.warning("Could not connect to TMDb. Please check API key or network connection.")
        st.markdown('</div>', unsafe_allow_html=True)

