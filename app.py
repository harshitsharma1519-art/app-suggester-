import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Mr Suggester", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("FINAL_WITH_LINKS.xlsx")
df = df.drop_duplicates(subset=["app_name", "sub_category"])

# ---------------- UI STYLE ----------------
st.markdown("""
<style>

/* GOOGLE FONT */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

/* REMOVE WHITE BG */
.stApp {
    background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
    color: white;
}

[data-testid="stAppViewContainer"] {
    background-color: #0f0f0f;
}

.block-container {
    background-color: transparent !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #121212, #0f0f0f);
    padding: 20px;
    border-right: 1px solid #ff2c2c;
}

/* SIDEBAR TITLE */
.sidebar-title {
    font-size: 24px;
    font-weight: bold;
    color: #ff2c2c;
    text-shadow: 0 0 10px rgba(255,0,0,0.5);
}

/* LABELS */
label {
    color: #e5e5e5 !important;
}

/* DROPDOWN */
div[data-baseweb="select"] {
    background-color: #1a1a1a !important;
    border-radius: 10px !important;
    border: 1px solid #333 !important;
}

div[data-baseweb="select"]:hover {
    border: 1px solid #ff2c2c !important;
}

/* TITLE */
.title {
    font-family: 'Orbitron', sans-serif;
    font-size: 50px;
    text-align: center;
    color: #ff2c2c;
    text-shadow: 0 0 20px rgba(255,0,0,0.7);
}

/* GLASS CARD */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 18px;
    margin: 12px 0;
    border: 1px solid rgba(255,44,44,0.3);
    box-shadow: 0 8px 25px rgba(255,0,0,0.2);
    transition: 0.3s;
}

/* HOVER */
.glass-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 12px 35px rgba(255,0,0,0.6);
}

/* TEXT */
.subtext {
    color: #d1d5db;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #ff2c2c, #b91c1c);
    color: white;
    border-radius: 10px;
}

/* ANIMATION */
.fade-in {
    animation: fadeIn 0.7s ease-in;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<i><div class="title">Mr Suggester</div></i>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown('<i><div class="sidebar-title">welcome</div></i>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<h2 style='color:#ff2c2c; text-shadow:0 0 10px rgba(255,0,0,0.7);'>Filters</h2>",
    unsafe_allow_html=True
)

category = st.sidebar.selectbox("Category", ["All"] + list(df["category"].unique()))
if category != "All":
    df = df[df["category"] == category]

sub_category = st.sidebar.selectbox("Sub Category", ["All"] + list(df["sub_category"].unique()))
if sub_category != "All":
    df = df[df["sub_category"] == sub_category]

price = st.sidebar.selectbox("Price", ["All"] + list(df["price_level"].unique()))
if price != "All":
    df = df[df["price_level"] == price]

# ---------------- SORT ----------------
df = df.sort_values(by=["rating", "downloads"], ascending=False)

# ---------------- DISPLAY ----------------
st.subheader("Recommended Apps")

cols = st.columns(3)

for i, row in df.head(30).iterrows():
    with cols[i % 3]:

        st.markdown(f"""
        <div class="glass-card fade-in">
            <h3>{row['app_name']}</h3>
            <p class="subtext">Category: {row['category']}</p>
            <p class="subtext">Type: {row['sub_category']}</p>
            <p class="subtext">Rating: {row['rating']}</p>
            <p class="subtext">Price: {row['price_level']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Open App", row["app_link"])

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
