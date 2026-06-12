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

# BASIC CSS
st.markdown("""
<style>
* { font-family: 'Poppins', sans-serif; }
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0F172A, #1A2F4A, #1A1F3A, #0F172A);
    background-size: 400% 400%;
    animation: bg 20s ease infinite;
}
@keyframes bg {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.card {
    background: rgba(30, 50, 85, 0.85);
    border: 1px solid rgba(29, 185, 84, 0.3);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    transition: all 0.3s ease;
}
.card:hover {
    background: rgba(40, 60, 100, 0.95);
    border-color: #1DB954;
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(29, 185, 84, 0.2);
}
.metric {
    background: rgba(29, 185, 84, 0.1);
    border: 1px solid rgba(29, 185, 84, 0.3);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    transition: all 0.3s ease;
}
.metric:hover {
    background: rgba(29, 185, 84, 0.2);
    border-color: #1DB954;
    transform: scale(1.05);
}
.metric-val {
    font-size: 2.5rem;
    font-weight: 900;
    color: #1ed760;
}
.gradient-text {
    background: linear-gradient(135deg, #1DB954, #1ed760);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stButton > button {
    background: linear-gradient(135deg, #1DB954, #1ed760) !important;
    color: black !important;
    font-weight: 700 !important;
    border-radius: 20px !important;
    padding: 12px 30px !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.4) !important;
}
.stTextInput > div > div > input {
    background: rgba(25, 40, 70, 0.8) !important;
    border: 1px solid rgba(29, 185, 84, 0.3) !important;
    color: white !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    background: rgba(25, 40, 70, 0.95) !important;
    border-color: #1DB954 !important;
    box-shadow: 0 0 15px rgba(29, 185, 84, 0.2) !important;
}
.tag {
    display: inline-block;
    background: rgba(29, 185, 84, 0.15);
    border: 1px solid rgba(29, 185, 84, 0.4);
    color: #1ed760;
    padding: 8px 12px;
    border-radius: 15px;
    margin: 5px;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
}
.tag:hover {
    background: rgba(29, 185, 84, 0.3);
    border-color: #1DB954;
    transform: translateY(-2px);
}
.login-box {
    background: rgba(30, 50, 85, 0.95);
    border: 2px solid rgba(29, 185, 84, 0.3);
    padding: 40px;
    border-radius: 20px;
    max-width: 450px;
    margin: 50px auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}
[data-testid="stSidebar"] {
    background: rgba(15, 25, 45, 0.95) !important;
    border-right: 1px solid rgba(29, 185, 84, 0.2) !important;
}
h1, h2, h3 { color: white; }
p, label { color: rgba(255, 255, 255, 0.8); }
</style>
""", unsafe_allow_html=True)

# DATA LOADING
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

# SESSION
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "Predictor"
if 'stats' not in st.session_state:
    st.session_state.stats = {'preds': 0, 'favs': [], 'last': None}

# FUNCTIONS
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

# LOGIN
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; margin: 50px 0;"><h1 style="font-size: 4rem;">♪</h1></div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; font-size: 2.5rem;"><span class="gradient-text">SPOTIFY PREDICTOR</span></h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; opacity: 0.6;">Predict Your Song\'s Popularity</p>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.subheader("Welcome")
            st.info("Demo: demo / demo123")
            u = st.text_input("Username", value="demo", key="u1")
            p = st.text_input("Password", type="password", value="demo123", key="p1")
            if st.button("Sign In", use_container_width=True, key="b1"):
                if u and p:
                    st.session_state.auth = True
                    st.session_state.user = u
                    st.success("Welcome!")
                    time.sleep(0.3)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.subheader("Create Account")
            u2 = st.text_input("Username", key="u2")
            e = st.text_input("Email", key="e")
            p2 = st.text_input("Password", type="password", key="p2")
            if st.button("Create", use_container_width=True, key="b2"):
                if u2 and e and p2 and len(p2) >= 6:
                    st.session_state.auth = True
                    st.session_state.user = u2
                    st.success("Account created!")
                    time.sleep(0.3)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# MAIN APP
