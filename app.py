# 🎵 SPOTIFY PREDICTOR - ULTRA VERSION
# Social sharing, dynamic background, interactive elements, minimal icons, song info

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import time
import json
from datetime import datetime
import urllib.parse

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Spotify Predictor",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ADVANCED CSS - ANIMATED BACKGROUND + INTERACTIVE
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
    --spotify-green: #1DB954;
    --spotify-light-green: #1ed760;
    --dark-bg: #0F172A;
    --card-bg: #1A1F3A;
    --text-primary: #FFFFFF;
    --text-secondary: rgba(255, 255, 255, 0.7);
}

* {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ANIMATED BACKGROUND */
html, body, .main {
    background: linear-gradient(-45deg, #0F172A, #1A1F3A, #0F172A, #1A2F4A);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: var(--text-primary);
    position: relative;
    overflow-x: hidden;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating particles effect */
.main::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(29, 185, 84, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(30, 215, 96, 0.1) 0%, transparent 50%);
    animation: float 20s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Main animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

@keyframes glow {
    0%, 100% { text-shadow: 0 0 10px rgba(29, 185, 84, 0.5); }
    50% { text-shadow: 0 0 20px rgba(29, 185, 84, 0.8); }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

.page-container {
    animation: fadeInUp 0.6s ease-out;
    padding: 20px;
    position: relative;
    z-index: 1;
}

/* Interactive Spotify Card */
.spotify-card {
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.9) 0%, rgba(20, 30, 50, 0.9) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(29, 185, 84, 0.3);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 8px 32px rgba(29, 185, 84, 0.1);
    position: relative;
    overflow: hidden;
}

.spotify-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shimmer 3s infinite;
}

.spotify-card:hover {
    background: linear-gradient(135deg, rgba(40, 50, 70, 0.95) 0%, rgba(30, 40, 60, 0.95) 100%);
    border-color: rgba(29, 185, 84, 0.6);
    transform: translateY(-8px);
    box-shadow: 0 15px 40px rgba(29, 185, 84, 0.25);
}

/* Gradient Text */
.gradient-text {
    background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

.gradient-text-large {
    background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 800;
    animation: glow 2s ease-in-out infinite;
}

/* Interactive Metric Card */
.metric-card {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(29, 185, 84, 0.05) 100%);
    border: 1px solid rgba(29, 185, 84, 0.4);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
}

.metric-card:hover {
    border-color: var(--spotify-green);
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.25) 0%, rgba(29, 185, 84, 0.1) 100%);
    transform: scale(1.08) rotateY(5deg);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.2);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--spotify-light-green);
    margin: 10px 0;
    letter-spacing: -1px;
    transition: transform 0.3s ease;
}

.metric-card:hover .metric-value {
    transform: scale(1.1);
}

.metric-label {
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Interactive Tags */
.tag {
    display: inline-block;
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.25) 0%, rgba(29, 185, 84, 0.1) 100%);
    border: 1px solid rgba(29, 185, 84, 0.5);
    color: var(--spotify-light-green);
    padding: 8px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    margin: 4px;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
}

.tag:hover {
    background: rgba(29, 185, 84, 0.3);
    border-color: var(--spotify-green);
    box-shadow: 0 4px 12px rgba(29, 185, 84, 0.2);
    transform: translateY(-2px);
}

/* Divider */
.divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(29, 185, 84, 0.4), transparent);
    margin: 24px 0;
    animation: pulse 2s ease-in-out infinite;
}

/* Music Visualizer */
.visualizer {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 4px;
    height: 80px;
    margin: 30px 0;
}

.visualizer-bar {
    width: 10px;
    background: linear-gradient(180deg, #1DB954, #1ed760);
    border-radius: 5px;
    animation: bounce 0.6s ease-in-out infinite;
    box-shadow: 0 0 10px rgba(29, 185, 84, 0.5);
}

@keyframes bounce {
    0%, 100% { height: 15px; }
    50% { height: 60px; }
}

.visualizer-bar:nth-child(1) { animation-delay: 0s; }
.visualizer-bar:nth-child(2) { animation-delay: 0.1s; }
.visualizer-bar:nth-child(3) { animation-delay: 0.2s; }
.visualizer-bar:nth-child(4) { animation-delay: 0.3s; }
.visualizer-bar:nth-child(5) { animation-delay: 0.4s; }
.visualizer-bar:nth-child(6) { animation-delay: 0.5s; }
.visualizer-bar:nth-child(7) { animation-delay: 0.4s; }
.visualizer-bar:nth-child(8) { animation-delay: 0.3s; }

/* Social Share Buttons */
.social-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 20px 0;
    justify-content: center;
}

