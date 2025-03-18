import os
import streamlit as st
import time
from pdf_extractor import process_directory

# Ensure temp_uploads directory exists
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="Pre-Consult Notes", layout="wide")

st.title("Pre-Consult Notes")
st.markdown("### Upload your files for processing and generating consultation notes.")

# File Upload Section
st.header("📂 Upload Files")
pdf_files = st.file_uploader("Upload Medical Reports (PDF)", type=["pdf"], accept_multiple_files=True)

if st.button("📌 Generate Report"):
    if not pdf_files:
        st.warning("⚠️ Please upload at least one PDF file to proceed!")
    else:
        with st.spinner("⏳ Processing files... Please wait."):

            saved_file_paths = []
            for pdf_file in pdf_files:
                save_path = os.path.join(UPLOAD_DIR, pdf_file.name)

                # Save file locally
                with open(save_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                saved_file_paths.append(save_path)

            # Process PDFs
            prompt_path = "prompt.txt"
            pdf_metadata = process_directory(prompt_path, saved_file_paths)

            if pdf_metadata:
                st.write(pdf_metadata)
            else:
                st.error("❌ Failed to generate report. Please check the logs.")