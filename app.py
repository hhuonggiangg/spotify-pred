# 🎵 SPOTIFY PREDICTOR - NEXT GENERATION
# Advanced ML, Custom cursors, Social integration, Dynamic UI

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import time
from datetime import datetime, timedelta
import urllib.parse
import json
from typing import Dict, List, Tuple

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Spotify Predictor",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ADVANCED CUSTOM CSS - MULTIPLE CURSORS + ANIMATIONS
# ============================================================================

ADVANCED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* ========== CUSTOM CURSORS ========== */
html, body, .main, [data-testid="stAppViewContainer"] {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28"><circle cx="14" cy="14" r="1.5" fill="%231ed760"/><circle cx="14" cy="14" r="6" fill="none" stroke="%231DB954" stroke-width="1.5"/></svg>') 14 14, auto;
}

button, a, .stButton > button, [role="button"] {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28"><circle cx="14" cy="14" r="10" fill="none" stroke="%231ed760" stroke-width="1.5"/><path d="M14 10 L14 18 M10 14 L18 14" stroke="%231ed760" stroke-width="1.5" stroke-linecap="round"/></svg>') 14 14, pointer;
}

input, textarea, select, .stTextInput, .stSelectbox {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 28 28"><rect x="2" y="2" width="24" height="24" fill="none" stroke="%231DB954" stroke-width="1.5" rx="3"/><circle cx="14" cy="14" r="1" fill="%231DB954"/></svg>') 14 14, text;
}

/* ========== ANIMATED BACKGROUND ========== */
html, body, .main, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0F172A 0%, #1A2F4A 20%, #1A1F3A 40%, #132238 60%, #0F172A 80%, #1A2F4A 100%);
    background-size: 500% 500%;
    animation: complexBg 30s ease infinite;
    position: relative;
}

@keyframes complexBg {
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
        radial-gradient(circle at 15% 45%, rgba(29, 185, 84, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 85% 75%, rgba(30, 215, 96, 0.08) 0%, transparent 45%);
    animation: multiFloat 40s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes multiFloat {
    0% { transform: translateY(0) translateX(0) rotate(0deg); }
    33% { transform: translateY(-40px) translateX(20px) rotate(120deg); }
    66% { transform: translateY(20px) translateX(-30px) rotate(240deg); }
    100% { transform: translateY(0) translateX(0) rotate(360deg); }
}

/* ========== ANIMATIONS ========== */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(50px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes glow {
    0%, 100% { 
        text-shadow: 0 0 8px rgba(29, 185, 84, 0.4),
                     0 0 16px rgba(29, 185, 84, 0.2);
        filter: drop-shadow(0 0 5px rgba(29, 185, 84, 0.3));
    }
    50% { 
        text-shadow: 0 0 16px rgba(29, 185, 84, 0.8),
                     0 0 32px rgba(29, 185, 84, 0.4);
        filter: drop-shadow(0 0 12px rgba(29, 185, 84, 0.6));
    }
}

@keyframes shimmer {
    0% { background-position: -1200px 0; }
    100% { background-position: 1200px 0; }
}

@keyframes bounce {
    0%, 100% { height: 12px; opacity: 0.6; }
    50% { height: 60px; opacity: 1; }
}

/* ========== CONTAINERS ========== */
.page-container {
    animation: slideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    padding: 35px 20px;
    position: relative;
    z-index: 1;
}

.main {
    position: relative;
    z-index: 1;
}

/* ========== CARDS ========== */
.card {
    background: linear-gradient(135deg, rgba(30, 50, 85, 0.8) 0%, rgba(15, 30, 55, 0.8) 100%);
    backdrop-filter: blur(25px);
    border: 1.5px solid rgba(29, 185, 84, 0.28);
    border-radius: 20px;
    padding: 28px;
    transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
    animation: shimmer 4s infinite;
}

.card:hover {
    background: linear-gradient(135deg, rgba(40, 65, 105, 0.95) 0%, rgba(25, 45, 75, 0.95) 100%);
    border-color: rgba(29, 185, 84, 0.6);
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 20px 60px rgba(29, 185, 84, 0.25);
}

/* ========== GRADIENT TEXT ========== */
.gradient-text {
    background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
    letter-spacing: -1px;
}

.gradient-text-large {
    background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.8rem;
    font-weight: 900;
    animation: glow 2.5s ease-in-out infinite;
    letter-spacing: -2px;
}

/* ========== METRICS ========== */
.metric {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.12) 0%, rgba(20, 35, 60, 0.12) 100%);
    border: 1.5px solid rgba(29, 185, 84, 0.35);
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.metric:hover {
    border-color: #1DB954;
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.3) 0%, rgba(29, 185, 84, 0.1) 100%);
    transform: scale(1.15) translateY(-8px);
    box-shadow: 0 15px 40px rgba(29, 185, 84, 0.3);
}

