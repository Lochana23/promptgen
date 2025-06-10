# prompt_generator_app.py

import streamlit as st
import requests
from fpdf import FPDF
import time

# CONFIGURATION
GEMINI_API_KEY = "AIzaSyBUjbvHg9nj8l3Fzeb6pL2wcaEv5eRObwY"
MODEL_NAME = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to call Gemini API
def call_gemini_api(topic, style, use_case):
    prompt_text = (
        f"Generate a high-quality AI prompt based on the following details:\n\n"
        f"Topic/Context: {topic}\n"
        f"Prompt Style: {style}\n"
        f"Target Use-case: {use_case}\n\n"
        f"The result should be a ready-to-use AI prompt."
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }
    
    response = requests.post(GEMINI_API_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    
    generated_prompt = data['candidates'][0]['content']['parts'][0]['text']
    return generated_prompt

# Function to save prompt as PDF
def save_prompt_as_pdf(prompt_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in prompt_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    filename = f"generated_prompt_{int(time.time())}.pdf"
    pdf.output(filename)
    return filename

# STREAMLIT APP
st.set_page_config(page_title="Prompt Generator App", layout="centered")

st.title("📝 Prompt Generator using Gemini API")
st.write("Generate optimized AI prompts for various use-cases.")

# User input
topic_input = st.text_area("Enter your topic, goal, or context:", placeholder="e.g. Prompt for generating marketing copy")

style_option = st.selectbox("Select Prompt Style:", [
    "Creative", "Instructional", "Descriptive", "Conversational", "Storytelling", "Analytical"
])

use_case_option = st.selectbox("Select Target Use-case:", [
    "Image Generation", "Email Writing", "Coding", "Marketing", "Education", "Social Media", "Business Analysis", "Customer Support", "Gaming", "Other"
])

# Buttons
col1, col2 = st.columns(2)
generate_clicked = col1.button("🚀 Generate Prompt")
regenerate_clicked = col2.button("🔄 Regenerate Prompt")

# Generate prompt
if (generate_clicked or regenerate_clicked) and topic_input.strip() != "":
    with st.spinner("Generating your prompt..."):
        try:
            prompt_output = call_gemini_api(topic_input, style_option, use_case_option)
            
            # Save to history
            st.session_state.history.append({
                "topic": topic_input,
                "style": style_option,
                "use_case": use_case_option,
                "prompt": prompt_output
            })
            
            # Display result
            st.subheader("🎁 Generated Prompt:")
            st.code(prompt_output, language="markdown")
            
            # Download PDF
            pdf_filename = save_prompt_as_pdf(prompt_output)
            with open(pdf_filename, "rb") as f:
                st.download_button(
                    label="📥 Download as PDF",
                    data=f,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
        
        except Exception as e:
            st.error(f"Error generating prompt: {e}")

# History view
if len(st.session_state.history) > 0:
    st.markdown("---")
    st.subheader("🕘 Previous Prompt Versions:")
    for idx, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Version {len(st.session_state.history) - idx}"):
            st.write(f"**Topic/Context:** {item['topic']}")
            st.write(f"**Prompt Style:** {item['style']}")
            st.write(f"**Target Use-case:** {item['use_case']}")
            st.code(item['prompt'], language="markdown")

# Footer
st.markdown("---")
st.write("© 2025 Prompt Generator App • Built with ❤️ using Streamlit & Gemini API")
