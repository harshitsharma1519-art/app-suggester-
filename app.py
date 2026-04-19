import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Mr Suggester", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_excel("FINAL_WITH_LINKS.xlsx")
    df = df.drop_duplicates(subset=["app_name", "sub_category"])
    return df

df = load_data()

# ---------------- SESSION ----------------

if "started" not in st.session_state:
    st.session_state.started = False

# ---------------- LOTTIE ----------------
def load_lottie(url):
    return requests.get(url).json()

lottie_empty = load_lottie("https://assets10.lottiefiles.com/packages/lf20_x62chJ.json")
lottie_start = load_lottie("https://assets1.lottiefiles.com/packages/lf20_2LdLki.json")

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

/* SELECTED VALUE TEXT (All, Category, etc.) */
div[data-baseweb="select"] div {
    color: #000000 !important;   /* BLACK TEXT */
    font-weight: 500;
}
            /* SIDEBAR DROPDOWN ARROW */
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #000000 !important;   /* BLACK ARROW */
}
                    
/* BACKGROUND */
.stApp {
    background: linear-gradient(270deg, #0f0f0f, #1a0000, #0f0f0f);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
    color: #f9fafb;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* TITLE */
.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 55px;
    text-align: center;
    color: #ff4d4d;
    text-shadow: 0 0 25px rgba(255,0,0,0.7);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0000, #0f0000);
    border-right: 1px solid #ff2c2c;
}
section[data-testid="stSidebar"] * {
    color: #f9fafb !important;
}

/* DROPDOWN */
div[data-baseweb="select"] {
    background-color: #1a0000 !important;
    border: 1px solid #ff2c2c !important;
}
ul[role="listbox"] {
    background-color: #1a0000 !important;
}
ul[role="listbox"] li:hover {
    background-color: #ff2c2c !important;
}

/* BUTTON */
div.stButton > button {
    background: linear-gradient(135deg, #ff2c2c, #b91c1c);
    color: white;
    border-radius: 10px;
    transition: 0.3s;
}
div.stButton > button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 20px rgba(255,0,0,0.7);
}

/* CARD */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 18px;
    margin: 10px 0;
    border: 1px solid rgba(255,44,44,0.3);
    transition: 0.3s;
}
.glass-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 30px rgba(255,0,0,0.6);
}

/* PROGRESS BAR */
.progress {
    height: 8px;
    background: #1f1f1f;
    border-radius: 10px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff2c2c, #ff6b6b);
}

/* TEXT */
.subtext {
    color: #d1d5db;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
if not st.session_state.started:

    st.markdown('<div class="title">Mr Suggester</div>', unsafe_allow_html=True)
    st_lottie(lottie_start, height=250)

    st.markdown("<h3 style='text-align:center;'>Find the perfect apps effortlessly 🚀</h3>", unsafe_allow_html=True)

    if st.button("🚀 Start Exploring"):
        st.session_state.started = True
        st.rerun()

# ---------------- MAIN ----------------
else:

    st.markdown('<div class="title">Mr Suggester</div>', unsafe_allow_html=True)

    # SIDEBAR
    st.sidebar.header("Filters")

    category = st.sidebar.selectbox("Category", ["All"] + list(df["category"].unique()))
    if category != "All":
        df = df[df["category"] == category]

    sub_category = st.sidebar.selectbox("Sub Category", ["All"] + list(df["sub_category"].unique()))
    if sub_category != "All":
        df = df[df["sub_category"] == sub_category]

    price = st.sidebar.selectbox("Price", ["All"] + list(df["price_level"].unique()))
    if price != "All":
        df = df[df["price_level"] == price]

    df = df.sort_values(by=["rating", "downloads"], ascending=False)

    # 🔥 PROGRESS BAR (WOW FEATURE)
    total = len(load_data())
    current = len(df)
    percent = int((current / total) * 100)

    st.markdown(f"""
    <div class="progress">
        <div class="progress-fill" style="width:{percent}%"></div>
    </div>
    <p class="subtext">{current} apps matched ({percent}%)</p>
    """, unsafe_allow_html=True)

    st.subheader("Recommended Apps")

    if df.empty:
        st_lottie(lottie_empty, height=200)
        st.warning("No apps found 😢")

    else:
        cols = st.columns(3)

        for i, row in df.head(30).iterrows():
            with cols[i % 3]:

                st.markdown(f"""
                <div class="glass-card">
                    <h3>{row['app_name']}</h3>
                    <p class="subtext">{row['category']} • {row['sub_category']}</p>
                    <p>⭐ {row['rating']} | 💰 {row['price_level']}</p>
                </div>
                """, unsafe_allow_html=True)

                st.link_button("Open App", row["app_link"])



# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:#9ca3af;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
