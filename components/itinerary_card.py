import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMG_DIR = BASE_DIR / "assets" / "images"

IMAGE_MAP = {
    "fort": "fort.jpg",
    "beach": "beach.jpg",
    "market": "market.jpg",
    "park": "planning.jpg",
    "temple": "fort.jpg",
    "museum": "planning.jpg"
}

def render_itinerary(itinerary):
    st.markdown("## 🗺️ Day-wise Itinerary")

    cols = st.columns(len(itinerary))

    for col, day in zip(cols, itinerary):
        with col:
            place = day["activities"][0].lower()
            img = "planning.jpg"

            for key in IMAGE_MAP:
                if key in place:
                    img = IMAGE_MAP[key]
                    break

            st.markdown(
                f"""
                <div class="itinerary-card">
                    <img src="data:image/jpeg;base64,{_img_to_base64(img)}">
                    <h4>{day['day']}</h4>
                    <p>{', '.join(day['activities'])}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

def _img_to_base64(img_name):
    import base64
    with open(IMG_DIR / img_name, "rb") as f:
        return base64.b64encode(f.read()).decode()
