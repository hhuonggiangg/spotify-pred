import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import time
import urllib.parse
from datetime import datetime

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Spotify Predictor", page_icon="🎵", layout="wide", initial_sidebar_state="collapsed")

# ============================================================================
# ADVANCED CSS - CURSORS, ANIMATIONS, GRADIENTS, INTERACTIVE
# ============================================================================

CSS_ADVANCED = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap');

* { 
    font-family: 'Poppins', sans-serif;
}

/* ========== CUSTOM CURSORS ========== */
html, body, .main {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="2" fill="%231ed760"/><circle cx="12" cy="12" r="8" fill="none" stroke="%231DB954" stroke-width="1"/></svg>') 12 12, auto;
}

button, a, [role="button"], .cursor-pointer {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="%231ed760" stroke-width="1.5"/><line x1="12" y1="8" x2="12" y2="16" stroke="%231ed760" stroke-width="1.5"/><line x1="8" y1="12" x2="16" y2="12" stroke="%231ed760" stroke-width="1.5"/></svg>') 12 12, pointer;
}

input, textarea, select {
    cursor: text;
}

/* ========== ANIMATED GRADIENT BACKGROUND ========== */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0F172A, #1A2F4A, #1A1F3A, #132238, #0F172A, #1A2F4A);
    background-size: 600% 600%;
    animation: gradientBG 25s ease infinite;
    position: relative;
    overflow: hidden;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    25% { background-position: 50% 100%; }
    50% { background-position: 100% 50%; }
    75% { background-position: 50% 0%; }
    100% { background-position: 0% 50%; }
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(29, 185, 84, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(30, 215, 96, 0.08) 0%, transparent 50%);
    animation: floatParticles 30s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes floatParticles {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-30px) rotate(10deg); }
}

/* ========== PAGE TRANSITIONS ========== */
@keyframes pageSlideIn {
    from {
        opacity: 0;
        transform: translateY(30px) scale(0.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes pageFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.page-container {
    animation: pageSlideIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    padding: 30px 20px;
    position: relative;
    z-index: 1;
}

/* ========== CARDS WITH INTERACTIVE EFFECTS ========== */
.card {
    background: linear-gradient(135deg, rgba(30, 50, 85, 0.85) 0%, rgba(15, 30, 55, 0.85) 100%);
    border: 1px solid rgba(29, 185, 84, 0.3);
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(29, 185, 84, 0.1) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.card:hover {
    background: linear-gradient(135deg, rgba(40, 60, 100, 0.95) 0%, rgba(25, 45, 75, 0.95) 100%);
    border-color: #1DB954;
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 45px rgba(29, 185, 84, 0.3);
}

.card:hover::before {
    opacity: 1;
}

.artist-card {
    background: linear-gradient(135deg, rgba(30, 50, 85, 0.9) 0%, rgba(15, 30, 55, 0.9) 100%);
    border: 2px solid rgba(29, 185, 84, 0.4);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.artist-card:hover {
    background: linear-gradient(135deg, rgba(50, 70, 120, 1) 0%, rgba(35, 55, 95, 1) 100%);
    border-color: #1ed760;
    transform: translateY(-10px) rotateX(5deg);
    box-shadow: 0 20px 50px rgba(29, 185, 84, 0.4);
}

.artist-image {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #1DB954, #1ed760);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
    margin-bottom: 15px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.artist-card:hover .artist-image {
    transform: scale(1.05);
    box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3);
}

/* ========== METRIC CARDS ========== */
.metric {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(20, 35, 60, 0.15) 100%);
    border: 1px solid rgba(29, 185, 84, 0.3);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    position: relative;
}

.metric:hover {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.25) 0%, rgba(29, 185, 84, 0.1) 100%);
    border-color: #1DB954;
    transform: scale(1.12) translateY(-5px);
    box-shadow: 0 12px 35px rgba(29, 185, 84, 0.25);
}

.metric-val {
    font-size: 2.8rem;
    font-weight: 900;
    color: #1ed760;
    margin: 8px 0;
    transition: transform 0.3s ease;
}

.metric:hover .metric-val {
    transform: scale(1.15);
}

/* ========== GRADIENT TEXT ========== */
.gradient-text {
    background: linear-gradient(135deg, #1DB954, #1ed760);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
}

/* ========== TAGS ========== */
.tag {
    display: inline-block;
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.2) 0%, rgba(29, 185, 84, 0.08) 100%);
    border: 1px solid rgba(29, 185, 84, 0.4);
    color: #1ed760;
    padding: 9px 14px;
    border-radius: 18px;
    margin: 5px;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
}

.tag:hover {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.35) 0%, rgba(29, 185, 84, 0.15) 100%);
    border-color: #1DB954;
    transform: translateY(-3px) scale(1.08);
    box-shadow: 0 6px 15px rgba(29, 185, 84, 0.2);
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #1DB954, #1ed760) !important;
    color: black !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 22px !important;
    padding: 14px 32px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: 0 6px 20px rgba(29, 185, 84, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.06) !important;
    box-shadow: 0 15px 40px rgba(29, 185, 84, 0.5) !important;
}

