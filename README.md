# 🌾 Sorgum Drought Detector

Aplikasi AI untuk deteksi kekeringan pada daun sorgum menggunakan Roboflow dan Streamlit.

## 🎯 Fitur

- ✅ Deteksi kekeringan real-time menggunakan AI
- ✅ Upload gambar atau gunakan URL
- ✅ Analisis tingkat keparahan kekeringan
- ✅ Confidence score dan visualisasi hasil
- ✅ Interface user-friendly dengan Streamlit

## 📋 Persyaratan

- Python 3.8+
- Git

## 🚀 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/lishanurcahyani-sketch/Sorgum-Drought-Detector.git
cd Sorgum-Drought-Detector
```

### 2. Buat Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy file example
cp .env.example .env

# Edit .env dan masukkan kredensial Anda
# ROBOFLOW_API_KEY=your_api_key_here
```

### 5. Jalankan Aplikasi
```bash
streamlit run app/app.py
```

Aplikasi akan terbuka di `http://localhost:8501`

## 📖 Cara Penggunaan

1. **Upload Gambar**: Pilih gambar daun sorgum dari komputer Anda
2. **Tunggu Analisis**: Aplikasi akan memproses gambar dengan model AI
3. **Lihat Hasil**: Tingkat keparahan, confidence score, dan area deteksi akan ditampilkan
4. **Ambil Keputusan**: Gunakan hasil untuk menentukan tindakan irigasi

## 🏗️ Struktur Folder

```
Sorgum-Drought-Detector/
├── app/
│   └── app.py                 # Main Streamlit application
├── utils/
│   └── roboflow_utils.py      # Roboflow integration utilities
├── models/
│   └── .gitkeep
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions workflow
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration settings
├── .env.example               # Environment variables template
├── .gitignore
└── README.md
```

## 🔧 Konfigurasi

### Environment Variables (.env)

```env
# Roboflow API
ROBOFLOW_API_KEY=your_api_key
ROBOFLOW_WORKSPACE=your_workspace
ROBOFLOW_PROJECT=drought_on_sorghum_leaves
ROBOFLOW_MODEL_VERSION=4

# App Settings
STREAMLIT_PAGE_TITLE=Sorgum Drought Detector
MAX_FILE_SIZE=200
CONFIDENCE_THRESHOLD=0.5
```

## 🧠 Model Information

- **Workspace**: lishanurcahyani-sketch
- **Project**: drought_on_sorghum_leaves
- **Version**: 4
- **Framework**: Roboflow
- **Type**: Object Detection

## 📚 Dependencies

- **streamlit**: Web framework untuk ML apps
- **roboflow**: Akses ke model ML
- **opencv-python**: Computer vision operations
- **numpy**: Numerical computations
- **pillow**: Image processing
- **python-dotenv**: Environment variable management

## 🌐 Deployment

### Deploy ke Streamlit Cloud

1. Push repository ke GitHub
2. Buka https://share.streamlit.io
3. Login dengan GitHub account Anda
4. Klik "New app"
5. Pilih repository: `Sorgum-Drought-Detector`
6. Branch: `main`
7. Main file path: `app/app.py`
8. Klik "Deploy"



## 👥 Kontribusi

Kontribusi sangat diterima! Silakan:
1. Fork repository ini
2. Buat branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📧 Kontak

- GitHub: [@lishanurcahyani-sketch](https://github.com/lishanurcahyani-sketch)

---

**Made with Indofood Riset Nugraha Support using Roboflow & Streamlit**# Sorgum-Drought-Detector
AI-powered drought detection system for sorghum leaves using Roboflow and Streamlit
