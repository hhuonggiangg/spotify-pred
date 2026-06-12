# 🎵 SPOTIFY PREDICTOR - SPOTIFY STYLED VERSION
# Enhanced UI, demo login, gradient backgrounds, artist images

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import time
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
# ADVANCED CSS - SPOTIFY STYLE
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap');

:root {
    --spotify-green: #1DB954;
    --spotify-light-green: #1ed760;
    --dark-bg: #0F172A;
    --card-bg: #1A1F3A;
    --text-primary: #FFFFFF;
    --text-secondary: rgba(255, 255, 255, 0.7);
}

* {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

html, body, .main {
    background: linear-gradient(135deg, #0F172A 0%, #1A1F3A 40%, #0F172A 100%);
    color: var(--text-primary);
}

/* Animations */
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

.page-container {
    animation: fadeInUp 0.6s ease-out;
    padding: 20px;
}

/* Spotify Card */
.spotify-card {
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.9) 0%, rgba(20, 30, 50, 0.9) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(29, 185, 84, 0.3);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 8px 32px rgba(29, 185, 84, 0.1);
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

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(29, 185, 84, 0.05) 100%);
    border: 1px solid rgba(29, 185, 84, 0.4);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: var(--spotify-green);
    background: linear-gradient(135deg, rgba(29, 185, 84, 0.25) 0%, rgba(29, 185, 84, 0.1) 100%);
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.15);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--spotify-light-green);
    margin: 10px 0;
    letter-spacing: -1px;
}

.metric-label {
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Tags */
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
}

.tag:hover {
    background: rgba(29, 185, 84, 0.3);
    border-color: var(--spotify-green);
    box-shadow: 0 4px 12px rgba(29, 185, 84, 0.2);
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(29, 185, 84, 0.4), transparent);
    margin: 24px 0;
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

/* Login Form */
.login-container {
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.95) 0%, rgba(20, 30, 50, 0.95) 100%);
    border: 1px solid rgba(29, 185, 84, 0.3);
    padding: 40px;
    border-radius: 20px;
    max-width: 500px;
    margin: 50px auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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

/* Song Card */
.song-card {
    background: linear-gradient(135deg, rgba(30, 40, 60, 0.8) 0%, rgba(20, 30, 50, 0.8) 100%);
    border: 1px solid rgba(29, 185, 84, 0.2);
    border-radius: 12px;
    padding: 16px;
    margin: 10px 0;
    transition: all 0.3s ease;
}

.song-card:hover {
    border-color: var(--spotify-green);
    background: linear-gradient(135deg, rgba(40, 50, 70, 0.9) 0%, rgba(30, 40, 60, 0.9) 100%);
    box-shadow: 0 8px 20px rgba(29, 185, 84, 0.15);
}

