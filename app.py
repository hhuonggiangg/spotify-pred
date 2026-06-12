import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import time
import urllib.parse

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Spotify Predictor", page_icon="🎵", layout="wide", initial_sidebar_state="expanded")

# ============================================================================
# CSS - ANIMATED BG + CURSORS + TRANSITIONS + INTERACTIVE (Streamlit-safe)
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* ---------- CUSTOM CURSORS (safe encoded SVG) ---------- */
html, body, [data-testid="stAppViewContainer"], .main {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='12' cy='12' r='3' fill='%231ed760'/%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='%231DB954' stroke-width='1.5'/%3E%3C/svg%3E") 12 12, auto;
}
button, a, [role="button"], [role="radio"], label, .stButton, .stTabs [data-baseweb="tab"] {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='26' height='26'%3E%3Ccircle cx='13' cy='13' r='10' fill='none' stroke='%231ed760' stroke-width='2'/%3E%3Cpath d='M13 8 L13 18 M8 13 L18 13' stroke='%231ed760' stroke-width='2'/%3E%3C/svg%3E") 13 13, pointer !important;
}
input, textarea { cursor: text !important; }

/* ---------- ANIMATED GRADIENT BACKGROUND ---------- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0F172A, #16324F, #1A1F3A, #132238, #0F172A);
    background-size: 500% 500%;
    animation: gradientBG 22s ease infinite;
}
[data-testid="stHeader"] { background: transparent; }
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    25% { background-position: 50% 100%; }
    50% { background-position: 100% 50%; }
    75% { background-position: 50% 0%; }
    100% { background-position: 0% 50%; }
}

/* Floating glow orbs */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle at 18% 40%, rgba(29,185,84,0.10) 0%, transparent 45%),
        radial-gradient(circle at 82% 75%, rgba(30,215,96,0.08) 0%, transparent 45%);
    animation: orbFloat 28s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes orbFloat {
    0%, 100% { transform: translateY(0px); opacity: 1; }
    50% { transform: translateY(-25px); opacity: 0.8; }
}

