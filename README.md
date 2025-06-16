# 🌐 Accessibility Analyzer

A simple and interactive web-based tool built with **Python**, **Streamlit**, and **Selenium** to evaluate the accessibility of websites using basic WCAG (Web Content Accessibility Guidelines) checks.


## 🧠 Features

- 🔍 Analyze any live website for basic accessibility issues
- 📸 Automatically captures a screenshot preview of the page
- 📊 Displays an accessibility score (out of 100)
- 🛠️ Provides grouped issues and fix suggestions
- ✅ Lists passed accessibility checks
- 🎨 Beautiful responsive UI with background image and stylized headings



## 🛠️ Tech Stack

- **Frontend & App Interface:** Streamlit  
- **Automation & Web Interaction:** Selenium WebDriver  
- **Screenshot Capture:** Headless Chrome  
- **Image Processing:** Pillow (PIL)  
- **Other:** Base64 encoding for background image, custom HTML/CSS styling



## 📸 UI Preview

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live--Demo-brightgreen?logo=streamlit)](https://accessibility-analyzer-gshlrpnmappekraaijaqhe7.streamlit.app/)



---

## 🚀 How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/accessibility-analyzer.git
   cd accessibility-analyzer
   Install Dependencies
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3.**Download ChromeDriver**
Make sure ChromeDriver version matches your installed Chrome version.
4.**Run the App**
  ```bash
streamlit run app.py

🔍 Example Accessibility Checks
| Check Type               | Description                                     |
| ------------------------ | ----------------------------------------------- |
| ❌ Missing Alt Text       | Detects `<img>` tags without `alt` attributes   |
| ⚠️ No Headings Found     | Checks for absence of `<h1>` to `<h6>`          |
| ❌ Missing `<title>` tag  | Checks if `<title>` exists in `<head>`          |
| ⚠️ Inputs Missing Labels | Detects form inputs without `label` or `aria-*` |


📦 Folder Structure
accessibility_analyzer_web/
│
├── app.py                   # Streamlit main app
├── analyzer.py              # Logic for scraping and analyzing
├── background.jpg           # Background image used in the UI
├── screenshot.png           # Saved preview screenshot
├── requirements.txt         # All Python dependencies
└── README.md                # This file


🙋‍♀️ Author
Amna Tariq
💼 Computer Engineering Student at UET Taxila
