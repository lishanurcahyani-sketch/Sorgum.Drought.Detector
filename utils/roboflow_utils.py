import os
import cv2
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str, default=None):
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


ROBOFLOW_API_KEY = get_secret("ROBOFLOW_API_KEY")
ROBOFLOW_WORKSPACE = get_secret("ROBOFLOW_WORKSPACE", "sorghumdrought")
ROBOFLOW_PROJECT = get_secret("ROBOFLOW_PROJECT", "drought_on_sorghum_leaves")
ROBOFLOW_MODEL_VERSION = get_secret("ROBOFLOW_MODEL_VERSION", "4")


def predict_image(image_path: str):
    try:
        if not ROBOFLOW_API_KEY:
            return {"success": False, "error": "ROBOFLOW_API_KEY belum diset."}

        url = f"https://detect.roboflow.com/{ROBOFLOW_PROJECT}/{ROBOFLOW_MODEL_VERSION}"

        with open(image_path, "rb") as image_file:
            response = requests.post(
                url,
                params={"api_key": ROBOFLOW_API_KEY},
                files={"file": image_file},
                timeout=60
            )

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }

        return {
            "success": True,
            "predictions": response.json()
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def class_color_bgr(class_name: str):
    name = class_name.strip().lower()

    if name in ["daun segar", "healthy", "segar"]:
        return (0, 255, 0)
    if name in ["kekeringan ringan", "light drought", "drought ringan"]:
        return (0, 255, 255)
    if name in ["kekeringan berat", "severe drought", "drought berat"]:
        return (0, 0, 255)

    return (255, 0, 0)


def draw_predictions(image_bgr, predictions):
    annotated = image_bgr.copy()

    for pred in predictions:
        x = pred.get("x", 0)
        y = pred.get("y", 0)
        w = pred.get("width", 0)
        h = pred.get("height", 0)
        cls = pred.get("class", "unknown")
        conf = float(pred.get("confidence", 0))

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        color = class_color_bgr(cls)

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)

        label = f"{cls} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 2)

        y_label_top = max(y1 - th - 12, 0)
        y_label_bottom = max(y1, th + 12)

        cv2.rectangle(
            annotated,
            (x1, y_label_top),
            (x1 + tw + 10, y_label_bottom),
            color,
            -1
        )

        cv2.putText(
            annotated,
            label,
            (x1 + 5, y_label_bottom - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

    return annotated


def summarize_predictions(predictions):
    if not predictions:
        return pd.DataFrame(columns=["Class", "Confidence", "Count"])

    summary = {}

    for pred in predictions:
        cls = pred.get("class", "unknown")
        conf = float(pred.get("confidence", 0))

        if cls not in summary:
            summary[cls] = {
                "Class": cls,
                "Confidence": conf,
                "Count": 1
            }
        else:
            summary[cls]["Count"] += 1
            summary[cls]["Confidence"] = max(summary[cls]["Confidence"], conf)

    df = pd.DataFrame(summary.values())
    df["Confidence"] = df["Confidence"].round(3)
    df = df.sort_values(by=["Count", "Confidence"], ascending=[False, False]).reset_index(drop=True)
    return df