/* ---------- PAGE TRANSITION ---------- */
@keyframes pageIn {
    from { opacity: 0; transform: translateY(28px) scale(0.985); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.block-container { animation: pageIn 0.65s cubic-bezier(0.34, 1.56, 0.64, 1); }
.page-anim { animation: pageIn 0.65s cubic-bezier(0.34, 1.56, 0.64, 1); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
h1, h2, h3 { color: white; animation: fadeIn 0.6s ease-out; }
p, label, span { color: rgba(255,255,255,0.85); }

/* ---------- CARDS ---------- */
.card {
    background: linear-gradient(135deg, rgba(30,50,85,0.85) 0%, rgba(15,30,55,0.85) 100%);
    border: 1px solid rgba(29,185,84,0.3);
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 8px 28px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    animation: shimmer 3.5s infinite;
}
@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}
.card:hover {
    background: linear-gradient(135deg, rgba(40,60,100,0.95) 0%, rgba(25,45,75,0.95) 100%);
    border-color: #1DB954;
    transform: translateY(-7px) scale(1.015);
    box-shadow: 0 16px 45px rgba(29,185,84,0.28);
}

/* ---------- METRICS ---------- */
.metric {
    background: linear-gradient(135deg, rgba(29,185,84,0.14) 0%, rgba(20,35,60,0.14) 100%);
    border: 1px solid rgba(29,185,84,0.35);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.metric:hover {
    border-color: #1DB954;
    background: linear-gradient(135deg, rgba(29,185,84,0.26) 0%, rgba(29,185,84,0.1) 100%);
    transform: scale(1.1) translateY(-5px);
    box-shadow: 0 12px 32px rgba(29,185,84,0.25);
}
.metric-val {
    font-size: 2.6rem;
    font-weight: 900;
    color: #1ed760;
    margin: 8px 0;
    letter-spacing: -2px;
    transition: transform 0.3s ease;
}
.metric:hover .metric-val { transform: scale(1.12); }
.metric-label {
    color: rgba(255,255,255,0.65);
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ---------- TAGS ---------- */
.tag {
    display: inline-block;
    background: linear-gradient(135deg, rgba(29,185,84,0.2) 0%, rgba(29,185,84,0.07) 100%);
    border: 1px solid rgba(29,185,84,0.42);
    color: #1ed760;
    padding: 8px 14px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.84rem;
    font-weight: 600;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.tag:hover {
    background: linear-gradient(135deg, rgba(29,185,84,0.38) 0%, rgba(29,185,84,0.18) 100%);
    border-color: #1DB954;
    transform: translateY(-3px) scale(1.07);
    box-shadow: 0 6px 16px rgba(29,185,84,0.25);
}

/* ---------- GRADIENT TEXT ---------- */
.gradient-text {
    background: linear-gradient(135deg, #1DB954, #1ed760);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
}
@keyframes glowPulse {
    0%, 100% { filter: drop-shadow(0 0 4px rgba(29,185,84,0.4)); }
    50% { filter: drop-shadow(0 0 14px rgba(29,185,84,0.8)); }
}
.logo-glow { animation: glowPulse 2.5s ease-in-out infinite; }

/* ---------- VISUALIZER ---------- */
.visualizer {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 6px;
    height: 90px;
    margin: 28px 0;
}
.bar {
    width: 12px;
    background: linear-gradient(180deg, #1DB954, #1ed760);
    border-radius: 6px;
    animation: bounceBar 0.8s ease-in-out infinite;
    box-shadow: 0 0 12px rgba(29,185,84,0.6);
}
@keyframes bounceBar {
    0%, 100% { height: 14px; opacity: 0.65; }
    50% { height: 62px; opacity: 1; }
}
.bar:nth-child(1) { animation-delay: 0s; }
.bar:nth-child(2) { animation-delay: 0.1s; }
.bar:nth-child(3) { animation-delay: 0.2s; }
.bar:nth-child(4) { animation-delay: 0.3s; }
.bar:nth-child(5) { animation-delay: 0.4s; }
.bar:nth-child(6) { animation-delay: 0.5s; }
.bar:nth-child(7) { animation-delay: 0.4s; }
.bar:nth-child(8) { animation-delay: 0.3s; }

/* ---------- BUTTONS ---------- */
.stButton > button {
    background: linear-gradient(135deg, #1DB954, #1ed760) !important;
    color: black !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 22px !important;
    padding: 12px 28px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: 0 5px 18px rgba(29,185,84,0.32) !important;
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.05) !important;
    box-shadow: 0 14px 36px rgba(29,185,84,0.5) !important;
}
.stButton > button:active { transform: translateY(-1px) !important; }

/* ---------- INPUTS ---------- */
.stTextInput > div > div > input {
    background: rgba(25,40,70,0.8) !important;
    border: 1.5px solid rgba(29,185,84,0.3) !important;
    color: white !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1DB954 !important;
    box-shadow: 0 0 18px rgba(29,185,84,0.25) !important;
}

/* ---------- ARTIST PANEL ---------- */
.artist-panel {
    background: linear-gradient(135deg, rgba(30,50,85,0.97) 0%, rgba(15,30,55,0.97) 100%);
    border: 2px solid rgba(29,185,84,0.45);
    border-radius: 20px;
    padding: 28px;
    margin: 14px 0;
    box-shadow: 0 18px 50px rgba(29,185,84,0.25);
    animation: pageIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.artist-avatar {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1DB954, #1ed760);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    margin: 0 auto 14px auto;
    box-shadow: 0 0 30px rgba(29,185,84,0.5);
    animation: glowPulse 2.5s ease-in-out infinite;
}
.link-btn {
    display: inline-block;
    padding: 11px 22px;
    border-radius: 14px;
    font-weight: 700;
    text-decoration: none !important;
    margin: 6px;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.link-btn:hover {
    transform: translateY(-4px) scale(1.06);
    box-shadow: 0 10px 26px rgba(0,0,0,0.4);
}
.spotify-btn { background: linear-gradient(135deg, #1DB954, #1ed760); color: black !important; }
.youtube-btn { background: linear-gradient(135deg, #FF0000, #FF4500); color: white !important; }

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,25,45,0.97), rgba(10,20,40,0.97)) !important;
    border-right: 1.5px solid rgba(29,185,84,0.22) !important;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar { width: 11px; }
::-webkit-scrollbar-track { background: rgba(20,30,50,0.4); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #1DB954, #1ed760); border-radius: 6px; }

/* Expander styling */
[data-testid="stExpander"] {
    background: rgba(25,40,70,0.5);
    border: 1px solid rgba(29,185,84,0.25);
    border-radius: 14px;
    transition: all 0.3s ease;
}
[data-testid="stExpander"]:hover { border-color: rgba(29,185,84,0.55); }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ARTIST DATABASE (info + links + image emoji)
# ============================================================================

ARTISTS_DB = {
    "The Weeknd": {
        "avatar": "🌙",
        "bio": "Canadian singer, songwriter and producer famous for dark, cinematic R&B-pop.",
        "spotify": "https://open.spotify.com/artist/1Xyo4u8uTS0wX3xdigHP7G",
        "youtube": "https://www.youtube.com/@TheWeeknd",
        "genres": ["Pop", "R&B", "Synthwave"],
        "hits": ["Blinding Lights", "Starboy", "The Hills"],
    },
    "Ed Sheeran": {
        "avatar": "🎸",
        "bio": "English singer-songwriter blending pop, folk and acoustic sounds.",
        "spotify": "https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V",
        "youtube": "https://www.youtube.com/@EdSheeran",
        "genres": ["Pop", "Folk", "Acoustic"],
        "hits": ["Shape of You", "Perfect", "Photograph"],
    },
    "Dua Lipa": {
        "avatar": "💫",
        "bio": "British-Albanian pop star known for disco-infused dance pop.",
        "spotify": "https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we",
        "youtube": "https://www.youtube.com/@DuaLipa",
        "genres": ["Pop", "Disco", "Dance"],
        "hits": ["Levitating", "Don't Start Now", "New Rules"],
    },
    "Ariana Grande": {
        "avatar": "🎀",
        "bio": "American pop & R&B vocalist with a signature whistle register.",
        "spotify": "https://open.spotify.com/artist/66CXWjxzNUsdJxJ2JdwL6V",
        "youtube": "https://www.youtube.com/@ArianaGrande",
        "genres": ["Pop", "R&B"],
        "hits": ["7 rings", "thank u, next", "positions"],
    },
    "Taylor Swift": {
        "avatar": "✨",
        "bio": "American singer-songwriter spanning country, pop and indie-folk eras.",
        "spotify": "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02",
        "youtube": "https://www.youtube.com/@TaylorSwift",
        "genres": ["Pop", "Country", "Indie Folk"],
        "hits": ["Anti-Hero", "Blank Space", "Cruel Summer"],
    },
    "Billie Eilish": {
        "avatar": "🖤",
        "bio": "American artist known for whispery vocals and genre-bending pop.",
        "spotify": "https://open.spotify.com/artist/6qqNVTkY8uBg9cP3Jd7DAH",
        "youtube": "https://www.youtube.com/@BillieEilish",
        "genres": ["Alt Pop", "Electropop"],
        "hits": ["bad guy", "Happier Than Ever", "BIRDS OF A FEATHER"],
    },
    "Drake": {
        "avatar": "🦉",
        "bio": "Canadian rapper and singer, one of the best-selling artists ever.",
        "spotify": "https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4",
        "youtube": "https://www.youtube.com/@Drake",
        "genres": ["Hip-Hop", "R&B"],
        "hits": ["God's Plan", "Hotline Bling", "One Dance"],
    },
    "BTS": {
        "avatar": "💜",
        "bio": "Global K-pop phenomenon breaking records worldwide.",
        "spotify": "https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX",
        "youtube": "https://www.youtube.com/@BTS",
        "genres": ["K-Pop", "Pop", "Hip-Hop"],
        "hits": ["Dynamite", "Butter", "Spring Day"],
    },
}

DEFAULT_ARTIST = {
    "avatar": "🎤",
    "bio": "Artist information not available yet — explore their music on Spotify and YouTube!",
    "spotify": None,
    "youtube": None,
    "genres": [],
    "hits": [],
}

def get_artist_info(name):
    if name in ARTISTS_DB:
        return ARTISTS_DB[name]
    info = dict(DEFAULT_ARTIST)
    q = urllib.parse.quote(str(name))
    info["spotify"] = f"https://open.spotify.com/search/{q}"
    info["youtube"] = f"https://www.youtube.com/results?search_query={q}"
    return info

# ============================================================================
# DATA + MODEL
# ============================================================================

@st.cache_data
def load_data():
    try:
        return pd.read_csv('data/spotify_songs_expanded.csv')
    except Exception:
        return pd.read_csv('spotify_songs_expanded.csv')

@st.cache_resource
def load_model():
    try:
        with open('model_lr.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception:
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
if 'stats' not in st.session_state:
    st.session_state.stats = {'preds': 0, 'favs': [], 'last': None}
if 'selected_artist' not in st.session_state:
    st.session_state.selected_artist = None

# ============================================================================
# HELPERS
# ============================================================================

def predict(features):
    if model is not None:
        try:
            return float(max(0, min(100, model.predict(np.array([features]).reshape(1, -1))[0])))
        except Exception:
            pass
    d, e, v = features[0], features[1], features[9]
    return float(max(0, min(100, d * 30 + e * 25 + v * 20 + 25)))

def share_url(platform, msg):
    enc = urllib.parse.quote(msg)
    urls = {
        'twitter': f"https://twitter.com/intent/tweet?text={enc}",
        'whatsapp': f"https://wa.me/?text={enc}",
        'telegram': f"https://t.me/share/url?url=https://spotify.com&text={enc}",
        'facebook': f"https://www.facebook.com/sharer/sharer.php?u=https://spotify.com&quote={enc}",
    }
    return urls.get(platform, '#')

def visualizer():
    bars = ''.join(['<div class="bar"></div>' for _ in range(8)])
    st.markdown(f'<div class="visualizer">{bars}</div>', unsafe_allow_html=True)

def render_artist_panel(name):
    info = get_artist_info(name)
    genres_html = ''.join([f'<span class="tag">{g}</span>' for g in info["genres"]]) or '<span class="tag">Explore</span>'
    hits_html = ''.join([f'<span class="tag">♪ {h}</span>' for h in info["hits"]]) or '<span class="tag">Discover their hits</span>'
    
    links = ""
    if info["spotify"]:
        links += f'<a class="link-btn spotify-btn" href="{info["spotify"]}" target="_blank">🎵 Listen on Spotify</a>'
    if info["youtube"]:
        links += f'<a class="link-btn youtube-btn" href="{info["youtube"]}" target="_blank">📺 Watch MV on YouTube</a>'
    
    st.markdown(f"""
    <div class="artist-panel">
        <div class="artist-avatar">{info["avatar"]}</div>
        <h3 style="text-align:center; color:#1ed760; margin: 6px 0;">{name}</h3>
        <p style="text-align:center; opacity:0.85; margin: 10px 0;">{info["bio"]}</p>
        <div style="text-align:center; margin: 14px 0;">
            <div style="color:#1DB954; font-weight:700; margin-bottom:6px;">Genres</div>
            {genres_html}
        </div>
        <div style="text-align:center; margin: 14px 0;">
            <div style="color:#1DB954; font-weight:700; margin-bottom:6px;">Popular Hits</div>
            {hits_html}
        </div>
        <div style="text-align:center; margin-top: 18px;">
            {links}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="page-anim" style="text-align:center; margin-top:40px;"><h1 class="logo-glow" style="font-size:4.2rem; margin:0;"><span class="gradient-text">♪</span></h1></div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center; font-size:2.6rem;"><span class="gradient-text">SPOTIFY PREDICTOR</span></h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; opacity:0.65;">Predict • Discover • Share</p>', unsafe_allow_html=True)
        
        visualizer()
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.info("Demo account: demo / demo123")
            u = st.text_input("Username", value="demo", key="u1")
            p = st.text_input("Password", type="password", value="demo123", key="p1")
            if st.button("SIGN IN", use_container_width=True, key="b1"):
                if u and p:
                    st.session_state.auth = True
                    st.session_state.user = u
                    st.balloons()
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Please fill in all fields")
        
        with tab2:
            u2 = st.text_input("Username", key="u2")
            e2 = st.text_input("Email", key="e2")
            p2 = st.text_input("Password", type="password", key="p2")
            if st.button("CREATE ACCOUNT", use_container_width=True, key="b2"):
                if u2 and e2 and p2 and len(p2) >= 6:
                    st.session_state.auth = True
                    st.session_state.user = u2
                    st.balloons()
                    time.sleep(0.4)
                    st.rerun()
                elif p2 and len(p2) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    st.error("Please fill in all fields")

# ============================================================================
# PAGES
# ============================================================================

def page_predictor():
    st.markdown('<h1 style="text-align:center;"><span class="gradient-text">🎵 Predict Your Song</span></h1>', unsafe_allow_html=True)
    visualizer()
    
    c1, c2 = st.columns(2)
    with c1:
        song = st.text_input("Song Title", placeholder="e.g., Blinding Lights")
    with c2:
        artist = st.text_input("Artist Name", placeholder="e.g., The Weeknd")
    
    st.markdown('<h3>📊 Audio Features</h3>', unsafe_allow_html=True)
    
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
    
    bc1, bc2, bc3 = st.columns([1, 2, 1])
    with bc2:
        if st.button("🚀 PREDICT POPULARITY", use_container_width=True):
            if song and artist:
                with st.spinner("Analyzing audio features..."):
                    time.sleep(0.6)
                    feats = [dance, energy, key_v, 0, 1, speech, acoustic, instr, live, valence, tempo, duration, 4]
                    score = predict(feats)
                    st.session_state.stats['preds'] += 1
                    st.session_state.stats['last'] = {'song': song, 'artist': artist, 'score': score}
            else:
                st.error("Please enter song title and artist name")
    
    last = st.session_state.stats['last']
    if last:
        st.markdown('<div class="card" style="border:2px solid #1DB954; text-align:center;"><h2 style="color:#1ed760; margin:0;">✨ PREDICTION RESULT ✨</h2></div>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric"><div class="metric-label">Song</div><div style="font-size:1.2rem; font-weight:900; color:#1ed760; margin:8px 0;">{last["song"]}</div><div style="opacity:0.7;">{last["artist"]}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric"><div class="metric-label">Score</div><div class="metric-val">{int(last["score"])}</div><div class="metric-label">/100</div></div>', unsafe_allow_html=True)
        with m3:
            s = last["score"]
            badge = "🔥 HIT" if s >= 80 else "⭐ STRONG" if s >= 60 else "📈 POTENTIAL"
            col_v = "#FF4500" if s >= 80 else "#1DB954" if s >= 60 else "#06B6D4"
            st.markdown(f'<div class="metric"><div class="metric-label">Status</div><div style="font-size:1.4rem; color:{col_v}; font-weight:900; margin:10px 0;">{badge}</div></div>', unsafe_allow_html=True)
        
        # Insights
        insights = []
        if dance > 0.7: insights.append(("💃 Danceable", "Perfect for the dance floor"))
        if energy > 0.7: insights.append(("⚡ High Energy", "Great workout track"))
        if valence > 0.6: insights.append(("😊 Uplifting", "Positive mood booster"))
        if acoustic > 0.5: insights.append(("🎸 Acoustic", "Organic, natural sound"))
        if insights:
            st.markdown('<h3>💡 Track Insights</h3>', unsafe_allow_html=True)
            cols = st.columns(len(insights))
            for col, (t, d) in zip(cols, insights):
                with col:
                    st.markdown(f'<div class="card" style="text-align:center;"><div style="font-weight:800; color:#1DB954;">{t}</div><div style="font-size:0.85rem; opacity:0.75; margin-top:6px;">{d}</div></div>', unsafe_allow_html=True)
        
        # Artist panel for predicted artist
        with st.expander(f"🎤 About {last['artist']}"):
            render_artist_panel(last['artist'])
        
        # Social share
        st.markdown('<h3 style="text-align:center;">📤 Share Your Result</h3>', unsafe_allow_html=True)
        msg = f"🎵 {last['song']} by {last['artist']} — predicted popularity {int(last['score'])}/100 on Spotify Predictor!"
        
        s1, s2, s3, s4, s5 = st.columns(5)
        with s1:
            st.link_button("𝕏 Twitter", share_url('twitter', msg), use_container_width=True)
        with s2:
            st.link_button("💬 WhatsApp", share_url('whatsapp', msg), use_container_width=True)
        with s3:
            st.link_button("✈️ Telegram", share_url('telegram', msg), use_container_width=True)
        with s4:
            st.link_button("📘 Facebook", share_url('facebook', msg), use_container_width=True)
        with s5:
            if st.button("❤️ Save", use_container_width=True, key="fav_btn"):
                st.session_state.stats['favs'].append({'song': last['song'], 'artist': last['artist'], 'score': int(last['score'])})
                st.success("Saved to favorites!")

def page_browse():
    st.markdown('<h1><span class="gradient-text">🎧 Browse & Discover</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="opacity:0.7;">Click on any song to see artist info, photos and links to Spotify / YouTube MV</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: minp = st.slider("Min Popularity", 0, 100, 50)
    with c2: maxp = st.slider("Max Popularity", 0, 100, 100)
    with c3: srch = st.text_input("Search Artist", placeholder="Type artist name...")
    
    filt = df[(df['popularity'] >= minp) & (df['popularity'] <= maxp)]
    if srch:
        filt = filt[filt['artist_name'].str.contains(srch, case=False, na=False)]
    filt = filt.sort_values('popularity', ascending=False).head(20)
    
    st.markdown(f"**Found {len(filt)} songs**")
    
    for idx, (_, r) in enumerate(filt.iterrows(), 1):
        artist_name = str(r['artist_name'])
        info = get_artist_info(artist_name)
        
        st.markdown(f'''
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:14px;">
                    <div style="font-size:2rem;">{info["avatar"]}</div>
                    <div>
                        <strong style="color:#1DB954;">#{idx} {r["track_name"]}</strong>
                        <div style="opacity:0.7; font-size:0.92rem;">{artist_name}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="color:#1ed760; font-weight:900; font-size:1.3rem;">{int(r["popularity"])}</div>
                    <div style="font-size:0.75rem; opacity:0.5;">popularity</div>
                </div>
            </div>
            <div style="margin-top:10px;">
                <span class="tag">💃 {r["danceability"]:.2f}</span>
                <span class="tag">⚡ {r["energy"]:.2f}</span>
                <span class="tag">😊 {r["valence"]:.2f}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        with st.expander(f"🎤 View {artist_name} — info, photos, Spotify & MV"):
            render_artist_panel(artist_name)

def page_analytics():
    st.markdown('<h1><span class="gradient-text">📊 Analytics Dashboard</span></h1>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric"><div class="metric-label">Avg Popularity</div><div class="metric-val">{df["popularity"].mean():.0f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric"><div class="metric-label">Avg Energy</div><div class="metric-val">{df["energy"].mean():.2f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric"><div class="metric-label">Avg Dance</div><div class="metric-val">{df["danceability"].mean():.2f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric"><div class="metric-label">Total Songs</div><div class="metric-val">{len(df)}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<h3 style="margin-top:25px;">🏆 Top 10 Artists</h3>', unsafe_allow_html=True)
    top = df.groupby('artist_name')['popularity'].mean().nlargest(10)
    for idx, (a, p) in enumerate(top.items(), 1):
        info = get_artist_info(str(a))
        st.markdown(f'<div class="card"><div style="display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; gap:12px;"><span style="font-size:1.5rem;">{info["avatar"]}</span><strong>#{idx} {a}</strong></div><span style="color:#1ed760; font-weight:900; font-size:1.2rem;">{p:.1f}</span></div></div>', unsafe_allow_html=True)
        with st.expander(f"View {a}"):
            render_artist_panel(str(a))

def page_favorites():
    st.markdown('<h1><span class="gradient-text">❤️ Your Favorites</span></h1>', unsafe_allow_html=True)
    
    favs = st.session_state.stats['favs']
    if favs:
        for i, f in enumerate(favs, 1):
            st.markdown(f'<div class="card"><strong style="color:#1DB954;">#{i} ❤️ {f["song"]}</strong><div style="opacity:0.7; margin:4px 0;">{f["artist"]}</div><span class="tag">Score: {f["score"]}/100</span></div>', unsafe_allow_html=True)
            with st.expander(f"🎤 About {f['artist']}"):
                render_artist_panel(f['artist'])
    else:
        st.markdown('<div class="card" style="text-align:center; padding:40px;"><div style="font-size:2.5rem;">💔</div><h3>No Favorites Yet</h3><p style="opacity:0.6;">Predict songs and save them here!</p></div>', unsafe_allow_html=True)

def page_profile():
    st.markdown(f'<h1><span class="gradient-text">👤 {st.session_state.user}</span></h1>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric"><div class="metric-label">Predictions</div><div class="metric-val">{st.session_state.stats["preds"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric"><div class="metric-label">Favorites</div><div class="metric-val">{len(st.session_state.stats["favs"])}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric"><div class="metric-label">Status</div><div class="metric-val">✨</div></div>', unsafe_allow_html=True)
    
    visualizer()

# ============================================================================
# MAIN
# ============================================================================

def main_app():
    with st.sidebar:
        st.markdown('<h2 class="logo-glow" style="color:#1DB954; text-align:center; margin:0; font-size:2.2rem;">♪</h2>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center; letter-spacing:2px;">SPOTIFY</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; opacity:0.6;">@{st.session_state.user}</p>', unsafe_allow_html=True)
        st.divider()
        page = st.radio("Navigation", ["Predictor", "Browse", "Analytics", "Favorites", "Profile"], label_visibility="collapsed")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.session_state.user = None
            st.rerun()
    
    if page == "Predictor":
        page_predictor()
    elif page == "Browse":
        page_browse()
    elif page == "Analytics":
        page_analytics()
    elif page == "Favorites":
        page_favorites()
    else:
        page_profile()

if st.session_state.auth:
    main_app()
else:
    login_page()
