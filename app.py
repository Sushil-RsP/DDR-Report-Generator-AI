
import streamlit as st
from utils import extract_text, extract_images, combine_texts
from prompts import generate_prompt
from groq import Groq
import os
from dotenv import load_dotenv
import time
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure page
st.set_page_config(
    page_title="DDR Report Generator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .success-box {
        background-color: #D4EDDA;
        border: 2px solid #28A745;
        padding: 1em;
        border-radius: 5px;
        margin: 1em 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 2px solid #FFC107;
        padding: 1em;
        border-radius: 5px;
        margin: 1em 0;
    }
    .info-box {
        background-color: #D1ECF1;
        border: 2px solid #17A2B8;
        padding: 1em;
        border-radius: 5px;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

if 'generated_report' not in st.session_state:
    st.session_state.generated_report = None
if 'extracted_images' not in st.session_state:
    st.session_state.extracted_images = []

def check_api_key():
    """Verify API key is properly configured."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key == "your_groq_api_key_here":
        return False
    
    return True

st.markdown('<h1 class="main-title">🏠 DDR Report Generator AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.1em; color: #666;">Generate professional Detailed Diagnostic Reports from PDF documents</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key status
    if check_api_key():
        st.success("🔐 API Key Configured (Groq)")
    else:
        st.error("🔓 API Key Not Configured")
        st.markdown("""
        **Setup Required:**
        1. Get FREE API key from [Groq Console](https://console.groq.com/keys)
        2. Create/edit `.env` file in project folder
        3. Add: `GROQ_API_KEY=your_key_here`
        4. Restart app
        """)
    
    st.divider()
    
    st.subheader("📋 Instructions")
    st.markdown("""
    1. **Upload PDFs**: Upload inspection and thermal reports
    2. **Generate**: Click button to create DDR
    3. **Review**: Check generated report
    4. **Extract**: Get images from PDFs
    5. **Download**: Copy report text
    """)

if not check_api_key():
    st.error("❌ Configuration Required - Please set up your API key (see sidebar)")
    st.stop()

def query_groq(prompt):
    """Send query to Groq Inference API."""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        
        return message.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"Groq API Error: {str(e)}")

try:
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        st.error("API key not configured")
        st.stop()
except Exception as e:
    st.error(f"Error configuring API: {str(e)}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Inspection Report")
    inspection_file = st.file_uploader("Upload Inspection PDF", type=["pdf"], key="inspection")

with col2:
    st.subheader("🌡️ Thermal Report")
    thermal_file = st.file_uploader("Upload Thermal PDF", type=["pdf"], key="thermal")

st.divider()

st.subheader("🚀 Generate DDR Report")

col1, col2, col3 = st.columns(3)

with col1:
    generate_button = st.button("📋 Generate Report", use_container_width=True)

with col2:
    extract_images_button = st.button("🖼️ Extract Images", use_container_width=True)

with col3:
    clear_button = st.button("🗑️ Clear All", use_container_width=True)

# Process generate report
if generate_button:
    if not inspection_file or not thermal_file:
        st.warning("⚠️ Please upload both inspection and thermal PDFs")
    else:
        # Create progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Extract text
            status_text.info("📖 Extracting text from inspection report...")
            progress_bar.progress(20)
            inspection_text = extract_text(inspection_file)
            
            status_text.info("📖 Extracting text from thermal report...")
            progress_bar.progress(40)
            thermal_text = extract_text(thermal_file)
            
            # Combine
            status_text.info("🔗 Combining documents...")
            progress_bar.progress(60)
            combined_text = combine_texts(inspection_text, thermal_text)
            
            prompt = generate_prompt(combined_text)
            
            # Send to Groq
            status_text.info("🧠 Generating report with Groq LLaMA 3.3 70B (this may take 10-30 seconds)...")
            progress_bar.progress(80)
            
            report = query_groq(prompt)
            
            st.session_state.generated_report = report
            
            progress_bar.progress(100)
            status_text.success("✅ Report Generated Successfully!")
            time.sleep(1)
            status_text.empty()
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            progress_bar.empty()
            status_text.empty()

# Process extract images
if extract_images_button:
    if not inspection_file and not thermal_file:
        st.warning("⚠️ Please upload at least one PDF")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            images = []
            
            if inspection_file:
                status_text.info("🖼️ Extracting images from inspection report...")
                progress_bar.progress(25)
                inspection_file.seek(0)
                images.extend(extract_images(inspection_file, "images/inspection"))
            
            if thermal_file:
                status_text.info("🖼️ Extracting images from thermal report...")
                progress_bar.progress(75)
                thermal_file.seek(0)
                images.extend(extract_images(thermal_file, "images/thermal"))
            
            st.session_state.extracted_images = images
            
            progress_bar.progress(100)
            status_text.success(f"✅ Extracted {len(images)} images!")
            time.sleep(1)
            status_text.empty()
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"❌ Error extracting images: {str(e)}")
            progress_bar.empty()
            status_text.empty()

# Clear session
if clear_button:
    st.session_state.generated_report = None
    st.session_state.extracted_images = []
    st.success("✅ Cleared all data")
    time.sleep(1)
    st.rerun()

st.divider()

# Display generated report
if st.session_state.generated_report:
    st.subheader("📊 Generated DDR Report")
    
    # Display report
    #with st.container(border=True):
    with st.container():
        st.markdown(st.session_state.generated_report)
    
    # Copy button and download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📥 Download as Text",
            data=st.session_state.generated_report,
            file_name="DDR_Report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📋 Copy to Clipboard",
            data=st.session_state.generated_report,
            file_name="DDR_Report.txt",
            mime="text/plain",
            use_container_width=True,
            help="Copy generated report"
        )
    
    with col3:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.session_state.generated_report = None
            st.rerun()

# Display extracted images
if st.session_state.extracted_images:
    st.subheader("📸 Extracted Images")
    
    cols = st.columns(3)
    
    for idx, img_path in enumerate(st.session_state.extracted_images):
        col_idx = idx % 3
        
        with cols[col_idx]:
            try:
                #st.image(img_path, use_container_width=True, caption=os.path.basename(img_path))
                st.image(img_path, width=300, caption=os.path.basename(img_path))
            except Exception as e:
                st.error(f"Error displaying image: {str(e)}")