/* ========== INPUTS ========== */
.stTextInput > div > div > input {
    background: rgba(25, 40, 70, 0.8) !important;
    border: 1.5px solid rgba(29, 185, 84, 0.3) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    background: rgba(25, 40, 70, 0.95) !important;
    border-color: #1DB954 !important;
    box-shadow: 0 0 20px rgba(29, 185, 84, 0.25) !important;
    transform: scale(1.01);
}

/* ========== SLIDERS ========== */
.stSlider > div > div {
    background: rgba(29, 185, 84, 0.1) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(29, 185, 84, 0.2) !important;
    padding: 12px !important;
    transition: all 0.3s ease !important;
}

.stSlider > div > div:hover {
    background: rgba(29, 185, 84, 0.15) !important;
    border-color: rgba(29, 185, 84, 0.4) !important;
}

/* ========== MODAL ========== */
.modal {
    display: none;
    position: fixed;
    z-index: 100;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    background: linear-gradient(135deg, rgba(30, 50, 85, 0.98) 0%, rgba(15, 30, 55, 0.98) 100%);
    margin: 5% auto;
    padding: 30px;
    border: 2px solid rgba(29, 185, 84, 0.4);
    border-radius: 25px;
    width: 90%;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-50px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.close-btn {
    color: #1ed760;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.close-btn:hover {
    color: #FF4500;
    transform: rotate(90deg);
}

/* ========== VISUALIZER ========== */
.visualizer {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 6px;
    height: 100px;
    margin: 30px 0;
}

.bar {
    width: 12px;
    background: linear-gradient(180deg, #1DB954, #1ed760);
    border-radius: 6px;
    animation: bars 0.8s ease-in-out infinite;
    box-shadow: 0 0 12px rgba(29, 185, 84, 0.6);
}

@keyframes bars {
    0%, 100% { height: 15px; }
    50% { height: 65px; }
}

.bar:nth-child(1) { animation-delay: 0s; }
.bar:nth-child(2) { animation-delay: 0.1s; }
.bar:nth-child(3) { animation-delay: 0.2s; }
.bar:nth-child(4) { animation-delay: 0.3s; }
.bar:nth-child(5) { animation-delay: 0.4s; }
.bar:nth-child(6) { animation-delay: 0.5s; }
.bar:nth-child(7) { animation-delay: 0.4s; }
.bar:nth-child(8) { animation-delay: 0.3s; }

/* ========== LOGIN ========== */
.login-box {
    background: linear-gradient(135deg, rgba(30, 50, 85, 0.95) 0%, rgba(15, 30, 55, 0.95) 100%);
    border: 2px solid rgba(29, 185, 84, 0.3);
    padding: 45px;
    border-radius: 22px;
    max-width: 480px;
    margin: 60px auto;
    box-shadow: 0 25px 70px rgba(0, 0, 0, 0.5);
    animation: pageSlideIn 0.7s ease-out;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 25, 45, 0.95), rgba(10, 20, 40, 0.95)) !important;
    border-right: 1.5px solid rgba(29, 185, 84, 0.2) !important;
}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar { width: 12px; }
::-webkit-scrollbar-track { background: rgba(20, 30, 50, 0.4); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #1DB954, #1ed760);
    border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #1ed760, #1DB954);
}

