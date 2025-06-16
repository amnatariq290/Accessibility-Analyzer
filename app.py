import streamlit as st
from analyzer import analyze_url
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import base64

# ---------- Page Setup ----------
st.set_page_config(page_title="Accessibility Analyzer", layout="wide")

# ---------- Background Image ----------
def add_bg(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

add_bg("background.jpg")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    header, footer, .block-container {
        background: transparent !important;
    }

    .main-box {
        background-color: transparent;
        padding: 2.5rem;
        border-radius: 16px;
        max-width: 760px;
        margin: 60px auto;
        color: white;
        
    }

    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&display=swap');

    h1.custom-heading {
        font-family: 'Montserrat', sans-serif;
        font-size: 80px;
        line-height: 1.1;
        font-weight: 800;
        margin-bottom: 20px;
    }

    .stTextInput > div > div > input {
        padding: 0.6rem;
        font-size: 16px;
        border: 2px solid #ff4b4b;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
    }

    .stTextInput > div > div > input:focus {
        animation: pulseGlow 1.2s infinite;
        outline: none;
        box-shadow: 0 0 12px #ff4b4b, 0 0 24px #ff4b4b;
        transform: scale(1.03);
        border-color: #ffffff;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px #ff4b4b; }
        50% { box-shadow: 0 0 20px #ff4b4b; }
        100% { box-shadow: 0 0 10px #ff4b4b; }
    }

    .stButton button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        transition: all 0.2s;
    }

    .stButton button:hover {
        background-color: #d63636;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Screenshot Capture ----------
def capture_screenshot(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1200x800")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        screenshot_path = "screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return screenshot_path
    except Exception as e:
        st.warning(f"Screenshot Error: {e}")
        return None

# ---------- Main Interface ----------
with st.container():
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.markdown("<h1 class='custom-heading'>Accessibility<br>Analyzer</h1>", unsafe_allow_html=True)
    st.write("🔗 **Paste your website URL below to analyze basic accessibility issues**:")

    url = st.text_input("Enter Website URL", placeholder="https://example.com")

    if st.button("Analyze"):
        if url and url.startswith("http"):
            with st.spinner("🔎 Analyzing..."):
                issues = analyze_url(url)

            # Screenshot Section
            screenshot_path = capture_screenshot(url)
            if screenshot_path and os.path.exists(screenshot_path):
                st.markdown("### 📸 Website Preview")
                image = Image.open(screenshot_path)
                st.image(image, use_column_width=True)

            # Score Calculation
            total_check_types = 4
            failed_checks = len(set([i["type"] for i in issues]))
            score = max(0, round(((total_check_types - failed_checks) / total_check_types) * 100))
            st.markdown(f"### 📊 Accessibility Score: `{score}%`")
            st.progress(score)

            st.info("ℹ️ This is a basic analyzer. For full WCAG compliance, use tools like [WAVE](https://wave.webaim.org/) or [axe](https://www.deque.com/axe/).")

            # Issues Grouped
            if issues:
                st.subheader("🔍 Issues Found (Grouped):")
                grouped = {}
                for issue in issues:
                    grouped.setdefault(issue["type"], []).append(issue["element"])

                for idx, (issue_type, elements) in enumerate(grouped.items(), 1):
                    st.markdown(f"**{idx}. {issue_type}**")
                    for el in elements:
                        st.code(el, language='html')

                # Fixing Tips
                st.subheader("🛠️ Tips for Fixing Issues")
                tips = {
                    "❌ Missing Alt Text": "Add descriptive `alt` attributes to all `<img>` tags.",
                    "⚠️ No Headings Found": "Use proper `<h1>` to `<h6>` headings to structure content.",
                    "❌ Missing <title>": "Include a meaningful `<title>` tag inside `<head>`.",
                    "⚠️ Form Input Missing Label": "Add `<label for='id'>` or `aria-label` for every input field."
                }
                for issue_type, tip in tips.items():
                    st.markdown(f"**{issue_type}**: {tip}")
            else:
                st.success("✅ No basic accessibility issues found!")

            # Passed Checks
            st.subheader("✅ Passed Checks")
            found_types = [i["type"] for i in issues]
            passed_checks = []

            if "Missing Alt Text" not in found_types:
                passed_checks.append("✅ All images have `alt` text.")
            if "No Headings Found" not in found_types:
                passed_checks.append("✅ Proper headings (`<h1>` to `<h6>`) found.")
            if "Missing <title>" not in found_types:
                passed_checks.append("✅ Page has a valid `<title>` tag.")
            if "Form Input Missing Label" not in found_types:
                passed_checks.append("✅ All form inputs have labels or `aria-labels`.")

            for check in passed_checks:
                st.markdown(check)
        else:
            st.warning("⚠️ Please enter a valid URL starting with http or https.")

    st.markdown("</div>", unsafe_allow_html=True)