.social-btn {
    padding: 12px 20px;
    border: none;
    border-radius: 50px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.instagram-btn {
    background: linear-gradient(135deg, #F58529 0%, #DD2A7B 50%, #8134AF 100%);
}

.twitter-btn {
    background: #1DA1F2;
}

.whatsapp-btn {
    background: #25D366;
}

.spotify-btn {
    background: var(--spotify-green);
}

.youtube-btn {
    background: #FF0000;
}

.social-btn:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.social-btn:active {
    transform: translateY(-1px);
}

/* Song Card Interactive */
.song-card {
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.8) 0%, rgba(20, 30, 50, 0.8) 100%);
    border: 1px solid rgba(29, 185, 84, 0.2);
    border-radius: 12px;
    padding: 16px;
    margin: 10px 0;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
}

.song-card:hover {
    border-color: var(--spotify-green);
    background: linear-gradient(135deg, rgba(40, 50, 70, 0.9) 0%, rgba(30, 40, 60, 0.9) 100%);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.15);
    transform: translateX(8px);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    color: black;
    font-weight: 700;
    border: none;
    border-radius: 24px;
    padding: 12px 32px;
    font-size: 1rem;
    transition: all 0.3s ease;
    cursor: pointer;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.4);
}

.stButton > button:active {
    transform: translateY(0px);
}

/* Login Form */
.login-container {
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.95) 0%, rgba(20, 30, 50, 0.95) 100%);
    border: 1px solid rgba(29, 185, 84, 0.3);
    padding: 40px;
    border-radius: 20px;
    max-width: 500px;
    margin: 50px auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: fadeInUp 0.6s ease-out;
}

/* Scrollbar */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: rgba(40, 40, 40, 0.3); }
::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, #1DB954, #1ed760);
    border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover { 
    background: linear-gradient(180deg, #1ed760, #1DB954);
}

/* Info Box */
.info-box {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.2) 0%, rgba(29, 215, 96, 0.1) 100%);
    border: 1px solid rgba(29, 185, 84, 0.4);
    padding: 16px;
    border-radius: 10px;
    margin: 10px 0;
    font-size: 0.95rem;
}

/* Slider Container */
.slider-group {
    background: rgba(30, 40, 60, 0.5);
    padding: 20px;
    border-radius: 12px;
    margin: 10px 0;
    border: 1px solid rgba(29, 185, 84, 0.2);
    transition: all 0.3s ease;
}

