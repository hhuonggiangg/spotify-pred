import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
import time
import hashlib
import urllib.parse

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Spotify Predictor", page_icon="🎵", layout="wide", initial_sidebar_state="expanded")

# ============================================================================
# CSS - ANIMATED GRADIENT BG + CURSORS + TRANSITIONS + INTERACTIVE
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* ---------- CUSTOM CURSORS ---------- */
html, body, [data-testid="stAppViewContainer"], .main {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E%3Ccircle cx='12' cy='12' r='3' fill='%231ed760'/%3E%3Ccircle cx='12' cy='12' r='9' fill='none' stroke='%231DB954' stroke-width='1.5'/%3E%3C/svg%3E") 12 12, auto;
}
button, a, [role="button"], [role="radio"], label, .stButton, .stTabs [data-baseweb="tab"] {
    cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='26' height='26'%3E%3Ccircle cx='13' cy='13' r='10' fill='none' stroke='%231ed760' stroke-width='2'/%3E%3Cpath d='M13 8 L13 18 M8 13 L18 13' stroke='%231ed760' stroke-width='2'/%3E%3C/svg%3E") 13 13, pointer !important;
}
input, textarea { cursor: text !important; }

/* ---------- ANIMATED GRADIENT BACKGROUND (pure gradient) ---------- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0F172A, #16324F, #1A1F3A, #0E2A22, #132238, #0F172A);
    background-size: 600% 600%;
    animation: gradientBG 24s ease infinite;
}
[data-testid="stHeader"] { background: transparent; }
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    20% { background-position: 50% 100%; }
    45% { background-position: 100% 50%; }
    70% { background-position: 50% 0%; }
    100% { background-position: 0% 50%; }
}

/* ---------- PAGE TRANSITION ---------- */
@keyframes pageIn {
    from { opacity: 0; transform: translateY(28px) scale(0.985); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.block-container { animation: pageIn 0.65s cubic-bezier(0.34, 1.56, 0.64, 1); }

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
@keyframes shimmer { 0% { left: -100%; } 100% { left: 100%; } }
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
.visualizer { display: flex; align-items: flex-end; justify-content: center; gap: 6px; height: 90px; margin: 28px 0; }
.bar {
    width: 12px;
    background: linear-gradient(180deg, #1DB954, #1ed760);
    border-radius: 6px;
    animation: bounceBar 0.8s ease-in-out infinite;
    box-shadow: 0 0 12px rgba(29,185,84,0.6);
}
@keyframes bounceBar { 0%, 100% { height: 14px; opacity: 0.65; } 50% { height: 62px; opacity: 1; } }
.bar:nth-child(1) { animation-delay: 0s; }
.bar:nth-child(2) { animation-delay: 0.1s; }
.bar:nth-child(3) { animation-delay: 0.2s; }
.bar:nth-child(4) { animation-delay: 0.3s; }
.bar:nth-child(5) { animation-delay: 0.4s; }
.bar:nth-child(6) { animation-delay: 0.5s; }
.bar:nth-child(7) { animation-delay: 0.4s; }
.bar:nth-child(8) { animation-delay: 0.3s; }

/* ---------- BUTTONS ---------- */
.stButton > button, .stLinkButton > a {
    background: linear-gradient(135deg, #1DB954, #1ed760) !important;
    color: black !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 22px !important;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    box-shadow: 0 5px 18px rgba(29,185,84,0.32) !important;
}
.stButton > button:hover, .stLinkButton > a:hover {
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

/* ---------- ARTIST PANEL + GRADIENT AVATAR ---------- */
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
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.4rem;
    font-weight: 900;
    color: white;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    margin: 0 auto 14px auto;
    box-shadow: 0 0 35px rgba(29,185,84,0.45);
    animation: avatarSpin 8s linear infinite, glowPulse 2.5s ease-in-out infinite;
    background-size: 200% 200% !important;
}
@keyframes avatarSpin {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.artist-avatar-sm {
    width: 52px;
    height: 52px;
    min-width: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.05rem;
    font-weight: 900;
    color: white;
    text-shadow: 0 1px 4px rgba(0,0,0,0.4);
    box-shadow: 0 0 14px rgba(29,185,84,0.3);
    background-size: 200% 200% !important;
    animation: avatarSpin 8s linear infinite;
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
.link-btn:hover { transform: translateY(-4px) scale(1.06); box-shadow: 0 10px 26px rgba(0,0,0,0.4); }
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

/* Expander */
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
# ARTIST DATABASE - FULL COVERAGE OF DATASET (84 artists)
# Keys are lowercase for accent/case-insensitive lookup
# ============================================================================

ARTISTS_DB = {
    "ac/dc": {"bio": "Legendary Australian hard rock band formed in 1973, famous for electrifying riffs.", "genres": ["Hard Rock", "Rock"], "hits": ["Highway to Hell", "Back in Black", "Thunderstruck"]},
    "aerosmith": {"bio": "Iconic American rock band from Boston, the 'Bad Boys from Boston'.", "genres": ["Rock", "Hard Rock"], "hits": ["Dream On", "I Don't Want to Miss a Thing", "Crazy"]},
    "anitta": {"bio": "Brazilian superstar bringing funk carioca and reggaeton to the world.", "genres": ["Funk", "Reggaeton", "Pop"], "hits": ["Envolver", "Downtown", "Vai Malandra"]},
    "arcángel": {"bio": "Puerto Rican reggaeton pioneer and one of Latin trap's biggest voices.", "genres": ["Reggaeton", "Latin Trap"], "hits": ["La Jumpa", "Sigues Con Él", "Me Prefieres a Mí"]},
    "arturo sandoval": {"bio": "Cuban jazz trumpet virtuoso, 10-time Grammy winner and protégé of Dizzy Gillespie.", "genres": ["Jazz", "Latin Jazz"], "hits": ["A Mis Abuelos", "Mambo Caliente", "Tumbaito"]},
    "aventura": {"bio": "Bronx bachata kings who modernized the genre for a global audience.", "genres": ["Bachata", "Latin"], "hits": ["Obsesión", "Dile al Amor", "El Perdedor"]},
    "bad bunny": {"bio": "Puerto Rican global phenomenon redefining reggaeton and Latin trap.", "genres": ["Reggaeton", "Latin Trap"], "hits": ["Tití Me Preguntó", "Me Porto Bonito", "Dakiti"]},
    "bad meets evil": {"bio": "Hip-hop duo of Eminem and Royce da 5'9\" with razor-sharp lyricism.", "genres": ["Hip-Hop", "Rap"], "hits": ["Lighters", "Fast Lane", "Welcome 2 Hell"]},
    "becky g": {"bio": "Mexican-American singer bridging Latin pop and urban music.", "genres": ["Latin Pop", "Reggaeton"], "hits": ["Mayores", "Sin Pijama", "Shower"]},
    "beyonce": {"bio": "Queen Bey — one of the greatest entertainers of all time.", "genres": ["Pop", "R&B"], "hits": ["Halo", "Crazy in Love", "Single Ladies"]},
    "big k.r.i.t.": {"bio": "Mississippi rapper-producer carrying the torch of Southern hip-hop.", "genres": ["Hip-Hop", "Southern Rap"], "hits": ["Country Shit", "1999", "Mt. Olympus"]},
    "black eyed peas": {"bio": "Genre-blending group behind some of the 2000s' biggest party anthems.", "genres": ["Pop", "Hip-Hop", "Dance"], "hits": ["I Gotta Feeling", "Where Is the Love?", "Boom Boom Pow"]},
    "bon jovi": {"bio": "New Jersey rock legends selling 130M+ records worldwide.", "genres": ["Rock", "Arena Rock"], "hits": ["Livin' on a Prayer", "It's My Life", "Always"]},
    "britney spears": {"bio": "The Princess of Pop who defined an era of pop music.", "genres": ["Pop", "Dance Pop"], "hits": ["...Baby One More Time", "Toxic", "Oops!... I Did It Again"]},
    "bruce springsteen": {"bio": "The Boss — heartland rock poet of the American working class.", "genres": ["Rock", "Heartland Rock"], "hits": ["Born to Run", "Dancing in the Dark", "Born in the U.S.A."]},
    "carlos gardel": {"bio": "The immortal voice of tango, Argentina's most beloved icon.", "genres": ["Tango"], "hits": ["Por una Cabeza", "El Día Que Me Quieras", "Volver"]},
    "chuck berry": {"bio": "Founding father of rock and roll whose guitar shaped modern music.", "genres": ["Rock and Roll"], "hits": ["Johnny B. Goode", "Roll Over Beethoven", "Maybellene"]},
    "crazy town": {"bio": "LA rap-rock band best known for their smash hit 'Butterfly'.", "genres": ["Rap Rock", "Nu Metal"], "hits": ["Butterfly", "Darkside", "Toxic"]},
    "dj snake": {"bio": "French producer fusing EDM with global pop and Latin sounds.", "genres": ["EDM", "Dance"], "hits": ["Taki Taki", "Lean On", "Turn Down for What"]},
    "daddy yankee": {"bio": "The King of Reggaeton who took the genre worldwide.", "genres": ["Reggaeton", "Latin"], "hits": ["Gasolina", "Despacito", "Con Calma"]},
    "donovan": {"bio": "Scottish folk-psychedelia troubadour of the 1960s.", "genres": ["Folk", "Psychedelic"], "hits": ["Sunshine Superman", "Mellow Yellow", "Hurdy Gurdy Man"]},
    "dua lipa": {"bio": "British-Albanian pop star known for disco-infused dance pop.", "genres": ["Pop", "Disco", "Dance"], "hits": ["Levitating", "Don't Start Now", "New Rules"]},
    "ed sheeran": {"bio": "English singer-songwriter blending pop, folk and acoustic sounds.", "genres": ["Pop", "Folk", "Acoustic"], "hits": ["Shape of You", "Perfect", "Photograph"]},
    "eddie santiago": {"bio": "Puerto Rican salsa romántica icon of the late 80s.", "genres": ["Salsa", "Latin"], "hits": ["Lluvia", "Que Locura Enamorarme de Ti", "Tú Me Quemas"]},
    "eslabon armado": {"bio": "California sierreño group behind the global hit 'Ella Baila Sola'.", "genres": ["Regional Mexican", "Sierreño"], "hits": ["Ella Baila Sola", "Jugaste y Sufrí", "Con Tus Besos"]},
    "eslabón armado": {"bio": "California sierreño group behind the global hit 'Ella Baila Sola'.", "genres": ["Regional Mexican", "Sierreño"], "hits": ["Ella Baila Sola", "Jugaste y Sufrí", "Con Tus Besos"]},
    "feid": {"bio": "Colombian reggaeton hitmaker also known as Ferxxo.", "genres": ["Reggaeton", "Latin"], "hits": ["Normal", "Ferxxo 100", "Classy 101"]},
    "fonseca": {"bio": "Colombian singer mixing vallenato and tropical pop.", "genres": ["Tropipop", "Vallenato"], "hits": ["Te Mando Flores", "Eres Mi Sueño", "Arroyito"]},
    "genesis": {"bio": "British prog-rock pioneers turned pop hit machine.", "genres": ["Prog Rock", "Pop Rock"], "hits": ["Invisible Touch", "Land of Confusion", "I Can't Dance"]},
    "girl in red": {"bio": "Norwegian indie-pop artist Marie Ulven, queer bedroom-pop icon.", "genres": ["Indie Pop", "Bedroom Pop"], "hits": ["we fell in love in october", "girls", "Serotonin"]},
    "glass animals": {"bio": "Oxford indie band behind the record-breaking 'Heat Waves'.", "genres": ["Indie Pop", "Psych Pop"], "hits": ["Heat Waves", "Gooey", "The Other Side of Paradise"]},
    "gracie abrams": {"bio": "American singer-songwriter crafting intimate confessional pop.", "genres": ["Pop", "Indie Pop"], "hits": ["I miss you, I'm sorry", "Mess It Up", "Risk"]},
    "grupo frontera": {"bio": "Texas norteño-cumbia group that exploded with 'No Se Va'.", "genres": ["Norteño", "Cumbia"], "hits": ["No Se Va", "un x100to", "Que Vuelvas"]},
    "grupo niche": {"bio": "Colombia's premier salsa orchestra from Cali.", "genres": ["Salsa", "Latin"], "hits": ["Cali Pachanguero", "Una Aventura", "Gotas de Lluvia"]},
    "gwen stefani": {"bio": "No Doubt frontwoman turned solo pop-ska superstar.", "genres": ["Pop", "Ska"], "hits": ["Hollaback Girl", "The Sweet Escape", "Rich Girl"]},
    "harry styles": {"bio": "British superstar redefining modern pop-rock with charisma and style.", "genres": ["Pop", "Pop Rock"], "hits": ["As It Was", "Watermelon Sugar", "Sign of the Times"]},
    "héctor lavoe": {"bio": "El Cantante — the legendary voice of salsa from Puerto Rico.", "genres": ["Salsa", "Latin"], "hits": ["El Cantante", "Periódico de Ayer", "Mi Gente"]},
    "imagine dragons": {"bio": "Las Vegas arena-rock band with stadium-sized anthems.", "genres": ["Pop Rock", "Alt Rock"], "hits": ["Believer", "Radioactive", "Thunder"]},
    "j balvin": {"bio": "Colombian reggaeton global ambassador, 'El Niño de Medellín'.", "genres": ["Reggaeton", "Latin"], "hits": ["Mi Gente", "Ginza", "Ay Vamos"]},
    "jack white": {"bio": "Rock polymath, White Stripes frontman and vinyl evangelist.", "genres": ["Rock", "Garage Rock"], "hits": ["Lazaretto", "Sixteen Saltines", "Love Interruption"]},
    "juan luis guerra": {"bio": "Dominican maestro of bachata and merengue with poetic lyrics.", "genres": ["Bachata", "Merengue"], "hits": ["Burbujas de Amor", "Ojalá Que Llueva Café", "Bachata Rosa"]},
    "justin timberlake": {"bio": "Pop-R&B icon who brought sexy back from NSYNC to solo stardom.", "genres": ["Pop", "R&B"], "hits": ["Cry Me a River", "Mirrors", "Can't Stop the Feeling!"]},
    "kendrick lamar": {"bio": "Pulitzer-winning Compton rapper, voice of a generation.", "genres": ["Hip-Hop", "Rap"], "hits": ["HUMBLE.", "Alright", "Not Like Us"]},
    "lany": {"bio": "LA trio crafting dreamy synth-driven heartbreak pop.", "genres": ["Indie Pop", "Synth Pop"], "hits": ["ILYSB", "Malibu Nights", "Super Far"]},
    "lmfao": {"bio": "Party-rock duo behind the world's biggest dance anthems of 2011.", "genres": ["Dance", "Electro Pop"], "hits": ["Party Rock Anthem", "Sexy and I Know It", "Shots"]},
    "lady gaga": {"bio": "Pop provocateur and powerhouse vocalist, Mother Monster.", "genres": ["Pop", "Dance"], "hits": ["Bad Romance", "Shallow", "Poker Face"]},
    "lewis capaldi": {"bio": "Scottish singer with gut-wrenching ballads and razor wit.", "genres": ["Pop", "Ballad"], "hits": ["Someone You Loved", "Before You Go", "Forget Me"]},
    "lil nas x": {"bio": "Genre-breaking artist who turned 'Old Town Road' into history.", "genres": ["Hip-Hop", "Pop"], "hits": ["Old Town Road", "MONTERO", "Industry Baby"]},
    "lil wayne": {"bio": "New Orleans rap legend, one of the most influential MCs ever.", "genres": ["Hip-Hop", "Rap"], "hits": ["Lollipop", "A Milli", "6 Foot 7 Foot"]},
    "lizzo": {"bio": "Flute-playing superstar spreading self-love and funk-pop joy.", "genres": ["Pop", "Funk", "R&B"], "hits": ["About Damn Time", "Truth Hurts", "Good as Hell"]},
    "los panchos": {"bio": "Legendary trío romántico that defined the bolero era.", "genres": ["Bolero", "Latin"], "hits": ["Bésame Mucho", "Sabor a Mí", "Contigo"]},
    "luis fonsi": {"bio": "Puerto Rican singer behind the most-streamed Spanish song ever.", "genres": ["Latin Pop", "Reggaeton"], "hits": ["Despacito", "Échame la Culpa", "No Me Doy por Vencido"]},
    "luis miguel": {"bio": "El Sol de México — Latin music's golden voice.", "genres": ["Latin Pop", "Bolero"], "hits": ["La Incondicional", "Ahora Te Puedes Marchar", "Hasta Que Me Olvides"]},
    "malo": {"bio": "70s Latin rock band led by Jorge Santana, famous for 'Suavecito'.", "genres": ["Latin Rock"], "hits": ["Suavecito", "Café", "Nena"]},
    "mark ronson": {"bio": "Super-producer behind era-defining funk-pop smashes.", "genres": ["Funk", "Pop"], "hits": ["Uptown Funk", "Nothing Breaks Like a Heart", "Valerie"]},
    "metallica": {"bio": "The biggest metal band in history, thrash pioneers.", "genres": ["Metal", "Thrash"], "hits": ["Enter Sandman", "Master of Puppets", "Nothing Else Matters"]},
    "miley cyrus": {"bio": "Pop chameleon who evolved from Disney star to rock-pop powerhouse.", "genres": ["Pop", "Rock"], "hits": ["Flowers", "Wrecking Ball", "Party in the U.S.A."]},
    "modern talking": {"bio": "German europop duo with unmistakable 80s synth sound.", "genres": ["Europop", "Synth Pop"], "hits": ["You're My Heart, You're My Soul", "Cheri Cheri Lady", "Brother Louie"]},
    "myke towers": {"bio": "Puerto Rican rapper-singer dominating the Latin urban scene.", "genres": ["Reggaeton", "Latin Trap"], "hits": ["LALA", "Diosa", "Bandido"]},
    "nicky youre": {"bio": "California artist behind the feel-good viral hit 'Sunroof'.", "genres": ["Pop"], "hits": ["Sunroof", "Eyes On You", "Sex and Lemonade"]},
    "nirvana": {"bio": "Seattle grunge icons who changed rock forever.", "genres": ["Grunge", "Rock"], "hits": ["Smells Like Teen Spirit", "Come as You Are", "Heart-Shaped Box"]},
    "olivia rodrigo": {"bio": "Gen-Z pop-rock sensation of heartbreak anthems.", "genres": ["Pop", "Pop Punk"], "hits": ["drivers license", "good 4 u", "vampire"]},
    "oscar d'león": {"bio": "El Sonero del Mundo — Venezuela's salsa giant.", "genres": ["Salsa", "Latin"], "hits": ["Llorarás", "Detalles", "Mi Bajo y Yo"]},
    "paquito d'rivera": {"bio": "Cuban clarinet & sax master bridging jazz and classical.", "genres": ["Latin Jazz", "Jazz"], "hits": ["Mambo Influenciado", "Tico Tico", "A Night in Tunisia"]},
    "pearl jam": {"bio": "Seattle grunge survivors with three decades of anthems.", "genres": ["Grunge", "Rock"], "hits": ["Alive", "Even Flow", "Black"]},
    "ruel": {"bio": "Australian singer with soulful vocals beyond his years.", "genres": ["Pop", "R&B"], "hits": ["Painkiller", "Younger", "Dazed & Confused"]},
    "rihanna": {"bio": "Barbadian icon — singer, mogul, and global hitmaker.", "genres": ["Pop", "R&B"], "hits": ["Umbrella", "Diamonds", "We Found Love"]},
    "rosalia": {"bio": "Spanish visionary fusing flamenco with avant-garde pop.", "genres": ["Flamenco Pop", "Urbano"], "hits": ["Despechá", "Malamente", "Con Altura"]},
    "rubén blades": {"bio": "Panamanian salsa poet, actor and political voice.", "genres": ["Salsa", "Latin"], "hits": ["Pedro Navaja", "Plástico", "Decisiones"]},
    "sabrina carpenter": {"bio": "Pop's sharpest pen with playful, viral-ready hits.", "genres": ["Pop"], "hits": ["Espresso", "Please Please Please", "Nonsense"]},
    "soundgarden": {"bio": "Grunge heavyweights led by the late great Chris Cornell.", "genres": ["Grunge", "Rock"], "hits": ["Black Hole Sun", "Spoonman", "Fell on Black Days"]},
    "steve miller band": {"bio": "Classic-rock staple with breezy 70s FM gold.", "genres": ["Classic Rock"], "hits": ["The Joker", "Fly Like an Eagle", "Abracadabra"]},
    "stone temple pilots": {"bio": "90s alt-rock hitmakers fronted by Scott Weiland.", "genres": ["Alt Rock", "Grunge"], "hits": ["Plush", "Interstate Love Song", "Creep"]},
    "taylor swift": {"bio": "American singer-songwriter spanning country, pop and indie-folk eras.", "genres": ["Pop", "Country", "Folk"], "hits": ["Anti-Hero", "Blank Space", "Cruel Summer"]},
    "the beach boys": {"bio": "California legends who invented the sound of summer.", "genres": ["Pop", "Surf Rock"], "hits": ["Good Vibrations", "God Only Knows", "Surfin' U.S.A."]},
    "the black keys": {"bio": "Ohio blues-rock duo with gritty garage grooves.", "genres": ["Blues Rock", "Garage"], "hits": ["Lonely Boy", "Tighten Up", "Gold on the Ceiling"]},
    "the kid laroi": {"bio": "Australian melodic rap prodigy gone global.", "genres": ["Pop", "Hip-Hop"], "hits": ["STAY", "Without You", "Love Again"]},
    "the neighbourhood": {"bio": "California band behind the moody mega-hit 'Sweater Weather'.", "genres": ["Alt Rock", "Indie"], "hits": ["Sweater Weather", "Daddy Issues", "Softcore"]},
    "the weeknd": {"bio": "Canadian superstar famous for dark, cinematic R&B-pop.", "genres": ["Pop", "R&B", "Synthwave"], "hits": ["Blinding Lights", "Starboy", "The Hills"]},
    "the white stripes": {"bio": "Detroit duo that revived garage rock with red-white minimalism.", "genres": ["Garage Rock", "Blues"], "hits": ["Seven Nation Army", "Fell in Love with a Girl", "Icky Thump"]},
    "usher": {"bio": "R&B king with three decades of smooth chart-toppers.", "genres": ["R&B", "Pop"], "hits": ["Yeah!", "U Got It Bad", "Confessions Part II"]},
    "willie colon": {"bio": "Trombone titan and salsa architect from the Bronx.", "genres": ["Salsa", "Latin"], "hits": ["Idilio", "Gitana", "Talento de Televisión"]},
    "yng lvcas": {"bio": "Mexican corridos tumbados artist behind 'La Bebe'.", "genres": ["Corridos", "Reggaeton"], "hits": ["La Bebe", "El Rescate", "Mami Chula"]},
}

# Gradient palette for artist avatars (pairs of colors)
AVATAR_GRADIENTS = [
    ("#1DB954", "#1ed760"), ("#667eea", "#764ba2"), ("#f093fb", "#f5576c"),
    ("#4facfe", "#00f2fe"), ("#43e97b", "#38f9d7"), ("#fa709a", "#fee140"),
    ("#a18cd1", "#fbc2eb"), ("#ff9a9e", "#fecfef"), ("#30cfd0", "#330867"),
    ("#ff6e7f", "#bfe9ff"), ("#e96443", "#904e95"), ("#11998e", "#38ef7d"),
    ("#fc466b", "#3f5efb"), ("#00c6ff", "#0072ff"), ("#f7971e", "#ffd200"),
    ("#8E2DE2", "#4A00E0"), ("#ee0979", "#ff6a00"), ("#56ab2f", "#a8e063"),
]

def get_artist_info(name):
    key = str(name).strip().lower()
    base = ARTISTS_DB.get(key)
    q = urllib.parse.quote(str(name))
    info = {
        "bio": base["bio"] if base else "Rising artist — dive into their catalog on Spotify and YouTube!",
        "genres": base["genres"] if base else ["Music"],
        "hits": base["hits"] if base else [],
        "spotify": f"https://open.spotify.com/search/{q}",
        "youtube": f"https://www.youtube.com/results?search_query={q}",
    }
    return info

def get_avatar_style(name):
    """Deterministic gradient avatar based on artist name"""
    h = int(hashlib.md5(str(name).strip().lower().encode()).hexdigest(), 16)
    c1, c2 = AVATAR_GRADIENTS[h % len(AVATAR_GRADIENTS)]
    angle = 90 + (h % 180)
    return f"background: linear-gradient({angle}deg, {c1}, {c2});"

def get_initials(name):
    words = [w for w in str(name).replace("/", " ").split() if w]
    if not words:
        return "♪"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[-1][0]).upper()

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
if 'browse_count' not in st.session_state:
    st.session_state.browse_count = 10
if 'analytics_count' not in st.session_state:
    st.session_state.analytics_count = 10

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
    avatar_style = get_avatar_style(name)
    initials = get_initials(name)
    genres_html = ''.join([f'<span class="tag">{g}</span>' for g in info["genres"]])
    hits_html = ''.join([f'<span class="tag">♪ {h}</span>' for h in info["hits"]]) or '<span class="tag">Discover their hits</span>'
    
    st.markdown(f"""
    <div class="artist-panel">
        <div class="artist-avatar" style="{avatar_style}">{initials}</div>
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
            <a class="link-btn spotify-btn" href="{info["spotify"]}" target="_blank">🎵 Listen on Spotify</a>
            <a class="link-btn youtube-btn" href="{info["youtube"]}" target="_blank">📺 Watch MV on YouTube</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align:center; margin-top:40px;"><h1 class="logo-glow" style="font-size:4.2rem; margin:0;"><span class="gradient-text">♪</span></h1></div>', unsafe_allow_html=True)
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
        
        with st.expander(f"🎤 About {last['artist']}"):
            render_artist_panel(last['artist'])
        
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
    st.markdown('<p style="opacity:0.7;">Click any song to open artist info, gradient portrait and Spotify / YouTube links</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: minp = st.slider("Min Popularity", 0, 100, 0)
    with c2: maxp = st.slider("Max Popularity", 0, 100, 100)
    with c3: srch = st.text_input("Search Artist", placeholder="Type artist name...")
    
    filt = df[(df['popularity'] >= minp) & (df['popularity'] <= maxp)]
    if srch:
        filt = filt[filt['artist_name'].str.contains(srch, case=False, na=False)]
    filt = filt.sort_values('popularity', ascending=False)
    
    total = len(filt)
    shown = min(st.session_state.browse_count, total)
    st.markdown(f"**Showing {shown} / {total} songs**")
    
    for idx, (_, r) in enumerate(filt.head(shown).iterrows(), 1):
        artist_name = str(r['artist_name'])
        avatar_style = get_avatar_style(artist_name)
        initials = get_initials(artist_name)
        
        st.markdown(f'''
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:14px;">
                    <div class="artist-avatar-sm" style="{avatar_style}">{initials}</div>
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
        
        with st.expander(f"🎤 View {artist_name} — info & links"):
            render_artist_panel(artist_name)
    
    # LOAD MORE / LOAD ALL
    if shown < total:
        lc1, lc2, lc3, lc4 = st.columns([1, 1, 1, 1])
        with lc2:
            if st.button(f"⬇️ Load 10 More", use_container_width=True, key="browse_more"):
                st.session_state.browse_count += 10
                st.rerun()
        with lc3:
            if st.button(f"📥 Load All ({total})", use_container_width=True, key="browse_all"):
                st.session_state.browse_count = total
                st.rerun()
    else:
        st.success(f"✅ All {total} songs loaded!")
        if total > 10:
            cc1, cc2, cc3 = st.columns([1, 1, 1])
            with cc2:
                if st.button("🔼 Collapse to 10", use_container_width=True, key="browse_collapse"):
                    st.session_state.browse_count = 10
                    st.rerun()

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
    
    ranked = df.groupby('artist_name')['popularity'].mean().sort_values(ascending=False)
    total_artists = len(ranked)
    shown = min(st.session_state.analytics_count, total_artists)
    
    st.markdown(f'<h3 style="margin-top:25px;">🏆 Artist Ranking — showing {shown} / {total_artists}</h3>', unsafe_allow_html=True)
    
    for idx, (a, p) in enumerate(ranked.head(shown).items(), 1):
        artist_name = str(a)
        avatar_style = get_avatar_style(artist_name)
        initials = get_initials(artist_name)
        st.markdown(f'<div class="card"><div style="display:flex; justify-content:space-between; align-items:center;"><div style="display:flex; align-items:center; gap:12px;"><div class="artist-avatar-sm" style="{avatar_style}">{initials}</div><strong>#{idx} {artist_name}</strong></div><span style="color:#1ed760; font-weight:900; font-size:1.2rem;">{p:.1f}</span></div></div>', unsafe_allow_html=True)
        with st.expander(f"View {artist_name}"):
            render_artist_panel(artist_name)
    
    # LOAD MORE / LOAD ALL
    if shown < total_artists:
        lc1, lc2, lc3, lc4 = st.columns([1, 1, 1, 1])
        with lc2:
            if st.button("⬇️ Load 10 More", use_container_width=True, key="analytics_more"):
                st.session_state.analytics_count += 10
                st.rerun()
        with lc3:
            if st.button(f"📥 Load All ({total_artists})", use_container_width=True, key="analytics_all"):
                st.session_state.analytics_count = total_artists
                st.rerun()
    else:
        st.success(f"✅ All {total_artists} artists loaded!")
        if total_artists > 10:
            cc1, cc2, cc3 = st.columns([1, 1, 1])
            with cc2:
                if st.button("🔼 Collapse to 10", use_container_width=True, key="analytics_collapse"):
                    st.session_state.analytics_count = 10
                    st.rerun()

def page_favorites():
    st.markdown('<h1><span class="gradient-text">❤️ Your Favorites</span></h1>', unsafe_allow_html=True)
    
    favs = st.session_state.stats['favs']
    if favs:
        for i, f in enumerate(favs, 1):
            avatar_style = get_avatar_style(f['artist'])
            initials = get_initials(f['artist'])
            st.markdown(f'<div class="card"><div style="display:flex; align-items:center; gap:12px;"><div class="artist-avatar-sm" style="{avatar_style}">{initials}</div><div><strong style="color:#1DB954;">#{i} ❤️ {f["song"]}</strong><div style="opacity:0.7; margin:4px 0;">{f["artist"]}</div><span class="tag">Score: {f["score"]}/100</span></div></div></div>', unsafe_allow_html=True)
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
