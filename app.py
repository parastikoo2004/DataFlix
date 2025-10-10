import streamlit as st
import os
import json
import time
from streamlit_lottie import st_lottie
from components import home_page, netflix_dashboard, prime_dashboard, disney_dashboard, hulu_dashboard

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DataFlix",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- LOAD LOTTIE ANIMATION ---
def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- Animated Loading Screen ---
def show_loading_screen():
    loading_animation = load_lottiefile("assets/loading_animation.json")
    if loading_animation:
        with st.spinner(" "): # Spinner without text
            st_lottie(loading_animation, height=200, key="loading")
            st.markdown("<h3 style='text-align: center;'>Give us a moment to create streaming data into strategy with passion :D </h3>", unsafe_allow_html=True)
            time.sleep(2.5) # Simulate loading time
    else:
        st.warning("Loading animation not found.")
        time.sleep(1)

# --- STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'app_loaded' not in st.session_state:
    st.session_state.app_loaded = False

def set_page(page_name):
    st.session_state.page = page_name

# --- LOAD STYLES ---
def load_css(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    css_file_path = os.path.join(script_dir, file_name)
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')

# --- Main App Logic ---
if not st.session_state.app_loaded:
    show_loading_screen()
    st.session_state.app_loaded = True
    st.rerun() 

else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.header("DataFlix 🔮")
        st.markdown("Welcome to DataFlix, your gateway to streaming analytics!")
        
        PAGES = ["Home", "Netflix", "Prime Video", "Disney+", "Hulu"]
        ICONS = ["🏠", "🔴", "🔵", "⚪", "🟢"]
        
        for page, icon in zip(PAGES, ICONS):
            if st.button(f"{icon} {page}", use_container_width=True, on_click=set_page, args=(page,)):
                pass
            
        st.markdown("---")
        
        # --- BACKGROUND MUSIC TOGGLE ---
        
        st.write("Ambient Music")
        audio_html = """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const audio = document.getElementById("bgMusic");
                const checkbox = document.getElementById("musicToggle");

                if (checkbox) {
                    checkbox.addEventListener('change', function() {
                        if (this.checked) {
                            audio.play();
                        } else {
                            audio.pause();
                        }
                    });
                }
            });
        </script>
        <audio id="bgMusic" loop>
            <source src="https://raw.githubusercontent.com/parastikoo2004/demo/main/ambient-background-347405.mp3" type="audio/mpeg">
        </audio>
        <label class="switch">
            <input type="checkbox" id="musicToggle">
            <span class="slider round"></span>
        </label>
        """
        st.components.v1.html(audio_html, height=35)

    # --- MAIN PAGE ROUTING ---
    PAGE_MAP = {
        "Home": home_page.show_home_page,
        "Netflix": netflix_dashboard.show_netflix_dashboard,
        "Prime Video": prime_dashboard.show_prime_dashboard,
        "Disney+": disney_dashboard.show_disney_dashboard,
        "Hulu": hulu_dashboard.show_hulu_dashboard,
    }

    if st.session_state.page == "Home":
        PAGE_MAP[st.session_state.page](set_page)
    else:
        PAGE_MAP[st.session_state.page]()

