import streamlit as st
import pandas as pd

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI App Finder", layout="wide")

# ---------------- THEME ----------------
st.markdown("""
<style>
.stApp { background-color: #020617; color: #e5e7eb; }

h1,h2,h3 { color: #ef4444; }

.card {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.top-card {
    background: #1f2937;
    border: 2px solid #ef4444;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI App Finder")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("MASTER_DATASET.xlsx")

# ---------------- CLEAN ----------------
df = df.fillna("")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["downloads"] = pd.to_numeric(df["downloads"], errors="coerce")
df = df.dropna()
df = df.drop_duplicates(subset=["app_name"])

# ---------------- FILTERS ----------------

st.sidebar.header("Filters")

# Category
category = st.sidebar.selectbox(
    "Category", ["All"] + sorted(df["category"].unique())
)

# Sub-category (dynamic)
if category != "All":
    sub_category = st.sidebar.selectbox(
        "Sub Category",
        ["All"] + sorted(df[df["category"] == category]["sub_category"].unique())
    )
else:
    sub_category = "All"

# Price
price = st.sidebar.selectbox(
    "Price Level", ["All", "free", "low", "medium", "high"]
)

# Rating
rating = st.sidebar.slider("Minimum Rating", 3.5, 5.0, 4.0)

# ---------------- FILTER LOGIC ----------------

filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[filtered_df["category"] == category]

if sub_category != "All":
    filtered_df = filtered_df[filtered_df["sub_category"] == sub_category]

if price != "All":
    filtered_df = filtered_df[filtered_df["price_level"] == price]

filtered_df = filtered_df[filtered_df["rating"] >= rating]

# ---------------- SORT ----------------
filtered_df = filtered_df.sort_values(by=["rating", "downloads"], ascending=False)

# ---------------- OUTPUT ----------------

st.subheader("Top Recommendation")

if not filtered_df.empty:

    top = filtered_df.iloc[0]

    st.markdown(f"""
    <div class="top-card">
        <h2>{top['app_name']}</h2>
        <p>Rating: {top['rating']} | Downloads: {int(top['downloads'])}</p>
        <p>{top['category']} | {top['sub_category']} | {top['price_level']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Other Apps")

    cols = st.columns(3)

    for i, (_, app) in enumerate(filtered_df.iloc[1:10].iterrows()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h3>{app['app_name']}</h3>
                <p>Rating: {app['rating']}</p>
                <p>Downloads: {int(app['downloads'])}</p>
                <p>{app['sub_category']} | {app['price_level']}</p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.warning("No apps match your filters")
