import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import sys
import requests

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.roboflow_utils import DroughtDetector
from config import (
    STREAMLIT_PAGE_TITLE,
    STREAMLIT_PAGE_ICON,
    STREAMLIT_LAYOUT,
    MAX_FILE_SIZE
)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon=STREAMLIT_PAGE_ICON,
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .severity-high {
        color: #ff4444;
        font-weight: bold;
    }
    .severity-medium {
        color: #ff9500;
        font-weight: bold;
    }
    .severity-low {
        color: #44b700;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE SESSION STATE ====================
if 'detector' not in st.session_state:
    st.session_state.detector = DroughtDetector()

if 'detection_results' not in st.session_state:
    st.session_state.detection_results = None

# ==================== HEADER ====================
st.markdown("# 🌾 Sorgum Drought Detector")
st.markdown("*Sistem deteksi kekeringan pada daun sorgum menggunakan AI*")
st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Konfigurasi")
    
    st.markdown("### 📊 Tentang Aplikasi")
    st.info("""
    **Sorgum Drought Detector** adalah aplikasi yang menggunakan 
    teknologi **Computer Vision** dan **Machine Learning** untuk 
    mendeteksi tingkat kekeringan pada daun tanaman sorgum.
    
    **Model**: Roboflow Drought Detection
    **Version**: 4
    """)
    
    st.markdown("### 🔧 Opsi Deteksi")
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Minimum confidence untuk deteksi yang dihitung sebagai positif"
    )

# ==================== MAIN CONTENT ====================
tab1, tab2, tab3 = st.tabs(["📸 Analisis Gambar", "📚 Panduan", "ℹ️ Tentang"])

# ==================== TAB 1: IMAGE ANALYSIS ====================
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Pilih Sumber Gambar")
        upload_option = st.radio(
            "Pilih metode input:",
            ["Upload File", "URL Gambar"],
            label_visibility="collapsed"
        )
        
        uploaded_file = None
        image_url = None
        
        if upload_option == "Upload File":
            uploaded_file = st.file_uploader(
                "Unggah gambar daun sorgum",
                type=["jpg", "jpeg", "png", "bmp"],
                help=f"Ukuran maksimal: {MAX_FILE_SIZE}MB"
            )
        else:
            image_url = st.text_input(
                "Masukkan URL gambar:",
                placeholder="https://example.com/image.jpg"
            )
    
    # ==================== PROCESS IMAGE ====================
    if uploaded_file is not None or image_url:
        try:
            # Load image
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                image_input = uploaded_file
                st.session_state.image_name = uploaded_file.name
            else:
                image = Image.open(requests.get(image_url, stream=True).raw)
                image_input = image_url
                st.session_state.image_name = "URL Image"
            
            # Display original image
            with col2:
                st.markdown("### 📷 Gambar Original")
                st.image(image, use_column_width=True)
            
            # Run detection
            with st.spinner("🔍 Menganalisis gambar..."):
                if isinstance(image_input, str):  # URL
                    results = st.session_state.detector.predict(image_url)
                else:  # File
                    # Save temporarily
                    temp_path = f"/tmp/{uploaded_file.name}"
                    os.makedirs("/tmp", exist_ok=True)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    results = st.session_state.detector.predict(temp_path)
                    os.remove(temp_path)
            
            st.session_state.detection_results = results
            
            # ==================== DISPLAY RESULTS ====================
            if results['success']:
                st.success("✅ Analisis selesai!")
                
                # Get severity analysis
                severity_data = st.session_state.detector.detect_drought_severity(results)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 📊 Tingkat Keparahan")
                    severity = severity_data['severity']
                    if severity == "Parah":
                        st.markdown(f"<p class='severity-high'>{severity}</p>", 
                                  unsafe_allow_html=True)
                    elif severity == "Sedang":
                        st.markdown(f"<p class='severity-medium'>{severity}</p>", 
                                  unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='severity-low'>{severity}</p>", 
                                  unsafe_allow_html=True)
                
                with col2:
                    st.metric(
                        "Confidence Score",
                        f"{severity_data['confidence']:.1f}%"
                    )
                
                with col3:
                    st.metric(
                        "Deteksi Area",
                        severity_data['detection_count']
                    )
                
                # Detailed results
                st.markdown("### 📈 Detail Hasil")
                st.info(severity_data['message'])
                
                # Raw predictions
                with st.expander("🔬 Detail Teknis (Raw Predictions)"):
                    st.json(results['predictions'])
            else:
                st.error(f"❌ Error: {results['error']}")
        
        except Exception as e:
            st.error(f"❌ Error memproses gambar: {str(e)}")

# ==================== TAB 2: PANDUAN ====================
with tab2:
    st.markdown("## 📚 Panduan Penggunaan")
    
    st.markdown("""
    ### 1️⃣ Persiapan Gambar
    - Ambil foto daun sorgum dengan pencahayaan yang baik
    - Gunakan background yang kontras
    - Pastikan fokus pada area yang ingin dianalisis
    - Ukuran file maksimal 200MB
    
    ### 2️⃣ Upload Gambar
    - Pilih metode: Upload File atau URL Gambar
    - Klik tombol "Browse Files" untuk upload
    - Atau masukkan URL gambar dari internet
    
    ### 3️⃣ Analisis
    - Aplikasi akan secara otomatis menganalisis gambar
    - Proses dapat memakan waktu 10-30 detik
    - Hasil akan ditampilkan dengan visualisasi
    
    ### 4️⃣ Interpretasi Hasil
    - **Tingkat Keparahan**: Ringan, Sedang, atau Parah
    - **Confidence Score**: Tingkat kepercayaan deteksi (0-100%)
    - **Deteksi Area**: Jumlah area dengan potensi kekeringan
    """)
    
    st.markdown("---")
    st.markdown("""
    ### 🔍 Interpretasi Hasil Deteksi
    
    | Tingkat | Deskripsi | Aksi Rekomendasi |
    |---------|-----------|-----------------|
    | **Sehat** | Tidak ada tanda kekeringan | Monitor secara berkala |
    | **Ringan** | Awal tanda kekeringan | Perhatikan pola irigasi |
    | **Sedang** | Kekeringan terlihat jelas | Tingkatkan frekuensi irigasi |
    | **Parah** | Kekeringan serius | Tindakan mendesak diperlukan |
    """)

# ==================== TAB 3: TENTANG ====================
with tab3:
    st.markdown("## ℹ️ Tentang Aplikasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ Teknologi
        - **Frontend**: Streamlit
        - **Backend**: Python
        - **ML Model**: Roboflow
        - **Computer Vision**: OpenCV
        
        ### 📚 Library
        - streamlit
        - roboflow
        - opencv-python
        - numpy
        - pillow
        """)
    
    with col2:
        st.markdown("""
        ### 👨‍💻 Developer
        - **Author**: Lisha Nur Cahyani
        - **GitHub**: [@lishanurcahyani-sketch](https://github.com/lishanurcahyani-sketch)
        
        ### 🔗 Link Penting
        - [Repository GitHub](https://github.com/lishanurcahyani-sketch/Sorgum-Drought-Detector)
        - [Roboflow](https://roboflow.com)
        - [Streamlit Docs](https://docs.streamlit.io)
        """)
    
    st.markdown("---")
    st.info("**Versi**: 1.0.0 | **Update**: 2026")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌾 Sorgum Drought Detector © 2026 | Powered by Roboflow & Streamlit</p>
</div>
""", unsafe_allow_html=True)