.metric-value {
    font-size: 3rem;
    font-weight: 900;
    color: #1ed760;
    margin: 12px 0;
    transition: all 0.3s ease;
    letter-spacing: -3px;
}

.metric:hover .metric-value {
    transform: scale(1.2);
    filter: drop-shadow(0 0 10px rgba(29, 185, 84, 0.5));
}

.metric-label {
    color: rgba(255, 255, 255, 0.65);
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ========== TAGS ========== */
.tag {
    display: inline-block;
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.18) 0%, rgba(29, 185, 84, 0.05) 100%);
    border: 1.2px solid rgba(29, 185, 84, 0.42);
    color: #1ed760;
    padding: 11px 18px;
    border-radius: 28px;
    font-size: 0.87rem;
    margin: 7px;
    font-weight: 700;
    transition: all 0.4s ease;
    cursor: pointer;
}

.tag:hover {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.4) 0%, rgba(29, 185, 84, 0.2) 100%);
    border-color: #1DB954;
    transform: translateY(-4px) scale(1.08);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.3);
}

/* ========== DIVIDER ========== */
.divider {
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, rgba(29, 185, 84, 0.35) 25%, rgba(29, 185, 84, 0.35) 75%, transparent 100%);
    margin: 32px 0;
    animation: pulse 2.5s ease-in-out infinite;
}

/* ========== VISUALIZER ========== */
.visualizer {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 6px;
    height: 110px;
    margin: 45px 0;
}

.bar {
    width: 13px;
    background: linear-gradient(180deg, #1DB954 0%, #1ed760 100%);
    border-radius: 7px;
    animation: bounce 0.8s ease-in-out infinite;
    box-shadow: 0 0 15px rgba(29, 185, 84, 0.7);
}

.bar:nth-child(1) { animation-delay: 0s; }
.bar:nth-child(2) { animation-delay: 0.1s; }
.bar:nth-child(3) { animation-delay: 0.2s; }
.bar:nth-child(4) { animation-delay: 0.3s; }
.bar:nth-child(5) { animation-delay: 0.4s; }
.bar:nth-child(6) { animation-delay: 0.5s; }
.bar:nth-child(7) { animation-delay: 0.4s; }
.bar:nth-child(8) { animation-delay: 0.3s; }

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%) !important;
    color: #000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 16px 40px !important;
    font-size: 1.08rem !important;
    transition: all 0.4s ease !important;
    box-shadow: 0 6px 20px rgba(29, 185, 84, 0.35) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-5px) scale(1.08) !important;
    box-shadow: 0 18px 45px rgba(29, 185, 84, 0.5) !important;
}

/* ========== INPUTS ========== */
.stTextInput > div > div > input {
    background: rgba(25, 40, 70, 0.75) !important;
    border: 1.2px solid rgba(29, 185, 84, 0.25) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 13px 18px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    background: rgba(25, 40, 70, 0.95) !important;
    border-color: rgba(29, 185, 84, 0.65) !important;
    box-shadow: 0 0 20px rgba(29, 185, 84, 0.25) !important;
}

/* ========== SONG CARDS ========== */
.song-card {
    background: linear-gradient(135deg, rgba(30, 40, 65, 0.7) 0%, rgba(20, 30, 50, 0.7) 100%);
    border: 1px solid rgba(29, 185, 84, 0.18);
    border-radius: 16px;
    padding: 20px;
    margin: 14px 0;
    transition: all 0.4s ease;
    cursor: pointer;
}

.song-card:hover {
    border-color: #1DB954;
    background: linear-gradient(135deg, rgba(40, 55, 85, 0.9) 0%, rgba(30, 45, 70, 0.9) 100%);
    transform: translateX(12px) scale(1.02);
    box-shadow: 0 12px 32px rgba(29, 185, 84, 0.2);
}

/* ========== LOGIN BOX ========== */
.login-box {
    background: linear-gradient(135deg, rgba(30, 50, 85, 0.95) 0%, rgba(15, 30, 55, 0.95) 100%);
    border: 2px solid rgba(29, 185, 84, 0.35);
    padding: 50px;
    border-radius: 25px;
    max-width: 520px;
    margin: 70px auto;
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
    animation: slideUp 0.9s ease;
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
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(29, 185, 84, 0.3);
}

h1, h2, h3 {
    animation: fadeIn 0.6s ease-out;
}

