import streamlit as st

st.set_page_config(page_title="Sorgum Drought Detector", page_icon="🌾", layout="wide")

st.markdown("# 🌾 Sorgum Drought Detector")
st.markdown("*Coming Soon - Aplikasi deteksi kekeringan sorgum*")
st.markdown("---")

st.info("🔧 Aplikasi sedang dalam tahap development. Fitur akan segera tersedia!")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Status", "Development")
with col2:
    st.metric("Version", "1.0.0")
with col3:
    st.metric("Model", "Roboflow")

st.markdown("### 📋 Fitur yang akan datang:")
st.markdown("""
- 📸 Upload dan analisis gambar
- 🤖 Deteksi kekeringan dengan AI
- 📊 Laporan analisis terperinci
- 🌾 Support berbagai jenis tanaman
""")
