import streamlit as st
import subprocess
import os
import uuid
import sys
from pathlib import Path
from datetime import datetime, timedelta
import shutil
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("CDISC_API_KEY")

st.set_page_config(page_title="CDISC CORE Validator", layout="wide")

# Add Update Cache button at the top-right
col1, col2 = st.columns([6, 1])
with col1:
    st.title("CDISC CORE Validator - Web GUI (Future-Proof)")
with col2:
    if st.button("🔄 Update Cache"):
        if not API_KEY:
            st.error("No API key found in .env file (CDISC_API_KEY).")
        else:
            cmd = [
                sys.executable, "cdisc-rules-engine/core.py", "update-cache",
                "--apikey", API_KEY,
                "--cache_path", "cdisc-rules-engine/resources/cache"
            ]
            st.write(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if result.returncode == 0:
                st.success("Cache updated successfully!")
                st.text(result.stdout)
            else:
                st.error("Cache update failed")
                st.text("STDOUT:\n" + result.stdout)
                st.text("STDERR:\n" + result.stderr)

# st.set_page_config(page_title="CDISC CORE Validator", layout="centered")
# st.title("CDISC CORE Validator - Web GUI (Future-Proof)")

# =======================
# Utility Functions
# =======================

def quote_if_needed(path: Path) -> str:
    """Quote path if it contains spaces."""
    p = str(path)
    return f'"{p}"' if " " in p else p

def clean_old_files(folder: Path, days_old: int = 7):
    """Delete files/folders older than given days."""
    now = datetime.now()
    cutoff = now - timedelta(days=days_old)
    if folder.exists():
        for item in folder.glob("*"):
            try:
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < cutoff:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            except Exception as e:
                print(f"Cleanup failed for {item}: {e}")

# =======================
# Setup Folders
# =======================
uploads_dir = Path("uploads")
results_dir = Path("results")
uploads_dir.mkdir(exist_ok=True)
results_dir.mkdir(exist_ok=True)
clean_old_files(uploads_dir)
clean_old_files(results_dir)

# =======================
# Streamlit Inputs
# =======================
uploaded_file = st.file_uploader("Upload SDTM Dataset (JSON/XPT)", type=["json", "xpt"])
standard = st.selectbox("Select Standard (-s)", ["sdtmig"])
version = st.selectbox("Select Version (-v)", ["3-4", "3-3", "3-2"])
output_format = st.selectbox("Select Output Format (-of)", ["XLSX", "JSON"])

# api_key = st.text_input("CDISC Library API Key (for Update Cache)", type="password")

# =======================
# Validate File
# =======================
if uploaded_file:
    # Save uploaded file
    unique_folder = uploads_dir / str(uuid.uuid4())
    unique_folder.mkdir(parents=True, exist_ok=True)
    temp_input = unique_folder / uploaded_file.name
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Validate"):
        output_dir = results_dir / f"{uuid.uuid4()}"
        output_dir.mkdir(parents=True, exist_ok=True)
        original_stem = Path(uploaded_file.name).stem
        output_file = output_dir / f"{original_stem}_result"

        # Build command
        cmd = [
            sys.executable, "cdisc-rules-engine/core.py", "validate",
            "-s", standard,
            "-v", version,
            "-rt", "cdisc-rules-engine/resources/templates/report-template.xlsx",
            "-dp", quote_if_needed(temp_input),
            "-of", output_format,
            "-o", quote_if_needed(output_file)
        ]


        st.write(f"Running: {' '.join(cmd)}")

        # Run validation
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)

        if result.returncode == 0:
            st.success("Validation completed!")
            for file in output_dir.glob("*"):
                st.download_button("Download Result", file.read_bytes(), file.name)
        else:
            st.error("Validation failed")
            st.text("STDOUT:\n" + result.stdout)
            st.text("STDERR:\n" + result.stderr)