.artist-image {
    width: 100%;
    height: 150px;
    background: linear-gradient(135deg, #1DB954, #1ed760);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    margin: 10px 0;
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

df = load_data()
model = load_model()

# ============================================================================
# SESSION STATE
# ============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "🎵 Predictor"

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
            danceability = features[0]
            energy = features[1]
            valence = features[10]
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

# ============================================================================
# AUTHENTICATION
# ============================================================================

def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class='page-container' style='text-align: center;'>
            <h1 style='font-size: 4rem; margin-bottom: 10px;'>
                <span class='gradient-text-large'>🎵</span>
            </h1>
            <h2 style='font-size: 2.5rem; margin: 20px 0; font-weight: 800;'>
                SPOTIFY PREDICTOR
            </h2>
            <p style='color: rgba(255,255,255,0.6); font-size: 1.2rem; margin-bottom: 40px;'>
                Predict Your Song's Spotify Popularity
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔓 Sign In", "📝 Sign Up"])
        
        with tab1:
            st.markdown("""
            <div class='login-container'>
            """, unsafe_allow_html=True)
            
            st.markdown("### Demo Login")
            st.info("💡 **Demo Credentials:**\n- Username: `demo`\n- Password: `demo123`")
            
            username = st.text_input("Username", placeholder="Enter username", value="demo", key="signin_user")
            password = st.text_input("Password", type="password", placeholder="Enter password", value="demo123", key="signin_pass")
            
            if st.button("Sign In", use_container_width=True, key="signin_btn"):
                if username and password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"✅ Welcome, {username}!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Please fill in all fields")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div class='login-container'>
            """, unsafe_allow_html=True)
            
            st.markdown("### Create Account")
            new_username = st.text_input("Username", placeholder="Create username", key="signup_user")
            new_email = st.text_input("Email", placeholder="your@email.com", key="signup_email")
            new_password = st.text_input("Password", type="password", placeholder="Create password", key="signup_pass")
            
            if st.button("Create Account", use_container_width=True, key="signup_btn"):
                if new_username and new_email and new_password:
                    st.session_state.authenticated = True
                    st.session_state.username = new_username
                    st.success(f"✅ Account created! Welcome, {new_username}!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Please fill in all fields")
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def show_app():
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: #1DB954; font-size: 2rem;'>🎵</h2>
            <h3 style='font-weight: 800;'>SPOTIFY</h3>
            <p style='color: rgba(255,255,255,0.6); font-size: 0.9rem;'>
                User: <strong>{st.session_state.username}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        pages = ["🎵 Predictor", "🎧 Browse", "📊 Analytics", "❤️ Favorites", "👤 Profile"]
        selected_page = st.radio("Navigation", pages, key="nav_radio")
        st.session_state.current_page = selected_page
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # ====== PAGE: PREDICTOR ======
    if st.session_state.current_page == "🎵 Predictor":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        
        st.markdown("""
        <h1 style='font-size: 3rem; margin-bottom: 10px;'>
            <span class='gradient-text'>🎵 Predict Your Song</span>
        </h1>
        <p style='color: rgba(255,255,255,0.6); margin-bottom: 30px; font-size: 1.1rem;'>
            Enter song details to predict its Spotify popularity
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown(create_music_visualizer(), unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Song Input
        col1, col2 = st.columns(2)
        with col1:
            song_title = st.text_input("🎵 Song Title", placeholder="e.g., Blinding Lights", key="song_title")
        with col2:
            artist_name = st.text_input("👤 Artist Name", placeholder="e.g., The Weeknd", key="artist_name")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin: 20px 0;'>📊 Song Features</h3>", unsafe_allow_html=True)
        
        # Feature Sliders
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            danceability = st.slider("💃 Danceability", 0.0, 1.0, 0.65, 0.01, key="dance")
        with col2:
            energy = st.slider("⚡ Energy", 0.0, 1.0, 0.65, 0.01, key="energy")
        with col3:
            valence = st.slider("😊 Valence", 0.0, 1.0, 0.50, 0.01, key="valence")
        with col4:
            acousticness = st.slider("🎸 Acousticness", 0.0, 1.0, 0.15, 0.01, key="acoustic")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            speechiness = st.slider("🎤 Speechiness", 0.0, 1.0, 0.05, 0.01, key="speech")
        with col2:
            instrumentalness = st.slider("🎼 Instrumentalness", 0.0, 1.0, 0.0, 0.01, key="instr")
        with col3:
            liveness = st.slider("🎙️ Liveness", 0.0, 1.0, 0.10, 0.01, key="live")
        with col4:
            key = st.slider("🎹 Key", 0, 11, 5, key="key_slider")
        
        col1, col2 = st.columns(2)
        with col1:
            tempo = st.slider("🎶 Tempo (BPM)", 50, 200, 120, key="tempo")
        with col2:
            duration_ms = st.slider("⏱️ Duration (ms)", 60000, 600000, 180000, 1000, key="duration")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        # Predict Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 PREDICT POPULARITY", use_container_width=True, key="predict_btn"):
                if not song_title or not artist_name:
                    st.error("❌ Please enter song title and artist name!")
                else:
                    with st.spinner("🎵 Analyzing your track..."):
                        time.sleep(0.5)
                        
                        features = [
                            danceability, energy, key, 0, 1, speechiness,
                            acousticness, instrumentalness, liveness, valence,
                            tempo, duration_ms, 4
                        ]
                        
                        prediction = predict_popularity(features)
                        
                        st.session_state.user_data['predictions_made'] += 1
                        st.session_state.user_data['last_prediction'] = {
                            'song': song_title,
                            'artist': artist_name,
                            'score': prediction
                        }
        
        # Display Result
        if st.session_state.user_data['last_prediction']:
            last_pred = st.session_state.user_data['last_prediction']
            pred = last_pred['score']
            
            st.markdown("""
            <div class='spotify-card' style='background: linear-gradient(135deg, rgba(29, 185, 84, 0.2) 0%, rgba(40, 40, 40, 0.9) 100%); border: 2px solid #1DB954; margin: 30px 0;'>
                <h2 style='text-align: center; color: var(--spotify-light-green);'>✨ PREDICTION RESULT ✨</h2>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem;'>Song</div>
                    <div style='font-size: 1.3rem; font-weight: 700; color: white; margin: 10px 0;'>{last_pred['song']}</div>
                    <div style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>{last_pred['artist']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem;'>Predicted Score</div>
                    <div class='metric-value'>{int(pred)}</div>
                    <div style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>out of 100</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if pred >= 80:
                    status = "🔥 Hit"
                    color = "#1DB954"
                elif pred >= 60:
                    status = "⭐ Good"
                    color = "#1DB954"
                else:
                    status = "📈 Potential"
                    color = "#06B6D4"
                
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.9rem;'>Status</div>
                    <div style='font-size: 1.3rem; font-weight: 700; color: {color}; margin: 10px 0;'>{status}</div>
                    <div style='font-size: 0.85rem;'>Based on features</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Insights
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin: 20px 0;'>💡 Key Factors</h3>", unsafe_allow_html=True)
            
            insights = []
            if danceability > 0.7:
                insights.append(("💃", "High Danceability", "Perfect for dance floors"))
            if energy > 0.7:
                insights.append(("⚡", "High Energy", "Great for workouts"))
            if valence > 0.6:
                insights.append(("😊", "Uplifting Vibes", "Positive mood booster"))
            if acousticness > 0.5:
                insights.append(("🎸", "Acoustic", "Organic sound"))
            
            if insights:
                cols = st.columns(len(insights))
                for col, (emoji, title, desc) in zip(cols, insights):
                    with col:
                        st.markdown(f"""
                        <div class='spotify-card'>
                            <div style='font-size: 1.5rem; margin-bottom: 10px;'>{emoji}</div>
                            <div style='font-weight: 700; color: #1DB954;'>{title}</div>
                            <div style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-top: 5px;'>{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== PAGE: BROWSE ======
    elif st.session_state.current_page == "🎧 Browse":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        
        st.markdown("""
        <h1 style='font-size: 3rem;'>
            <span class='gradient-text'>🎧 Browse Songs</span>
        </h1>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            min_pop = st.slider("Min Popularity", 0, 100, 50, key="browse_min")
        with col2:
            max_pop = st.slider("Max Popularity", 0, 100, 100, key="browse_max")
        with col3:
            search = st.text_input("Search Artist", placeholder="e.g., The Weeknd", key="search_artist")
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        
        filtered = df[(df['popularity'] >= min_pop) & (df['popularity'] <= max_pop)]
        if search:
            filtered = filtered[filtered['artist_name'].str.contains(search, case=False, na=False)]
        
        filtered = filtered.sort_values('popularity', ascending=False)
        
        st.markdown(f"**Found {len(filtered)} songs**")
        
        for idx, (_, song) in enumerate(filtered.head(15).iterrows(), 1):
            st.markdown(f"""
            <div class='song-card'>
                <h4 style='color: #1DB954; margin-bottom: 5px;'>#{idx} {song['track_name']}</h4>
                <p style='color: rgba(255,255,255,0.7); margin: 5px 0;'>👤 {song['artist_name']}</p>
                <div style='margin-top: 10px;'>
                    <span class='tag'>💃 {song['danceability']:.2f}</span>
                    <span class='tag'>⚡ {song['energy']:.2f}</span>
                    <span class='tag'>😊 {song['valence']:.2f}</span>
                    <span class='tag' style='float: right;'>🎵 {int(song['popularity'])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== PAGE: ANALYTICS ======
    elif st.session_state.current_page == "📊 Analytics":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        
        st.markdown("""
        <h1 style='font-size: 3rem;'>
            <span class='gradient-text'>📊 Music Analytics</span>
        </h1>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Avg Popularity</div>
                <div class='metric-value'>{df['popularity'].mean():.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Avg Energy</div>
                <div class='metric-value'>{df['energy'].mean():.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Avg Danceability</div>
                <div class='metric-value'>{df['danceability'].mean():.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Total Songs</div>
                <div class='metric-value'>{len(df)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin: 20px 0;'>🏆 Top 10 Artists</h3>", unsafe_allow_html=True)
        
        top_artists = df.groupby('artist_name')['popularity'].mean().nlargest(10)
        
        for idx, (artist, pop) in enumerate(top_artists.items(), 1):
            st.markdown(f"""
            <div class='spotify-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div><strong style='color: #1DB954;'>#{idx}</strong> <strong style='margin-left: 10px;'>{artist}</strong></div>
                    <div style='color: #1DB954; font-weight: 700; font-size: 1.2rem;'>{pop:.1f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== PAGE: FAVORITES ======
    elif st.session_state.current_page == "❤️ Favorites":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        
        st.markdown("""
        <h1 style='font-size: 3rem;'>
            <span class='gradient-text'>❤️ Your Favorites</span>
        </h1>
        """, unsafe_allow_html=True)
        
        if st.session_state.user_data['favorites']:
            for idx, fav in enumerate(st.session_state.user_data['favorites']):
                st.markdown(f"""
                <div class='spotify-card'>
                    <h4 style='color: #1DB954; margin-bottom: 5px;'>❤️ {fav.get('song', 'Unknown')}</h4>
                    <p style='color: rgba(255,255,255,0.7); margin: 5px 0;'>👤 {fav.get('artist', 'Unknown Artist')}</p>
                    <div style='margin-top: 10px;'>
                        <span class='tag'>⭐ {fav.get('score', 0)}/100</span>
                        <span class='tag'>📅 {fav.get('timestamp', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='spotify-card' style='text-align: center; padding: 40px;'>
                <div style='font-size: 3rem; margin-bottom: 20px;'>💔</div>
                <h3 style='color: rgba(255,255,255,0.6);'>No favorites yet!</h3>
                <p style='color: rgba(255,255,255,0.4);'>Add songs to see them here</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ====== PAGE: PROFILE ======
    elif st.session_state.current_page == "👤 Profile":
        st.markdown("<div class='page-container'>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <h1 style='font-size: 3rem;'>
            <span class='gradient-text'>👤 {st.session_state.username}'s Profile</span>
        </h1>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Predictions</div>
                <div class='metric-value'>{st.session_state.user_data['predictions_made']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Favorites</div>
                <div class='metric-value'>{len(st.session_state.user_data['favorites'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem;'>Member Since</div>
                <div class='metric-value'>Today</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN
# ============================================================================

if st.session_state.authenticated:
    show_app()
else:
    show_auth_page()
