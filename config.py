import os
from dotenv import load_dotenv

load_dotenv()

# Roboflow Configuration
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY", "rf_FwwkOW2utJUXL7TuLflGWQtUO183")
ROBOFLOW_WORKSPACE = os.getenv("ROBOFLOW_WORKSPACE", "lishanurcahyani-sketch")
ROBOFLOW_PROJECT = os.getenv("ROBOFLOW_PROJECT", "drought_on_sorghum_leaves")
ROBOFLOW_MODEL_VERSION = os.getenv("drought_on_sorghum_leaves/4")

# Streamlit Configuration
STREAMLIT_PAGE_TITLE = "Sorgum Drought Detector"
STREAMLIT_PAGE_ICON = "🌾"
STREAMLIT_LAYOUT = "wide"

# App Configuration
MAX_FILE_SIZE = 200  # MB
CONFIDENCE_THRESHOLD = 0.5
