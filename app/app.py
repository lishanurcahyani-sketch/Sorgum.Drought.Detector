import os
import sys
import base64
import cv2
import numpy as np
import pandas as pd
import streamlit as st
import tempfile
from PIL import Image

# supaya bisa import dari folder root project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from roboflow_utils import predict_image, draw_predictions, summarize_predictions


st.set_page_config(
    page_title="Sorghum Drought Detector",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def get_base64_image(image_path: str):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# karena app.py ada di folder /app
bg_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sorghum_bg.jpg")
bg_base64 = get_base64_image(bg_path)

if bg_base64:
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background:
            linear-gradient(rgba(8, 22, 14, 0.72), rgba(8, 22, 14, 0.82)),
            url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
else:
    bg_css = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #123524 0%, #1f5134 50%, #2f6e43 100%);
    }
    </style>
    """

st.markdown(bg_css, unsafe_allow_html=True)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 1rem 1.35rem;
        border-radius: 24px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.16);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.22);
        margin-bottom: 1.2rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        color: white;
    }

    .brand-icon {
        font-size: 2.1rem;
    }

    .brand-title {
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: rgba(255,255,255,0.84);
        font-size: 0.96rem;
        margin-top: 0.15rem;
    }

    .nav-links {
        display: flex;
        gap: 0.7rem;
        flex-wrap: wrap;
    }

    .nav-pill {
        color: white;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.14);
        padding: 0.55rem 0.95rem;
        border-radius: 999px;
        font-size: 0.95rem;
        font-weight: 600;
        transition: 0.25s ease;
    }

    .hero-card {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.16);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 12px 34px rgba(0,0,0,0.22);
        border-radius: 28px;
        padding: 1.6rem;
        color: white;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 850;
        line-height: 1.1;
        margin-bottom: 0.55rem;
    }

    .hero-desc {
        font-size: 1.03rem;
        line-height: 1.7;
        color: rgba(255,255,255,0.9);
    }

    .feature-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin-top: 1rem;
    }

    .feature-pill {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.16);
        color: white;
        padding: 0.58rem 0.95rem;
        border-radius: 999px;
        font-size: 0.92rem;
        font-weight: 650;
    }

    .glass-card {
        background: rgba(255,255,255,0.11);
        border: 1px solid rgba(255,255,255,0.16);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 12px 36px rgba(0,0,0,0.22);
        border-radius: 24px;
        padding: 1.25rem;
        color: white;
        margin-bottom: 1rem;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 780;
        color: white;
        margin-bottom: 0.7rem;
    }

    .legend-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin-top: 0.8rem;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.62rem 0.95rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.14);
        color: white;
        font-weight: 650;
    }

    .dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
    }

    .green { background: #22c55e; }
    .yellow { background: #facc15; }
    .red { background: #ef4444; }

    .note {
        margin-top: 0.85rem;
        padding: 0.95rem 1rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.10);
        border-left: 4px solid #93c5fd;
        color: white;
        line-height: 1.6;
    }

    .empty-result {
        min-height: 320px;
        border-radius: 22px;
        background: rgba(255,255,255,0.08);
        border: 1px dashed rgba(255,255,255,0.22);
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.05rem;
        padding: 1rem;
    }

    .subtle-text {
        color: rgba(255,255,255,0.88);
        line-height: 1.65;
        font-size: 0.98rem;
    }

    .soft-divider {
        height: 1px;
        margin: 0.6rem 0 0.8rem 0;
        background: linear-gradient(to right, rgba(255,255,255,0.0), rgba(255,255,255,0.25), rgba(255,255,255,0.0));
    }

    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.08);
        border: 1px dashed rgba(255,255,255,0.24);
        border-radius: 22px;
        padding: 0.4rem;
    }

    div[data-testid="stFileUploader"] label,
    div[data-testid="stSlider"] label {
        color: white !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 20px;
        padding: 0.9rem 0.9rem;
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: white !important;
    }

    .footer-tag {
        text-align: center;
        color: rgba(255,255,255,0.72);
        font-size: 0.92rem;
        margin-top: 1.25rem;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="navbar">
    <div class="brand">
        <div class="brand-icon">🌾</div>
        <div>
            <div class="brand-title">Sorghum Drought Detector</div>
            <div class="brand-subtitle">Smart detection for drought symptoms on sorghum leaves</div>
        </div>
    </div>
    <div class="nav-links">
        <div class="nav-pill">Home</div>
        <div class="nav-pill">Unggah Gambar</div>
        <div class="nav-pill">Hasil</div>
        <div class="nav-pill">Tentang</div>
    </div>
</div>
""", unsafe_allow_html=True)


