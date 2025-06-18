import streamlit as st
import requests
import base64
from dotenv import load_dotenv
from datetime import datetime

# Page config
st.set_page_config(page_title="AI Image Generator", layout="centered", page_icon="🎨")

# Load API key from .env
load_dotenv()
API_TOKEN = st.secrets["HUGGINGFACE_API_KEY"]
# Model configuration
MODEL = "black-forest-labs/FLUX.1-dev"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Sidebar settings
with st.sidebar:
    st.title("⚙️ Settings")
    guidance_scale = st.slider("🎚️ Creativity (Guidance Scale)", 1.0, 20.0, 7.5, 0.5)
    height = st.number_input("📐 Image Height (px)", min_value=256, max_value=1024, value=512, step=64)
    width = st.number_input("📏 Image Width (px)", min_value=256, max_value=1024, value=512, step=64)
    dark_mode = st.toggle("🌙 Dark Mode", value=False)
    st.markdown("---")
    st.info("Try prompts like:\n- A futuristic cyberpunk city\n- A dreamy watercolor landscape\n- A cute robot in space")

# Apply dark mode
if dark_mode:
    st.markdown("""
        <style>
        html, body, [data-testid="stApp"] {
            background-color: #0e1117;
            color: #ffffff;
        }
        .st-emotion-cache-18ni7ap {
            background-color: #0e1117;
        }
        .st-emotion-cache-1v0mbdj, .st-emotion-cache-1xw8zd0, .st-emotion-cache-16txtl3, .stTextInput input, .stNumberInput input {
            background-color: #1c1e23;
            color: #ffffff;
        }
        .st-emotion-cache-19rxjzo {
            background-color: #0e1117 !important;
        }
        .stButton>button {
            background-color: #1f2229;
            color: white;
            border: 1px solid #3a3a3a;
        }
        .stButton>button:hover {
            background-color: #31343f;
            color: white;
        }
        .stRadio > div {
            background-color: #1c1e23;
            color: white;
            border-radius: 8px;
        }
        .css-1offfwp {
            color: white !important;
        }
        .stMarkdown a {
            color: #8ab4f8;
        }
        </style>
    """, unsafe_allow_html=True)

# Main UI
st.title("🎨 Free AI Image Generator")
st.caption("Generate high-quality images with AI. Powered by Hugging Face ✨")

prompt = st.text_input("📝 Your Prompt", placeholder="Describe the image you want...")
image_format = st.radio("📁 Download Format", ["PNG", "JPG"], horizontal=True)

# Generate button
if st.button("🚀 Generate Image"):
    if not API_TOKEN:
        st.error("❌ API key missing! Please add 'HUGGINGFACE_API_KEY' in your .env file.")
    elif not prompt.strip():
        st.warning("⚠️ Please enter a valid prompt.")
    else:
        with st.spinner("⌛ Generating image... Please wait..."):
            try:
                payload = {
                    "inputs": prompt,
                    "options": {"guidance_scale": guidance_scale},
                    "parameters": {"height": height, "width": width}
                }
                response = requests.post(API_URL, headers=HEADERS, json=payload)

                if response.status_code == 200:
                    image_bytes = response.content
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    ext = "png" if image_format == "PNG" else "jpg"
                    filename = f"ai_image_{timestamp}.{ext}"

                    st.image(image_bytes, caption="✅ Generated Image", width=400)
                    b64 = base64.b64encode(image_bytes).decode()
                    download_link = f'<a href="data:file/{ext};base64,{b64}" download="{filename}">📥 Download {ext.upper()} Image</a>'
                    st.markdown(download_link, unsafe_allow_html=True)

                elif response.status_code == 503:
                    st.warning("⏳ Model is still loading. Please wait a moment and try again.")
                elif response.status_code == 403:
                    st.error("🔒 You may need to accept the models license or use a different model.")
                else:
                    st.error(f"❌ Failed to generate image (Status {response.status_code})")
                    st.code(response.text)

            except Exception as e:
                st.error("🚫 An error occurred during image generation.")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("Made by ❤️ Siddiqa Badar")