/* ========== INTERACTIVE LINKS ========== */
.artist-link {
    display: inline-block;
    padding: 12px 20px;
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.2), rgba(29, 185, 84, 0.1));
    border: 1px solid rgba(29, 185, 84, 0.4);
    border-radius: 12px;
    color: #1ed760;
    text-decoration: none;
    margin: 8px;
    transition: all 0.3s ease;
    font-weight: 600;
}

.artist-link:hover {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.4), rgba(29, 185, 84, 0.2));
    border-color: #1DB954;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.2);
}

h1, h2, h3 {
    animation: pageFadeIn 0.5s ease-out;
}
</style>
"""

st.markdown(CSS_ADVANCED, unsafe_allow_html=True)

# ============================================================================
# ARTIST DATABASE
# ============================================================================

ARTISTS_DB = {
    "The Weeknd": {
        "emoji": "🎤",
        "image": "🌙",
        "bio": "Canadian singer, songwriter, and record producer",
        "spotify": "https://open.spotify.com/artist/1Xyo4u8uTS0wX3xdigHP7G",
        "youtube": "https://www.youtube.com/c/TheWeeknd",
        "genres": ["Pop", "R&B", "Alternative"],
        "hits": ["Blinding Lights", "Starboy", "The Hills"],
    },
    "Ed Sheeran": {
        "emoji": "🎸",
        "image": "🔴",
        "bio": "English singer-songwriter known for pop and folk music",
        "spotify": "https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V",
        "youtube": "https://www.youtube.com/user/EdSheeranVEVO",
        "genres": ["Pop", "Folk", "Acoustic"],
        "hits": ["Shape of You", "Perfect", "Thinking Out Loud"],
    },
    "Dua Lipa": {
        "emoji": "💃",
        "image": "💫",
        "bio": "British-Kosovar pop singer and songwriter",
        "spotify": "https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we",
        "youtube": "https://www.youtube.com/channel/UCoKzVrXRK3l-uXZaYzYHoVA",
        "genres": ["Pop", "Disco", "Synthpop"],
        "hits": ["Levitating", "Don't Start Now", "Break My Heart"],
    },
    "Ariana Grande": {
        "emoji": "✨",
        "image": "🎀",
        "bio": "American pop singer and songwriter",
        "spotify": "https://open.spotify.com/artist/66CXWjxzNUsdJxJ2JdwL6V",
        "youtube": "https://www.youtube.com/c/ArianaGrande",
        "genres": ["Pop", "R&B", "Vocal"],
        "hits": ["Thank U, Next", "Into You", "No Tears Left to Cry"],
    },
    "The Weeknd": {
        "emoji": "🎭",
        "image": "🌃",
        "bio": "Canadian artist known for dark pop and R&B",
        "spotify": "https://open.spotify.com/artist/1Xyo4u8uTS0wX3xdigHP7G",
        "youtube": "https://www.youtube.com/c/TheWeeknd",
        "genres": ["Pop", "R&B", "Hip-Hop"],
        "hits": ["Blinding Lights", "Starboy", "The Hills"],
    }
}

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    try:
        return pd.read_csv('data/spotify_songs_expanded.csv')
    except:
        return pd.read_csv('spotify_songs_expanded.csv')

@st.cache_resource
def load_model():
    try:
        with open('model_lr.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

df = load_data()
model = load_model()

# ============================================================================
# SESSION STATE
# ============================================================================

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "Predictor"
if 'stats' not in st.session_state:
    st.session_state.stats = {'preds': 0, 'favs': [], 'last': None}
if 'modal_artist' not in st.session_state:
    st.session_state.modal_artist = None

# ============================================================================
# FUNCTIONS
# ============================================================================

def predict(features):
    if model:
        try:
            return max(0, min(100, model.predict(np.array([features]).reshape(1, -1))[0]))
        except:
            return 50
    return 50

def share_url(platform, msg):
    enc = urllib.parse.quote(msg)
    urls = {
        'instagram': f"https://www.instagram.com/?text={enc}",
        'twitter': f"https://twitter.com/intent/tweet?text={enc}",
        'whatsapp': f"https://wa.me/?text={enc}",
        'telegram': f"https://t.me/share/url?text={enc}",
    }
    return urls.get(platform, '#')

def render_visualizer():
    return '<div class="visualizer">' + ''.join(['<div class="bar"></div>' for _ in range(8)]) + '</div>'

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="page-container" style="text-align: center;"><h1 style="font-size: 4.5rem; margin: 0;">♪</h1></div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; font-size: 2.8rem;"><span class="gradient-text">SPOTIFY PREDICTOR</span></h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; opacity: 0.6; font-size: 1.1rem;">AI-Powered Song Analysis</p>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.subheader("Welcome Back")
            st.info("Demo: demo / demo123")
            u = st.text_input("Username", value="demo", key="u1")
            p = st.text_input("Password", type="password", value="demo123", key="p1")
            if st.button("ENTER", use_container_width=True, key="b1"):
                if u and p:
                    st.session_state.auth = True
                    st.session_state.user = u
                    st.balloons()
                    time.sleep(0.3)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.subheader("Create Account")
            u2 = st.text_input("Username", key="u2")
            e = st.text_input("Email", key="e")
            p2 = st.text_input("Password", type="password", key="p2")
            if st.button("CREATE", use_container_width=True, key="b2"):
                if u2 and e and p2 and len(p2) >= 6:
                    st.session_state.auth = True
                    st.session_state.user = u2
                    st.balloons()
                    time.sleep(0.3)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ARTIST MODAL
# ============================================================================

def show_artist_modal(artist_name):
    if artist_name in ARTISTS_DB:
        info = ARTISTS_DB[artist_name]
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(30, 50, 85, 0.98), rgba(15, 30, 55, 0.98)); 
                    border: 2px solid #1DB954; border-radius: 25px; padding: 35px; 
                    margin: 30px 0; box-shadow: 0 20px 60px rgba(29, 185, 84, 0.3);">
            <h2 style="color: #1ed760; text-align: center; margin: 0;">{artist_name} {info['emoji']}</h2>
            <div style="text-align: center; font-size: 3rem; margin: 20px 0;">{info['image']}</div>
            <p style="text-align: center; opacity: 0.8; font-size: 1rem; margin: 15px 0;">{info['bio']}</p>
            
            <div style="margin: 20px 0;">
                <h4 style="color: #1DB954;">🎵 Genres:</h4>
                <div style="margin: 10px 0;">
                    {''.join([f'<span class="tag">{g}</span>' for g in info['genres']])}
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <h4 style="color: #1DB954;">🎼 Popular Hits:</h4>
                <div style="margin: 10px 0;">
                    {''.join([f'<span class="tag">{h}</span>' for h in info['hits']])}
                </div>
            </div>
            
            <div style="margin: 25px 0; display: flex; flex-wrap: wrap; justify-content: center; gap: 10px;">
                <a href="{info['spotify']}" target="_blank" style="display: inline-block; padding: 12px 20px; 
                   background: linear-gradient(135deg, #1DB954, #1ed760); color: black; text-decoration: none; 
                   border-radius: 12px; font-weight: 700; transition: all 0.3s ease;">🎵 Spotify</a>
                <a href="{info['youtube']}" target="_blank" style="display: inline-block; padding: 12px 20px; 
                   background: linear-gradient(135deg, #FF0000, #FF4500); color: white; text-decoration: none; 
                   border-radius: 12px; font-weight: 700; transition: all 0.3s ease;">📺 YouTube</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main_app():
    with st.sidebar:
        st.markdown('<h2 style="color: #1DB954; text-align: center; margin: 0;">♪</h2>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: white; margin: 10px 0;">SPOTIFY</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; opacity: 0.6;">@{st.session_state.user}</p>', unsafe_allow_html=True)
        st.divider()
        
        pages = ["Predictor", "Browse", "Analytics", "Favorites", "Profile"]
        old_page = st.session_state.page
        st.session_state.page = st.radio("Navigation", pages, label_visibility="collapsed")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()
    
    # ====== PREDICTOR PAGE ======
    if st.session_state.page == "Predictor":
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center;"><span class="gradient-text">🎵 Predict Your Song</span></h1>', unsafe_allow_html=True)
        st.markdown(render_visualizer(), unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: song = st.text_input("Song Title", placeholder="e.g., Blinding Lights")
        with c2: artist = st.text_input("Artist Name", placeholder="e.g., The Weeknd")
        
        st.markdown('<hr style="border: 1px solid rgba(29, 185, 84, 0.2); margin: 20px 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">📊 Audio Features</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: dance = st.slider("Danceability", 0.0, 1.0, 0.65, 0.01)
        with col2: energy = st.slider("Energy", 0.0, 1.0, 0.65, 0.01)
        with col3: valence = st.slider("Valence", 0.0, 1.0, 0.50, 0.01)
        with col4: acoustic = st.slider("Acousticness", 0.0, 1.0, 0.15, 0.01)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: speech = st.slider("Speechiness", 0.0, 1.0, 0.05, 0.01)
        with col2: instr = st.slider("Instrumentalness", 0.0, 1.0, 0.0, 0.01)
        with col3: live = st.slider("Liveness", 0.0, 1.0, 0.10, 0.01)
        with col4: key_v = st.slider("Key", 0, 11, 5)
        
        col1, col2 = st.columns(2)
        with col1: tempo = st.slider("Tempo (BPM)", 50, 200, 120)
        with col2: duration = st.slider("Duration (ms)", 60000, 600000, 180000, 1000)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 PREDICT POPULARITY", use_container_width=True):
                if song and artist:
                    with st.spinner("🔍 Analyzing audio features..."):
                        time.sleep(0.6)
                        feats = [dance, energy, key_v, 0, 1, speech, acoustic, instr, live, valence, tempo, duration, 4]
                        score = predict(feats)
                        st.session_state.stats['preds'] += 1
                        st.session_state.stats['last'] = {'song': song, 'artist': artist, 'score': score}
        
        if st.session_state.stats['last']:
            p = st.session_state.stats['last']
            st.markdown('<div class="card" style="border: 2px solid #1DB954; text-align: center;"><h2 style="color: #1ed760;">✨ PREDICTION RESULT ✨</h2></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric"><div style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">Song</div><div style="font-size: 1.2rem; font-weight: 900; color: #1ed760;">{p["song"]}</div><div style="font-size: 0.9rem; opacity: 0.6;">{p["artist"]}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric"><div style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">Score</div><div class="metric-val">{int(p["score"])}</div><div style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">/100</div></div>', unsafe_allow_html=True)
            with col3:
                s = p["score"]
                badge = "🔥 HIT" if s >= 80 else "⭐ STRONG" if s >= 60 else "📈 POTENTIAL"
                col_v = "#FF4500" if s >= 80 else "#1DB954" if s >= 60 else "#06B6D4"
                st.markdown(f'<div class="metric"><div style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">Status</div><div style="font-size: 1.3rem; color: {col_v}; font-weight: 900;">{badge}</div></div>', unsafe_allow_html=True)
            
            st.markdown('<hr style="border: 1px solid rgba(29, 185, 84, 0.2); margin: 20px 0;">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center;">📤 Share Result</h3>', unsafe_allow_html=True)
            
            msg = f"🎵 {p['song']} - Score: {int(p['score'])}/100! #SpotifyPredictor"
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("Instagram", use_container_width=True, key="ig"):
                    st.markdown(f"[Share]({share_url('instagram', msg)})")
            with c2:
                if st.button("Twitter", use_container_width=True, key="tw"):
                    st.markdown(f"[Share]({share_url('twitter', msg)})")
            with c3:
                if st.button("WhatsApp", use_container_width=True, key="wa"):
                    st.markdown(f"[Share]({share_url('whatsapp', msg)})")
            with c4:
                if st.button("Telegram", use_container_width=True, key="tg"):
                    st.markdown(f"[Share]({share_url('telegram', msg)})")
            with c5:
                if st.button("Save ❤️", use_container_width=True, key="fav"):
                    st.session_state.stats['favs'].append({'song': p['song'], 'artist': p['artist'], 'score': int(p['score'])})
                    st.success("✅ Added to favorites!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ====== BROWSE PAGE ======
    elif st.session_state.page == "Browse":
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.markdown('<h1><span class="gradient-text">🎧 Browse & Discover</span></h1>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: minp = st.slider("Min Popularity", 0, 100, 50)
        with c2: maxp = st.slider("Max Popularity", 0, 100, 100)
        with c3: srch = st.text_input("Search Artist", placeholder="Type artist name...")
        
        st.markdown('<hr style="border: 1px solid rgba(29, 185, 84, 0.2); margin: 20px 0;">', unsafe_allow_html=True)
        
        filt = df[(df['popularity'] >= minp) & (df['popularity'] <= maxp)]
        if srch:
            filt = filt[filt['artist_name'].str.contains(srch, case=False, na=False)]
        
        for idx, (_, r) in enumerate(filt.sort_values('popularity', ascending=False).head(25).iterrows(), 1):
            artist_name = r['artist_name']
            artist_info = ARTISTS_DB.get(artist_name, {"emoji": "🎤", "image": "🎵"})
            
            if st.button(f"", key=f"artist_{idx}_{artist_name}"):
                st.session_state.modal_artist = artist_name
            
            st.markdown(f'''
            <div class="artist-card" onclick="document.getElementById('modal_{idx}').style.display='block';">
                <div class="artist-image">{artist_info["image"]}</div>
                <h4 style="margin: 0; color: #1DB954;"><strong>#{idx} {r["track_name"]}</strong></h4>
                <p style="margin: 5px 0; opacity: 0.7; font-size: 0.95rem; cursor: pointer; color: #1ed760;"><u>{artist_name}</u></p>
                <div style="margin-top: 12px;">
                    <span class="tag">🎵 {r["danceability"]:.2f}</span>
                    <span class="tag">⚡ {r["energy"]:.2f}</span>
                    <span class="tag">📊 {int(r["popularity"])}</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            with st.expander(f"View {artist_name} Info"):
                show_artist_modal(artist_name)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ====== ANALYTICS PAGE ======
    elif st.session_state.page == "Analytics":
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.markdown('<h1><span class="gradient-text">📊 Analytics Dashboard</span></h1>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Avg Popularity</div><div class="metric-val">{df["popularity"].mean():.0f}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Avg Energy</div><div class="metric-val">{df["energy"].mean():.2f}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Avg Danceability</div><div class="metric-val">{df["danceability"].mean():.2f}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Total Songs</div><div class="metric-val">{len(df)}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<h3 style="color: #1DB954;">🏆 Top 15 Artists</h3>', unsafe_allow_html=True)
        for idx, (a, p) in enumerate(df.groupby('artist_name')['popularity'].mean().nlargest(15).items(), 1):
            st.markdown(f'<div class="card"><div style="display: flex; justify-content: space-between;"><strong>#{idx} {a}</strong><span style="color: #1ed760; font-weight: 900;">{p:.1f}</span></div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ====== FAVORITES PAGE ======
    elif st.session_state.page == "Favorites":
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.markdown('<h1><span class="gradient-text">❤️ Your Favorites</span></h1>', unsafe_allow_html=True)
        
        if st.session_state.stats['favs']:
            for idx, f in enumerate(st.session_state.stats['favs']):
                st.markdown(f'<div class="card"><strong style="color: #1DB954;">#{idx+1} ❤️ {f["song"]}</strong><div style="opacity: 0.7; margin: 5px 0;">{f["artist"]}</div><div style="margin-top: 8px;"><span class="tag">Score: {f["score"]}/100</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card" style="text-align: center; padding: 40px;"><div style="font-size: 2.5rem; margin: 15px 0;">💔</div><h3 style="color: rgba(255,255,255,0.8);">No Favorites Yet</h3><p style="opacity: 0.6;">Predict songs and save them here!</p></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ====== PROFILE PAGE ======
    else:
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.markdown(f'<h1><span class="gradient-text">👤 {st.session_state.user}\'s Profile</span></h1>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Predictions Made</div><div class="metric-val">{st.session_state.stats["preds"]}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Favorite Songs</div><div class="metric-val">{len(st.session_state.stats["favs"])}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric"><div style="font-size: 0.85rem;">Status</div><div style="font-size: 1.8rem; color: #1ed760; margin: 8px 0;">✨</div></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if st.session_state.auth:
    main_app()
else:
    login_page()