left_col, right_col = st.columns([1.05, 0.95], gap="large")

with left_col:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Deteksi Kekeringan Daun Sorgum secara Visual</div>
        <div class="hero-desc">
            Unggah citra daun sorgum untuk mengidentifikasi kondisi <b>Daun Segar</b>,
            <b>Kekeringan Ringan</b>, dan <b>Kekeringan Berat</b> menggunakan model object detection berbasis Roboflow.
        </div>
        <div class="feature-row">
            <div class="feature-pill">Bounding Box</div>
            <div class="feature-pill">Confidence Filter</div>
            <div class="feature-pill">Object Detection</div>
            <div class="feature-pill">Real-time Visualization</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Pengaturan Deteksi</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle-text">Atur confidence threshold untuk menyaring prediksi yang terlalu lemah.</div>', unsafe_allow_html=True)

    conf_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.10,
        max_value=0.95,
        value=0.40,
        step=0.05
    )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Unggah gambar daun sorgum",
        type=["jpg", "jpeg", "png", "bmp"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class="glass-card">
        <div class="card-title">Legenda Kelas</div>
        <div class="legend-wrap">
            <div class="legend-item"><div class="dot green"></div><span>Daun Segar</span></div>
            <div class="legend-item"><div class="dot yellow"></div><span>Kekeringan Ringan</span></div>
            <div class="legend-item"><div class="dot red"></div><span>Kekeringan Berat</span></div>
        </div>
        <div class="note">
            Hasil analisis akan menampilkan bounding box pada area daun yang terdeteksi, lengkap dengan label kelas dan confidence score.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">Preview Hasil</div>
            <div class="empty-result">
                Unggah gambar terlebih dahulu untuk melihat hasil deteksi di sini.
            </div>
        </div>
        """, unsafe_allow_html=True)


if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np_rgb = np.array(image)
    image_np_bgr = cv2.cvtColor(image_np_rgb, cv2.COLOR_RGB2BGR)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        temp_path = tmp.name

    try:
        result = predict_image(temp_path)

        col_a, col_b = st.columns([1, 1], gap="large")

        with col_a:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Gambar Asli</div>', unsafe_allow_html=True)
            st.image(image_np_rgb, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Hasil Bounding Box</div>', unsafe_allow_html=True)

            if not result.get("success", False):
                st.error(result.get("error", "Prediksi gagal."))
                filtered_predictions = []
            else:
                raw_predictions = result.get("predictions", {}).get("predictions", [])
                filtered_predictions = [
                    p for p in raw_predictions
                    if float(p.get("confidence", 0)) >= conf_threshold
                ]
                annotated = draw_predictions(image_np_bgr, filtered_predictions)
                st.image(annotated, channels="BGR", use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Ringkasan Deteksi</div>', unsafe_allow_html=True)

        summary_df = summarize_predictions(filtered_predictions)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Bounding Box", len(filtered_predictions))
        with m2:
            st.metric("Jumlah Kelas", 0 if summary_df.empty else len(summary_df))
        with m3:
            dominant = "-" if summary_df.empty else str(summary_df.iloc[0]["Class"])
            st.metric("Kondisi Dominan", dominant)

        if summary_df.empty:
            st.warning("Tidak ada objek yang lolos confidence threshold.")
        else:
            st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Tabel Ringkasan</div>', unsafe_allow_html=True)
            st.dataframe(summary_df, use_container_width=True)

            detail_rows = []
            for i, pred in enumerate(filtered_predictions, start=1):
                detail_rows.append({
                    "No": i,
                    "Class": pred.get("class", "unknown"),
                    "Confidence": round(float(pred.get("confidence", 0)), 3),
                    "x": round(float(pred.get("x", 0)), 1),
                    "y": round(float(pred.get("y", 0)), 1),
                    "width": round(float(pred.get("width", 0)), 1),
                    "height": round(float(pred.get("height", 0)), 1),
                })

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="card-title">Detail Prediksi</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(detail_rows), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Terjadi error saat memproses gambar: {e}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

st.markdown('<div class="footer-tag">Built with Streamlit • Roboflow • Sorghum Field Vision</div>', unsafe_allow_html=True)
