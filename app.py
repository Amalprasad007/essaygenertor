import streamlit as st
import requests
import time

# Your API key
API_KEY = "AIzaSyAP91kWKUZqHzJqDaAz7B18QOIPCeHvCSQ"

# Google Gemini API URL
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

# Function to call the Google Gemini API to generate an essay
def generate_essay(keyword):
    headers = {
        "Content-Type": "application/json"
    }
    prompt = f"Write an essay about {keyword}."
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        content = response.json()
        essay = content.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error: No content generated.")
        return essay
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI Enhancements
st.set_page_config(page_title="Essay Generator", page_icon="📝", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 3em;'>📝 Essay Generator</h1>", unsafe_allow_html=True)

# Sidebar Input Section
st.sidebar.markdown("Enter the details below to generate your essay:")

# Sidebar styling
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f0f0f5;
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content h1 {
            color: #2E8B57;
        }
        .sidebar .sidebar-content input {
            border: 1px solid #2E8B57;
        }
        .sidebar .sidebar-content button {
            background-color: #2E8B57;
            color: white;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Input for keyword with placeholder and tooltip
keyword = st.sidebar.text_input("Keyword/Topic:", placeholder="Enter a keyword or topic here...", help="Enter the main idea for the essay.")

# Button to generate the essay with minimal animation
generate_button = st.sidebar.button("Generate Essay", help="Click to generate the essay based on the provided keyword.")

# Adding a separator for better layout
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

# Displaying the generated essay in a text area with custom styling
if generate_button:
    if keyword:
        with st.spinner("Generating essay..."):
            time.sleep(1)  # Minimal delay for better UX
            essay = generate_essay(keyword)
            st.markdown("<h2 style='color: #2E8B57; font-size: 2.5em;'>Generated Essay</h2>", unsafe_allow_html=True)
            st.text_area(label="", value=essay, height=400, max_chars=None)
            st.markdown(f"<p style='text-align: right; color: gray;'>Character Count: {len(essay)}</p>", unsafe_allow_html=True)
            
            # Download button for the essay
            st.download_button(label="Download Essay", data=essay, file_name="generated_essay.txt", mime="text/plain")
    else:
        st.sidebar.error("Please enter a keyword or topic.")

# Simple footer with attribution
st.markdown("""
    <footer style='text-align: center; color: gray; margin-top: 50px;'>
        Created by Amal Prasad
    </footer>
""", unsafe_allow_html=True)
