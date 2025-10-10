import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data
from utils.insights import generate_prime_insights

def show_prime_dashboard():
    st.markdown("## 🔵 Prime Video Strategic Analysis")
    
    try:
        df = load_data('Prime Video')
    except FileNotFoundError:
        st.error("Prime Video dataset not found. Please ensure `amazon_prime_titles.csv` is in the `data` folder.")
        return

    # --- Filters ---
    st.sidebar.header("Filters")
    selected_type = st.sidebar.selectbox("Content Type", ["All", "Movie", "TV Show"], key="prime_type")
    
    if selected_type != "All":
        df_filtered = df[df['type'] == selected_type].copy()
    else:
        df_filtered = df.copy()

    # --- KPI Section ---
    total_titles = df_filtered.shape[0]
    total_movies = df_filtered[df_filtered['type'] == 'Movie'].shape[0]
    total_tv_shows = df_filtered[df_filtered['type'] == 'TV Show'].shape[0]
    top_director = df_filtered['director'].mode()[0] if not df_filtered['director'].dropna().empty else "N/A"

    with st.container():
        
        kpi_cols = st.columns(4)
        kpi_cols[0].metric(label="Total Titles", value=f"{total_titles:,}")
        kpi_cols[1].metric(label="Movies", value=f"{total_movies:,}")
        kpi_cols[2].metric(label="TV Shows", value=f"{total_tv_shows:,}")
        kpi_cols[3].metric(label="Top Director", value=top_director)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Main Dashboard with Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Content Library", "📊 Genre & Audience", "📈 Temporal & Creator", "🌍 Geographic Footprint"])

    with tab1:
        st.subheader("Library Composition")
        col1, col2 = st.columns([1, 2])
        with col1:
            
            st.markdown("##### Content Type Distribution")
            fig_pie = px.pie(df_filtered, names='type', title='',
                             color_discrete_map={'Movie':'#00A8E1', 'TV Show':'#1E3A8A'})
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
            fig_hist.add_trace(go.Histogram(x=df_movies['duration_int'], name='Movies (mins)', marker_color='#00A8E1'))
            fig_hist.add_trace(go.Histogram(x=df_tv['duration_int'], name='TV Shows (seasons)', marker_color='#1E3A8A'))
            fig_hist.update_layout(barmode='overlay', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_hist.update_traces(opacity=0.75)
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with tab2:
        st.subheader("Audience Targeting Analysis")
        col1, col2 = st.columns(2)
        with col1:
            
            st.markdown("##### Top 10 Genres")
            top_genres = df_filtered['listed_in'].str.split(', ').explode().value_counts().nlargest(10)
            fig_donut = px.pie(top_genres, values=top_genres.values, names=top_genres.index, hole=0.6,
                               color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_donut.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            
            st.markdown("##### Top Content Ratings")
            rating_counts = df_filtered['rating'].value_counts().nlargest(10)
            fig_funnel = px.funnel(rating_counts, x=rating_counts.values, y=rating_counts.index,
                                   color_discrete_sequence=px.colors.sequential.Blues_r)
            fig_funnel.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_funnel, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Content Release & Creator Strategy")
        col1, col2 = st.columns(2)
        with col1:
            
            st.markdown("##### Titles Released by Year")
            release_year_counts = df_filtered['release_year'].value_counts().sort_index()
            fig_area = px.area(release_year_counts, x=release_year_counts.index, y=release_year_counts.values,
                               labels={'y':'Titles Released', 'x':'Year'}, markers=True)
            fig_area.update_traces(line_color='#00A8E1', line_width=2)
            fig_area.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_area, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            
            st.markdown("##### Top 10 Directors")
            top_directors = df_filtered['director'].dropna().value_counts().nlargest(10)
            fig_dir = px.bar(top_directors, x=top_directors.values, y=top_directors.index, orientation='h',
                             color=top_directors.values, color_continuous_scale='Blues')
            fig_dir.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_dir, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.subheader("Global Content Distribution")
        
        st.markdown("##### Content Production by Country")
        country_counts = df_filtered['country'].str.split(', ').explode().dropna().value_counts()
        
        fig_map = px.choropleth(country_counts, 
                                locations=country_counts.index, 
                                locationmode='country names',
                                color=country_counts.values,
                                color_continuous_scale=px.colors.sequential.Blues,
                                title="Global Content Production Hotspots")
        fig_map.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BI Insights Section ---
    generate_prime_insights(df_filtered)

