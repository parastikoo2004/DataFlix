import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data
from utils.insights import generate_disney_insights

def show_disney_dashboard():
    st.markdown("## ✨ Disney+ Universe Analytics")
    
    try:
        df = load_data('Disney+')
    except FileNotFoundError:
        st.error("Disney+ dataset not found. Please ensure `disney_plus_titles.csv` is in the `data` folder.")
        return

    # --- Filters ---
    st.sidebar.header("Filters")
    selected_type = st.sidebar.selectbox("Content Type", ["All", "Movie", "TV Show"], key="disney_type")
    
    if selected_type != "All":
        df_filtered = df[df['type'] == selected_type].copy()
    else:
        df_filtered = df.copy()

    # --- KPI Section ---
    total_titles = df_filtered.shape[0]
    movies = df_filtered[df_filtered['type'] == 'Movie'].shape[0]
    tv_shows = df_filtered[df_filtered['type'] == 'TV Show'].shape[0]
    newest_addition = pd.to_datetime(df['date_added'], errors='coerce').dt.year.max() if not df['date_added'].dropna().empty else "N/A"

    with st.container():
        
        kpi_cols = st.columns(4)
        kpi_cols[0].metric(label="Total Titles", value=f"{total_titles:,}")
        kpi_cols[1].metric(label="Movies", value=f"{movies:,}")
        kpi_cols[2].metric(label="TV Shows", value=f"{tv_shows:,}")
        kpi_cols[3].metric(label="Latest Content Year", value=newest_addition)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Main Dashboard with Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Content Overview", "📊 Genre & Rating Analysis", "📈 Temporal Trends", "🌍 Geographic Insights"])

    with tab1:
        st.subheader("Library Composition")
        col1, col2 = st.columns([1, 2])
        with col1:
            
            st.markdown("##### Content Type Distribution")
            fig_pie = px.pie(df_filtered, names='type', title='', 
                             color_discrete_map={'Movie':'#3E82FC', 'TV Show':"#CFCF5A"})
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
            fig_hist.add_trace(go.Histogram(x=df_movies['duration_int'], name='Movies (mins)', marker_color='#3E82FC'))
            fig_hist.add_trace(go.Histogram(x=df_tv['duration_int'], name='TV Shows (seasons)', marker_color='#1DA1F2'))
            fig_hist.update_layout(barmode='overlay', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig_hist.update_traces(opacity=0.75)
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("Genre and Audience Analysis")
        col1, col2 = st.columns(2)
        with col1:
            
            st.markdown("##### Top 10 Genres")
            top_genres = df_filtered['listed_in'].str.split(', ').explode().value_counts().nlargest(10)
            fig_bar = px.bar(top_genres, y=top_genres.values, x=top_genres.index,
                             color=top_genres.values, color_continuous_scale='Blues')
            fig_bar.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
           
            st.markdown("##### Content by Maturity Rating")
            rating_counts = df_filtered['rating'].value_counts().nlargest(10)
            fig_treemap = px.treemap(rating_counts, path=[rating_counts.index], values=rating_counts.values,
                                     color=rating_counts.values, color_continuous_scale='Blues')
            fig_treemap.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_treemap, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Content Growth & Seasonality")
        col1, col2 = st.columns(2)
        with col1:
            
            st.markdown("##### Content Added Per Year")
            df_filtered['date_added'] = pd.to_datetime(df_filtered['date_added'], errors='coerce')
            year_counts = df_filtered['date_added'].dt.year.value_counts().sort_index()
            fig_line = px.line(year_counts, x=year_counts.index, y=year_counts.values, markers=True,
                               labels={'y':'Titles Added', 'x':'Year'})
            fig_line.update_traces(line_color='#3E82FC', line_width=3)
            fig_line.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            
            st.markdown("##### Content Added by Month")
            df_filtered['month_added'] = df_filtered['date_added'].dt.month_name()
            month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            month_counts = df_filtered['month_added'].value_counts().reindex(month_order)
            
            fig_radar = px.line_polar(month_counts, r=month_counts.values, theta=month_counts.index, 
                                      line_close=True, template='plotly_dark',
                                      color_discrete_sequence=['#1DA1F2'])
            fig_radar.update_traces(fill='toself')
            fig_radar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.subheader("Geographic Production Insights")
   
        st.markdown("##### Top 15 Content Producing Countries")
        country_counts = df_filtered['country'].str.split(', ').explode().dropna().value_counts().nlargest(15)
        fig_map_bar = px.bar(country_counts, y=country_counts.values, x=country_counts.index, 
                             color=country_counts.values, color_continuous_scale='Blues',
                             labels={'y':'Number of Titles', 'x':'Country'})
        fig_map_bar.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_map_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BI Insights Section ---
    generate_disney_insights(df_filtered)

