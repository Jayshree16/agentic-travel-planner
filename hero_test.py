import streamlit as st
from pathlib import Path
import base64

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(layout="wide")

BASE_DIR = Path(__file__).parent
IMAGE_PATH = BASE_DIR / "assets" / "images" / "hero_plane.jpg"

# -----------------------------
# Load image as base64
# -----------------------------
def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if not IMAGE_PATH.exists():
    st.error("hero_plane.jpg not found")
    st.stop()

img_base64 = load_image_base64(IMAGE_PATH)

# -----------------------------
# CSS (REAL CONTROL)
# -----------------------------
st.markdown("""
<style>
.hero {
    position: relative;
    width: 100%;
    height: 400px;              /* 🔥 VERY SMALL */
    overflow: hidden;
    border-radius: 12px;
    margin-bottom: 20px;
}

.hero img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-text {
    position: absolute;
    top: 50%;
    left: 4%;
    transform: translateY(-50%);
    color: white;
    font-size: 18px;
    font-weight: 600;
    text-shadow: 0 1px 4px rgba(0,0,0,0.7);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO RENDER (HTML IMG)
# -----------------------------
st.markdown(f"""
<div class="hero">
    <img src="data:image/jpeg;base64,{img_base64}">
    <div class="hero-text">
        Agentic AI Travel Planner ✈️
    </div>
</div>
""", unsafe_allow_html=True)
