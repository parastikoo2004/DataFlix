import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data
from utils.insights import generate_hulu_insights

def show_hulu_dashboard():
    st.markdown("## 🟢 Hulu Content Landscape")
    try:
        df = load_data('Hulu')
    except FileNotFoundError:
        st.error("Hulu dataset not found.")
        return

    # --- Filters ---
    st.sidebar.header("Filters")
    min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
    selected_year = st.sidebar.slider("Filter by Release Year", min_year, max_year, (min_year, max_year), key="hulu_year")
    df_filtered = df[(df['release_year'] >= selected_year[0]) & (df['release_year'] <= selected_year[1])].copy()

    # --- KPI Section (Reverted to simpler version without Lottie) ---
    total_titles = df_filtered.shape[0]
    movies = df_filtered[df_filtered['type'] == 'Movie'].shape[0]
    tv_shows = df_filtered[df_filtered['type'] == 'TV Show'].shape[0]
    top_genre = df_filtered['listed_in'].str.split(', ').explode().mode()[0] if not df_filtered['listed_in'].dropna().empty else "N/A"
    
    with st.container(border=True):
        kpi_cols = st.columns(4)
        kpi_cols[0].metric(label="Total Titles (Filtered)", value=f"{total_titles:,}")
        kpi_cols[1].metric(label="Movies", value=f"{movies:,}")
        kpi_cols[2].metric(label="TV Shows", value=f"{tv_shows:,}")
        kpi_cols[3].metric(label="Dominant Genre", value=top_genre)

    # --- Main Dashboard with Tabs ---
    tab1, tab2, tab3 = st.tabs(["📚 Library Overview", "📊 Genre & Rating Insights", "📈 Creator & Content Analysis"])
    with tab1:
        st.subheader("Content Acquisition Strategy")
        col1, col2 = st.columns(2)
        with col1:

                st.markdown("##### Content Added to Hulu Over Time")
                df_filtered['date_added'] = pd.to_datetime(df_filtered['date_added'], errors='coerce')
                content_over_time = df_filtered.set_index('date_added').resample('M').size()
                fig_line = px.area(content_over_time, x=content_over_time.index, y=content_over_time.values, labels={"y": "Titles Added", "x": "Month"}, markers=True)
                fig_line.update_traces(line_color='#1CE783', line_width=2)
                fig_line.update_layout(template='seaborn', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_line, use_container_width=True)
        with col2:

                st.markdown("##### Lag Between Release and Addition")
                df_filtered['year_added'] = df_filtered['date_added'].dt.year
                df_filtered['lag_years'] = df_filtered['year_added'] - df_filtered['release_year']
                avg_lag = df_filtered[df_filtered['lag_years'] >= 0]['lag_years'].mean()
                st.metric(label="Average Lag (Years)", value=f"{avg_lag:.1f}")
                lag_dist = df_filtered[(df_filtered['lag_years'] >= 0) & (df_filtered['lag_years'] <= 20)]
                fig_lag = px.histogram(lag_dist, x='lag_years', nbins=20, title="Distribution of Content Lag", color_discrete_sequence=['#3DBB3D'])
                fig_lag.update_layout(template='seaborn', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_lag, use_container_width=True)
    with tab2:
        st.subheader("Genre and Rating Breakdown")
        col1, col2 = st.columns(2)
        with col1:

                st.markdown("##### Top 10 Genres")
                top_genres = df_filtered['listed_in'].str.split(', ').explode().value_counts().nlargest(10)
                fig_bar = px.bar(top_genres, x=top_genres.values, y=top_genres.index, orientation='h', color=top_genres.values, color_continuous_scale='Greens')
                fig_bar.update_layout(template='seaborn', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_bar, use_container_width=True)
        with col2:

                st.markdown("##### Content by Rating")
                rating_counts = df_filtered['rating'].value_counts().nlargest(10)
                fig_pie = px.pie(rating_counts, values=rating_counts.values, names=rating_counts.index, hole=0.5, color_discrete_sequence=px.colors.sequential.Greens_r)
                fig_pie.update_layout(template='seaborn', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
                
    with tab3:
        st.subheader("Creator and Content Length Analysis")
        col1, col2 = st.columns(2)
        with col1:

                st.markdown("##### Top 10 Directors by Content Volume")
                top_directors = df_filtered['director'].str.split(', ').explode().dropna().value_counts().nlargest(10)
                fig_dir = px.bar(top_directors, x=top_directors.values, y=top_directors.index, orientation='h',
                                 color=top_directors.values, color_continuous_scale='Greens_r',
                                 labels={'x':'Number of Titles', 'y':'Director'})
                fig_dir.update_layout(template='seaborn', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_dir, use_container_width=True)
        with col2:
                st.markdown("##### Content Duration Analysis")
                df_movies = df_filtered[df_filtered['type'] == 'Movie'].copy()
                df_tv = df_filtered[df_filtered['type'] == 'TV Show'].copy()
                df_movies['duration_int'] = pd.to_numeric(df_movies['duration'].str.replace(' min', ''), errors='coerce').dropna()
                df_tv['duration_int'] = pd.to_numeric(df_tv['duration'].str.extract('(\d+)')[0], errors='coerce').dropna()

                fig_dur = go.Figure()
                fig_dur.add_trace(go.Histogram(x=df_movies['duration_int'], name='Movies (mins)', marker_color='#1CE783'))
                fig_dur.add_trace(go.Histogram(x=df_tv['duration_int'], name='TV Shows (seasons)', marker_color='#3DBB3D'))
                fig_dur.update_layout(barmode='overlay', template='seaborn', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                fig_dur.update_traces(opacity=0.75)
                st.plotly_chart(fig_dur, use_container_width=True)
    
    generate_hulu_insights(df_filtered)

