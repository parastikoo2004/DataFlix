import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.insights import generate_netflix_insights
import pandas as pd

def show_netflix_dashboard():
    st.markdown("## 🔴 Netflix Content Intelligence")
    
    try:
        df = load_data('Netflix')
    except FileNotFoundError:
        st.error("Netflix dataset not found. Please ensure `netflix_titles.csv` is in the `data` folder.")
        return

    # --- Filters ---
    st.sidebar.header("Filters")
    selected_type = st.sidebar.selectbox("Content Type", ["All", "Movie", "TV Show"], key="netflix_type")
    
    if selected_type != "All":
        df_filtered = df[df['type'] == selected_type].copy()
    else:
        df_filtered = df.copy()

    # --- KPI Section ---
    total_titles = df_filtered.shape[0]
    total_movies = df_filtered[df_filtered['type'] == 'Movie'].shape[0]
    total_tv_shows = df_filtered[df_filtered['type'] == 'TV Show'].shape[0]
    top_country = df_filtered['country'].mode()[0] if not df_filtered['country'].dropna().empty else "N/A"

    with st.container():
        kpi_cols = st.columns(4)
        kpi_cols[0].metric(label="Total Titles", value=f"{total_titles:,}")
        kpi_cols[1].metric(label="Movies", value=f"{total_movies:,}")
        kpi_cols[2].metric(label="TV Shows", value=f"{total_tv_shows:,}")
        kpi_cols[3].metric(label="Top Content Country", value=top_country)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Main Dashboard with Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Content Library", "📊 Genre & Audience", "📈 Temporal Analysis", "🌍 Geographic Footprint"])

    with tab1:
        st.subheader("Library Composition")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("##### Content Type Distribution")
            fig_pie = px.pie(df_filtered, names='type', title='', 
                             color_discrete_sequence=['#E50914', '#B20710'])
            fig_pie.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown("##### Movie Duration vs. TV Show Seasons")
            df_movies = df_filtered[df_filtered['type'] == 'Movie'].copy()
            df_tv = df_filtered[df_filtered['type'] == 'TV Show'].copy()
            df_movies['duration_int'] = pd.to_numeric(df_movies['duration'].str.replace(' min', ''), errors='coerce').dropna()
            df_tv['duration_int'] = pd.to_numeric(df_tv['duration'].str.extract('(\d+)')[0], errors='coerce').dropna()
            
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(x=df_movies['duration_int'], name='Movies (mins)', marker_color='#E50914'))
            fig_hist.add_trace(go.Histogram(x=df_tv['duration_int'], name='TV Shows (seasons)', marker_color='#B20710'))
            fig_hist.update_layout(barmode='overlay', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_hist.update_traces(opacity=0.75)
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("Genre and Rating Deep Dive")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Top 10 Genres")
            top_genres = df_filtered['listed_in'].str.split(', ').explode().value_counts().nlargest(10)
            fig_bar = px.bar(top_genres, x=top_genres.values, y=top_genres.index, orientation='h', 
                             color=top_genres.values, color_continuous_scale='Reds')
            fig_bar.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("##### Content by Maturity Rating")
            rating_counts = df_filtered['rating'].value_counts().nlargest(10)
            fig_donut = px.pie(rating_counts, values=rating_counts.values, names=rating_counts.index, hole=0.5,
                               color_discrete_sequence=px.colors.sequential.Reds_r)
            fig_donut.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Content Release and Addition Trends")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Content Added to Netflix (Quarterly)")
            df_filtered['date_added'] = pd.to_datetime(df_filtered['date_added'], errors='coerce')
            content_over_time = df_filtered.set_index('date_added').resample('Q').size()
            fig_line = px.area(content_over_time, x=content_over_time.index, y=content_over_time.values,
                               labels={"y": "Titles Added", "x": "Date"}, markers=True)
            fig_line.update_traces(line_color='#E50914', line_width=2)
            fig_line.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown("##### Content by Original Release Year")
            release_year_dist = df_filtered['release_year'].value_counts().sort_index()
            fig_release = px.bar(release_year_dist, x=release_year_dist.index, y=release_year_dist.values,
                                 labels={'y':'Number of Titles', 'x':'Release Year'})
            fig_release.update_traces(marker_color='#B20710')
            fig_release.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_release, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.subheader("Global Content Distribution")
        st.markdown("##### Content Production by Country")
        country_counts = df_filtered['country'].str.split(', ').explode().dropna().value_counts()
        
        fig_map = px.choropleth(country_counts, 
                                locations=country_counts.index, 
                                locationmode='country names',
                                color=country_counts.values,
                                color_continuous_scale=px.colors.sequential.Reds,
                                title="Global Content Production Hotspots")
        fig_map.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BI Insights Section ---
    generate_netflix_insights(df_filtered)