.info-box {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(30, 215, 96, 0.08) 100%);
    border-left: 5px solid #1DB954;
    padding: 20px;
    border-radius: 12px;
    margin: 18px 0;
}
</style>
"""

st.markdown(ADVANCED_CSS, unsafe_allow_html=True)

# ============================================================================
# ADVANCED DATA OPERATIONS
# ============================================================================

class SongAnalysisEngine:
    """Advanced audio analysis and prediction"""
    def __init__(self):
        self.dataset = self._load_data()
        self.predictor = self._load_predictor()
    
    def _load_data(self):
        try:
            return pd.read_csv('data/spotify_songs_expanded.csv')
        except:
            return pd.read_csv('spotify_songs_expanded.csv')
    
    def _load_predictor(self):
        try:
            with open('model_lr.pkl', 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def compute_score(self, features: List) -> float:
        """Compute popularity score"""
        if self.predictor:
            try:
                return float(max(0, min(100, self.predictor.predict(np.array([features]).reshape(1, -1))[0])))
            except:
                return 50.0
        return 50.0

@st.cache_resource
def get_engine():
    return SongAnalysisEngine()

engine = get_engine()

# ============================================================================
# SESSION STATE
# ============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Predictor"
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {'total_predictions': 0, 'favorites': [], 'last_prediction': None}

# ============================================================================
# LOGIN
# ============================================================================

def render_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='page-container' style='text-align: center;'>
            <h1 style='font-size: 4.8rem; margin: 0;'><span class='gradient-text-large'>♪</span></h1>
            <h2 style='font-size: 3rem; margin: 20px 0;'>SPOTIFY PREDICTOR</h2>
            <p style='color: rgba(255,255,255,0.65); font-size: 1.2rem;'>AI-Powered Song Analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            st.subheader("Welcome Back")
            st.info("Demo: demo / demo123")
            
            user = st.text_input("Username", value="demo", key="u1")
            pwd = st.text_input("Password", type="password", value="demo123", key="p1")
            
            if st.button("ENTER", use_container_width=True, key="b1"):
                if user and pwd:
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.balloons()
                    time.sleep(0.3)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            st.subheader("Create Account")
            
            user2 = st.text_input("Username", key="u2")
            mail = st.text_input("Email", key="m")
            pwd2 = st.text_input("Password", type="password", key="p2")
            
            if st.button("CREATE", use_container_width=True, key="b2"):
                if user2 and mail and pwd2 and len(pwd2) >= 6:
                    st.session_state.authenticated = True
                    st.session_state.username = user2
                    st.balloons()
                    st.success("✅ Account created!")
                    time.sleep(0.3)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def render_main():
    with st.sidebar:
        st.markdown("<h2 style='color: #1DB954; text-align: center;'>♪ SPOTIFY</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; opacity: 0.7;'>@{st.session_state.username}</p>", unsafe_allow_html=True)
        st.divider()
        
        st.session_state.current_page = st.radio("Nav", ["Predictor", "Browse", "Analytics", "Favorites", "Profile"], label_visibility="collapsed")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    if st.session_state.current_page == "Predictor":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'><span class='gradient-text'>🎵 Predict</span></h1>", unsafe_allow_html=True)
        st.markdown('<div class="visualizer">' + ''.join(['<div class="bar"></div>' for _ in range(8)]) + '</div>', unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: song = st.text_input("Song", placeholder="Song title")
        with c2: artist = st.text_input("Artist", placeholder="Artist name")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
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
        with col1: tempo = st.slider("Tempo", 50, 200, 120)
        with col2: duration = st.slider("Duration", 60000, 600000, 180000, 1000)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("PREDICT", use_container_width=True):
                if song and artist:
                    with st.spinner("Analyzing..."):
                        time.sleep(0.6)
                        feats = [dance, energy, key_v, 0, 1, speech, acoustic, instr, live, valence, tempo, duration, 4]
                        score = engine.compute_score(feats)
                        st.session_state.user_stats['total_predictions'] += 1
                        st.session_state.user_stats['last_prediction'] = {'song': song, 'artist': artist, 'score': score}
        
        if st.session_state.user_stats['last_prediction']:
            p = st.session_state.user_stats['last_prediction']
            
            st.markdown('<div class="card" style="border: 2px solid #1DB954; text-align: center; margin: 35px 0;"><h2 style="color: #1ed760; margin: 0;">✨ RESULT ✨</h2></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric"><div class="metric-label">Song</div><div style="font-size: 1.3rem; font-weight: 900; color: #1ed760;">{p["song"]}</div><div style="opacity: 0.7;">{p["artist"]}</div></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="metric"><div class="metric-label">Score</div><div class="metric-value">{int(p["score"])}</div><div class="metric-label">/100</div></div>', unsafe_allow_html=True)
            
            with col3:
                s = p["score"]
                badge = "🔥 HIT" if s >= 80 else "⭐ STRONG" if s >= 60 else "📈 PROMISING"
                col_v = "#FF4500" if s >= 80 else "#1DB954" if s >= 60 else "#06B6D4"
                st.markdown(f'<div class="metric"><div class="metric-label">Status</div><div style="font-size: 1.3rem; color: {col_v}; font-weight: 900;">{badge}</div></div>', unsafe_allow_html=True)
            
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>📤 Share</h3>", unsafe_allow_html=True)
            
            msg = f"🎵 {p['song']} - Score: {int(p['score'])}/100! #SpotifyPredictor"
            enc = urllib.parse.quote(msg)
            
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("Instagram", use_container_width=True, key="ig"):
                    st.markdown(f"[Share](https://www.instagram.com/?text={enc})")
            with c2:
                if st.button("Twitter", use_container_width=True, key="tw"):
                    st.markdown(f"[Share](https://twitter.com/intent/tweet?text={enc})")
            with c3:
                if st.button("WhatsApp", use_container_width=True, key="wa"):
                    st.markdown(f"[Share](https://wa.me/?text={enc})")
            with c4:
                if st.button("Telegram", use_container_width=True, key="tg"):
                    st.markdown(f"[Share](https://t.me/share/url?text={enc})")
            with c5:
                if st.button("❤️ Save", use_container_width=True, key="fav"):
                    st.session_state.user_stats['favorites'].append({'song': p['song'], 'artist': p['artist'], 'score': int(p['score'])})
                    st.success("✅ Saved!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.current_page == "Browse":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1><span class='gradient-text'>🎧 Browse</span></h1>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: minp = st.slider("Min Pop", 0, 100, 50)
        with c2: maxp = st.slider("Max Pop", 0, 100, 100)
        with c3: srch = st.text_input("Search")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        filt = engine.dataset[(engine.dataset['popularity'] >= minp) & (engine.dataset['popularity'] <= maxp)]
        if srch:
            filt = filt[filt['artist_name'].str.contains(srch, case=False, na=False)]
        
        for idx, (_, r) in enumerate(filt.sort_values('popularity', ascending=False).head(20).iterrows(), 1):
            st.markdown(f'<div class="song-card"><div style="display: flex; justify-content: space-between;"><div><strong style="color: #1DB954;">#{idx}</strong> <strong>{r["track_name"]}</strong><div style="opacity: 0.7;">{r["artist_name"]}</div></div><div style="text-align: right; color: #1ed760; font-weight: 900;">{int(r["popularity"])}</div></div><div style="margin-top: 12px;"><span class="tag">Energy: {r["energy"]:.2f}</span><span class="tag">Dance: {r["danceability"]:.2f}</span></div></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.current_page == "Analytics":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1><span class='gradient-text'>📊 Analytics</span></h1>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric"><div class="metric-label">Avg Pop</div><div class="metric-value">{engine.dataset["popularity"].mean():.0f}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric"><div class="metric-label">Avg Energy</div><div class="metric-value">{engine.dataset["energy"].mean():.2f}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric"><div class="metric-label">Avg Dance</div><div class="metric-value">{engine.dataset["danceability"].mean():.2f}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric"><div class="metric-label">Total</div><div class="metric-value">{len(engine.dataset)}</div></div>', unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        for idx, (a, p) in enumerate(engine.dataset.groupby('artist_name')['popularity'].mean().nlargest(15).items(), 1):
            st.markdown(f'<div class="card"><div style="display: flex; justify-content: space-between;"><strong>#{idx} {a}</strong><div style="color: #1ed760; font-weight: 900;">{p:.1f}</div></div></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.current_page == "Favorites":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown("<h1><span class='gradient-text'>❤️ Favorites</span></h1>", unsafe_allow_html=True)
        
        if st.session_state.user_stats['favorites']:
            for f in st.session_state.user_stats['favorites']:
                st.markdown(f'<div class="card"><strong style="color: #1DB954;">❤️ {f["song"]}</strong><div style="opacity: 0.7;">{f["artist"]}</div><div style="margin-top: 8px;"><span class="tag">{f["score"]}/100</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box" style="text-align: center;"><div style="font-size: 3rem;">💔</div><h3>No Favorites</h3></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        st.markdown(f"<h1><span class='gradient-text'>👤 {st.session_state.username}</span></h1>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric"><div class="metric-label">Predictions</div><div class="metric-value">{st.session_state.user_stats["total_predictions"]}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric"><div class="metric-label">Favorites</div><div class="metric-value">{len(st.session_state.user_stats["favorites"])}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric"><div class="metric-label">Status</div><div class="metric-value">Active</div></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# RUN
# ============================================================================

if st.session_state.authenticated:
    render_main()
else:
    render_login()