def main_app():
    with st.sidebar:
        st.markdown('<h2 style="color: #1DB954; text-align: center;">♪ SPOTIFY</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; opacity: 0.6;color:white;">@{st.session_state.user}</p>', unsafe_allow_html=True)
        st.divider()
        st.session_state.page = st.radio("", ["Predictor", "Browse", "Analytics", "Favorites", "Profile"])
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()
    
    # PREDICTOR
    if st.session_state.page == "Predictor":
        st.markdown('<h1 style="text-align: center;"><span class="gradient-text">🎵 Predict Song</span></h1>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; margin: 30px 0;"><div style="display: flex; gap: 5px; justify-content: center; height: 80px; align-items: flex-end;"><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 40px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 60px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 30px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 70px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 50px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 65px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 45px;"></div><div style="width: 10px; background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 5px; height: 55px;"></div></div></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: song = st.text_input("Song Title", placeholder="e.g., Blinding Lights")
        with c2: artist = st.text_input("Artist", placeholder="e.g., The Weeknd")
        
        st.markdown('<hr style="border: 1px solid rgba(29, 185, 84, 0.3); margin: 20px 0;">', unsafe_allow_html=True)
        
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
            if st.button("PREDICT POPULARITY", use_container_width=True):
                if song and artist:
                    with st.spinner("Analyzing..."):
                        time.sleep(0.5)
                        features = [dance, energy, key_v, 0, 1, speech, acoustic, instr, live, valence, tempo, duration, 4]
                        score = predict(features)
                        st.session_state.stats['preds'] += 1
                        st.session_state.stats['last'] = {'song': song, 'artist': artist, 'score': score}
        
        if st.session_state.stats['last']:
            p = st.session_state.stats['last']
            st.markdown('<div class="card" style="border: 2px solid #1DB954; text-align: center; margin: 30px 0;"><h2 style="color: #1ed760;">✨ PREDICTION RESULT ✨</h2></div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric"><div style="font-size: 0.9rem;">Song</div><div style="font-size: 1.2rem; font-weight: 900; color: #1ed760;">{p["song"]}</div><div style="opacity: 0.7;">{p["artist"]}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric"><div style="font-size: 0.9rem;">Score</div><div class="metric-val">{int(p["score"])}</div><div style="font-size: 0.9rem;">/100</div></div>', unsafe_allow_html=True)
            with col3:
                s = p["score"]
                badge = "🔥 HIT" if s >= 80 else "⭐ GOOD" if s >= 60 else "📈 POTENTIAL"
                col_v = "#FF4500" if s >= 80 else "#1DB954" if s >= 60 else "#06B6D4"
                st.markdown(f'<div class="metric"><div style="font-size: 0.9rem;">Status</div><div style="font-size: 1.3rem; color: {col_v}; font-weight: 900;">{badge}</div></div>', unsafe_allow_html=True)
            
            st.markdown('<hr style="border: 1px solid rgba(29, 185, 84, 0.3); margin: 20px 0;">', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center;">📤 Share Your Result</h3>', unsafe_allow_html=True)
            
            msg = f"🎵 {p['song']} - Score: {int(p['score'])}/100! #SpotifyPredictor"
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                if st.button("Instagram", use_container_width=True, key="ig"):
                    st.markdown(f"[Share]({share_url('instagram', msg)})", unsafe_allow_html=True)
            with c2:
                if st.button("Twitter", use_container_width=True, key="tw"):
                    st.markdown(f"[Share]({share_url('twitter', msg)})", unsafe_allow_html=True)
            with c3:
                if st.button("WhatsApp", use_container_width=True, key="wa"):
                    st.markdown(f"[Share]({share_url('whatsapp', msg)})", unsafe_allow_html=True)
            with c4:
                if st.button("Telegram", use_container_width=True, key="tg"):
                    st.markdown(f"[Share]({share_url('telegram', msg)})", unsafe_allow_html=True)
            with c5:
                if st.button("Save ❤️", use_container_width=True, key="fav"):
                    st.session_state.stats['favs'].append({'song': p['song'], 'artist': p['artist'], 'score': int(p['score'])})
                    st.success("Added to favorites!")
    
    # BROWSE
    elif st.session_state.page == "Browse":
        st.markdown('<h1><span class="gradient-text">🎧 Browse Songs</span></h1>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: minp = st.slider("Min Popularity", 0, 100, 50)
        with c2: maxp = st.slider("Max Popularity", 0, 100, 100)
        with c3: srch = st.text_input("Search Artist")
        
        filt = df[(df['popularity'] >= minp) & (df['popularity'] <= maxp)]
        if srch:
            filt = filt[filt['artist_name'].str.contains(srch, case=False, na=False)]
        
        for idx, (_, r) in enumerate(filt.sort_values('popularity', ascending=False).head(20).iterrows(), 1):
            st.markdown(f'<div class="card"><strong style="color: #1DB954;">#{idx} {r["track_name"]}</strong><div style="opacity: 0.7;">{r["artist_name"]}</div><div style="margin-top: 10px;"><span class="tag">Dance: {r["danceability"]:.2f}</span><span class="tag">Energy: {r["energy"]:.2f}</span><span class="tag">Pop: {int(r["popularity"])}</span></div></div>', unsafe_allow_html=True)
    
    # ANALYTICS
    elif st.session_state.page == "Analytics":
        st.markdown('<h1><span class="gradient-text">📊 Analytics</span></h1>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric"><div>Avg Popularity</div><div class="metric-val">{df["popularity"].mean():.0f}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric"><div>Avg Energy</div><div class="metric-val">{df["energy"].mean():.2f}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric"><div>Avg Dance</div><div class="metric-val">{df["danceability"].mean():.2f}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric"><div>Total Songs</div><div class="metric-val">{len(df)}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<h3>🏆 Top Artists</h3>', unsafe_allow_html=True)
        for idx, (a, p) in enumerate(df.groupby('artist_name')['popularity'].mean().nlargest(15).items(), 1):
            st.markdown(f'<div class="card"><strong>#{idx} {a}</strong> - <span style="color: #1ed760; font-weight: 900;">{p:.1f}</span></div>', unsafe_allow_html=True)
    
    # FAVORITES
    elif st.session_state.page == "Favorites":
        st.markdown('<h1><span class="gradient-text">❤️ Favorites</span></h1>', unsafe_allow_html=True)
        if st.session_state.stats['favs']:
            for f in st.session_state.stats['favs']:
                st.markdown(f'<div class="card"><strong style="color: #1DB954;">❤️ {f["song"]}</strong><div style="opacity: 0.7;">{f["artist"]}</div><div style="margin-top: 8px;"><span class="tag">Score: {f["score"]}/100</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card" style="text-align: center;"><div style="font-size: 2rem;">💔</div><p>No favorites yet!</p></div>', unsafe_allow_html=True)
    
    # PROFILE
    else:
        st.markdown(f'<h1><span class="gradient-text">👤 {st.session_state.user}</span></h1>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric"><div>Predictions</div><div class="metric-val">{st.session_state.stats["preds"]}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric"><div>Favorites</div><div class="metric-val">{len(st.session_state.stats["favs"])}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric"><div>Status</div><div class="metric-val">Active</div></div>', unsafe_allow_html=True)

# RUN
if st.session_state.auth:
    main_app()
else:
    login_page()