.slider-group:hover {
    background: rgba(30, 40, 60, 0.7);
    border-color: rgba(29, 185, 84, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHING
# ============================================================================

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/spotify_songs_expanded.csv')
        return df
    except:
        df = pd.read_csv('spotify_songs_expanded.csv')
        return df

@st.cache_resource
def load_model():
    try:
        with open('model_lr.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

# Sample song info database
@st.cache_data
def get_song_info():
    return {
        "Blinding Lights": {
            "artist": "The Weeknd",
            "spotify": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMwbk",
            "youtube": "https://www.youtube.com/watch?v=4NRXx6U8ABQ",
            "genre": "Synthwave Pop"
        },
        "Shape of You": {
            "artist": "Ed Sheeran",
            "spotify": "https://open.spotify.com/track/7qiZfU4dY1lsylvNEJik4j",
            "youtube": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
            "genre": "Pop"
        },
        "Levitating": {
            "artist": "Dua Lipa",
            "spotify": "https://open.spotify.com/track/3UIVDhQVkeaJnXM4QYLiWi",
            "youtube": "https://www.youtube.com/watch?v=TUVcZfQe-Kw",
            "genre": "Disco Pop"
        },
    }

df = load_data()
model = load_model()
song_info_db = get_song_info()

# ============================================================================
# SESSION STATE
# ============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Predictor"

if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'predictions_made': 0,
        'favorites': [],
        'last_prediction': None
    }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def predict_popularity(features):
    try:
        if model is not None:
            feature_values = np.array([features]).reshape(1, -1)
            prediction = model.predict(feature_values)[0]
            return max(0, min(100, prediction))
        else:
            danceability, energy, valence = features[0], features[1], features[10]
            score = (danceability * 30 + energy * 25 + valence * 20 + 25)
            return max(0, min(100, score))
    except:
        return 50

def create_music_visualizer():
    return """
    <div class='visualizer'>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
        <div class='visualizer-bar'></div>
    </div>
    """

def share_on_social(platform, message):
    """Generate social share URLs and handle opening"""
    encoded_msg = urllib.parse.quote(message)
    
    urls = {
        'instagram': f"https://www.instagram.com/?text={encoded_msg}",
        'twitter': f"https://twitter.com/intent/tweet?text={encoded_msg}",
        'whatsapp': f"https://wa.me/?text={encoded_msg}",
        'facebook': f"https://www.facebook.com/sharer/sharer.php?quote={encoded_msg}",
    }
    
    return urls.get(platform, '#')

# ============================================================================
# AUTHENTICATION PAGE
# ============================================================================

def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='page-container' style='text-align: center;'>
            <h1 style='font-size: 4rem; margin-bottom: 10px;'>
                <span class='gradient-text-large'>♪</span>
            </h1>
            <h2 style='font-size: 2.5rem; margin: 20px 0; font-weight: 800;'>
                SPOTIFY PREDICTOR
            </h2>
            <p style='color: rgba(255,255,255,0.6); font-size: 1.2rem; margin-bottom: 40px;'>
                Predict Your Song's Popularity & Share With Friends
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown("<div class='login-container'>", unsafe_allow_html=True)
            st.markdown("### Welcome Back")
            st.info("Demo: demo / demo123")
            
            username = st.text_input("Username", placeholder="Enter username", value="demo", key="signin_user")
            password = st.text_input("Password", type="password", placeholder="Enter password", value="demo123", key="signin_pass")
            
            if st.button("Sign In", use_container_width=True, key="signin_btn"):
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<div class='login-container'>", unsafe_allow_html=True)
            st.markdown("### Create Account")
            
            new_username = st.text_input("Username", placeholder="Create username", key="signup_user")
            new_email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
            new_password = st.text_input("Password", type="password", placeholder="Create password", key="signup_pass")
            
            if st.button("Create Account", use_container_width=True, key="signup_btn"):
                if new_username and new_email and new_password:
                    st.session_state.authenticated = True
                    st.session_state.username = new_username
                    st.success(f"Account created! Welcome, {new_username}!")
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def show_app():
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: #1DB954; font-size: 2.5rem; margin: 0;'>♪</h2>
            <h3 style='font-weight: 800; margin: 10px 0;'>SPOTIFY</h3>
            <p style='color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;'>
                {st.session_state.username}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        pages = ["Predictor", "Browse", "Analytics", "Favorites", "Profile"]
        selected = st.radio("Navigation", pages, key="nav")
        st.session_state.current_page = selected
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # ====== PREDICTOR PAGE ======
    if st.session_state.current_page == "Predictor":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        
        st.markdown("""
        <h1 style='font-size: 3rem; text-align: center; margin-bottom: 20px;'>
            <span class='gradient-text'>Predict Your Song</span>
        </h1>
        """, unsafe_allow_html=True)
        
        st.markdown(create_music_visualizer(), unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Song Info
        col1, col2 = st.columns(2)
        with col1:
            song_title = st.text_input("Song Title", placeholder="e.g., Blinding Lights", key="song")
        with col2:
            artist = st.text_input("Artist", placeholder="e.g., The Weeknd", key="artist")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin: 20px 0;'>Song Features</h3>", unsafe_allow_html=True)
        
        # Feature Sliders
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            danceability = st.slider("Danceability", 0.0, 1.0, 0.65, 0.01, key="dance")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            energy = st.slider("Energy", 0.0, 1.0, 0.65, 0.01, key="energy")
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            valence = st.slider("Valence", 0.0, 1.0, 0.50, 0.01, key="valence")
            st.markdown("</div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            acousticness = st.slider("Acousticness", 0.0, 1.0, 0.15, 0.01, key="acoustic")
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            speechiness = st.slider("Speechiness", 0.0, 1.0, 0.05, 0.01, key="speech")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            instrumentalness = st.slider("Instrumentalness", 0.0, 1.0, 0.0, 0.01, key="instr")
            st.markdown("</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            liveness = st.slider("Liveness", 0.0, 1.0, 0.10, 0.01, key="live")
            st.markdown("</div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            key = st.slider("Key", 0, 11, 5, key="key_slider")
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            tempo = st.slider("Tempo (BPM)", 50, 200, 120, key="tempo")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='slider-group'>", unsafe_allow_html=True)
            duration_ms = st.slider("Duration (ms)", 60000, 600000, 180000, 1000, key="duration")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("PREDICT POPULARITY", use_container_width=True, key="predict"):
                if not song_title or not artist:
                    st.error("Please enter song title and artist!")
                else:
                    with st.spinner("Analyzing..."):
                        time.sleep(0.5)
                        features = [danceability, energy, key, 0, 1, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, 4]
                        prediction = predict_popularity(features)
                        
                        st.session_state.user_data['predictions_made'] += 1
                        st.session_state.user_data['last_prediction'] = {
                            'song': song_title,
                            'artist': artist,
                            'score': prediction
                        }
        
        # RESULT
        if st.session_state.user_data['last_prediction']:
            last = st.session_state.user_data['last_prediction']
            pred = last['score']
            
            st.markdown("""
            <div class='spotify-card' style='border: 2px solid #1DB954; margin: 30px 0; text-align: center;'>
                <h2 style='color: #1ed760;'>PREDICTION RESULT</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem; margin: 0;'>Song</div>
                    <div style='font-size: 1.2rem; font-weight: 700; margin: 8px 0;'>{last['song']}</div>
                    <div style='font-size: 0.85rem; opacity: 0.7;'>{last['artist']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem; margin: 0;'>Score</div>
                    <div class='metric-value'>{int(pred)}</div>
                    <div style='font-size: 0.85rem; opacity: 0.7;'>/100</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                status = "Hit" if pred >= 80 else "Good" if pred >= 60 else "Potential"
                color = "#1DB954" if pred >= 60 else "#06B6D4"
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem; margin: 0;'>Status</div>
                    <div style='font-size: 1.3rem; color: {color}; font-weight: 700; margin: 8px 0;'>{status}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Key Insights
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin: 20px 0;'>Key Factors</h3>", unsafe_allow_html=True)
            
            insights = []
            if danceability > 0.7:
                insights.append(("High Danceability", "Great for dancing"))
            if energy > 0.7:
                insights.append(("High Energy", "Perfect for workouts"))
            if valence > 0.6:
                insights.append(("Uplifting Vibes", "Positive mood"))
            if acousticness > 0.5:
                insights.append(("Acoustic", "Organic sound"))
            
            if insights:
                cols = st.columns(len(insights))
                for col, (title, desc) in zip(cols, insights):
                    with col:
                        st.markdown(f"""
                        <div class='info-box'>
                            <strong style='color: #1DB954;'>{title}</strong>
                            <div style='font-size: 0.9rem; opacity: 0.8;'>{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # SOCIAL SHARING
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Share Your Result</h3>", unsafe_allow_html=True)
            
            share_msg = f"🎵 {last['song']} by {last['artist']} - Predicted popularity: {int(pred)}/100! Check it out!"
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button("📱 Instagram", use_container_width=True, key=f"ig_{last['song']}"):
                    url = share_on_social('instagram', share_msg)
                    st.markdown(f"[Open Instagram]({url})", unsafe_allow_html=True)
            
            with col2:
                if st.button("𝕏 Twitter", use_container_width=True, key=f"tw_{last['song']}"):
                    url = share_on_social('twitter', share_msg + " #SpotifyPredictor")
                    st.markdown(f"[Open Twitter]({url})", unsafe_allow_html=True)
            
            with col3:
                if st.button("💬 WhatsApp", use_container_width=True, key=f"wa_{last['song']}"):
                    url = share_on_social('whatsapp', share_msg)
                    st.markdown(f"[Open WhatsApp]({url})", unsafe_allow_html=True)
            
            with col4:
                if st.button("🎵 Spotify", use_container_width=True, key=f"spotify_{last['song']}"):
                    st.info("Search the song on Spotify to listen!")
            
            with col5:
                if st.button("❤️ Save", use_container_width=True, key=f"fav_{last['song']}"):
                    st.session_state.user_data['favorites'].append({
                        'song': last['song'],
                        'artist': last['artist'],
                        'score': int(pred),
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Added to favorites!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== BROWSE PAGE ======
    elif st.session_state.current_page == "Browse":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 3rem;'><span class='gradient-text'>Browse Songs</span></h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            min_pop = st.slider("Min Popularity", 0, 100, 50, key="min")
        with col2:
            max_pop = st.slider("Max Popularity", 0, 100, 100, key="max")
        with col3:
            search = st.text_input("Search", placeholder="Artist name", key="search")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        filtered = df[(df['popularity'] >= min_pop) & (df['popularity'] <= max_pop)]
        if search:
            filtered = filtered[filtered['artist_name'].str.contains(search, case=False, na=False)]
        
        filtered = filtered.sort_values('popularity', ascending=False)
        st.markdown(f"**Found {len(filtered)} songs**")
        
        for idx, (_, song) in enumerate(filtered.head(12).iterrows(), 1):
            st.markdown(f"""
            <div class='song-card'>
                <strong style='color: #1DB954;'>#{idx} {song['track_name']}</strong>
                <div style='color: rgba(255,255,255,0.7); margin: 5px 0;'>{song['artist_name']}</div>
                <div style='margin-top: 10px;'>
                    <span class='tag'>Danceability: {song['danceability']:.2f}</span>
                    <span class='tag'>Energy: {song['energy']:.2f}</span>
                    <span class='tag'>Popularity: {int(song['popularity'])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== ANALYTICS PAGE ======
    elif st.session_state.current_page == "Analytics":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 3rem;'><span class='gradient-text'>Music Analytics</span></h1>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class='metric-card'><div>Avg Popularity</div><div class='metric-value'>{df['popularity'].mean():.0f}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='metric-card'><div>Avg Energy</div><div class='metric-value'>{df['energy'].mean():.2f}</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class='metric-card'><div>Avg Danceability</div><div class='metric-value'>{df['danceability'].mean():.2f}</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class='metric-card'><div>Total Songs</div><div class='metric-value'>{len(df)}</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<h3>Top 10 Artists</h3>", unsafe_allow_html=True)
        
        top = df.groupby('artist_name')['popularity'].mean().nlargest(10)
        for idx, (artist, pop) in enumerate(top.items(), 1):
            st.markdown(f"""<div class='spotify-card'><strong>#{idx} {artist}</strong> - {pop:.1f}</div>""", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== FAVORITES PAGE ======
    elif st.session_state.current_page == "Favorites":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 3rem;'><span class='gradient-text'>Your Favorites</span></h1>", unsafe_allow_html=True)
        
        if st.session_state.user_data['favorites']:
            for fav in st.session_state.user_data['favorites']:
                st.markdown(f"""
                <div class='song-card'>
                    <strong style='color: #1DB954;'>❤️ {fav['song']}</strong>
                    <div style='color: rgba(255,255,255,0.7);'>{fav['artist']}</div>
                    <div style='margin-top: 8px;'><span class='tag'>Score: {fav['score']}/100</span></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='info-box' style='text-align: center;'><p>No favorites yet. Start predicting!</p></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== PROFILE PAGE ======
    elif st.session_state.current_page == "Profile":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 3rem;'><span class='gradient-text'>{st.session_state.username}'s Profile</span></h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><div>Predictions</div><div class='metric-value'>{st.session_state.user_data['predictions_made']}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div>Favorites</div><div class='metric-value'>{len(st.session_state.user_data['favorites'])}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div>Member Since</div><div class='metric-value'>Today</div></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN
# ============================================================================

if st.session_state.authenticated:
    show_app()
else:
    show_auth_page()
