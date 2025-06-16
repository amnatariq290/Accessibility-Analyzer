import requests
from bs4 import BeautifulSoup

def analyze_url(url):
    issues = []

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Missing Alt Text
        for img in soup.find_all('img'):
            if not img.get('alt'):
                issues.append({
                    "type": "❌ Missing Alt Text",
                    "element": str(img).strip()
                })

        # 2. No Headings
        headings = sum(len(soup.find_all(f'h{i}')) for i in range(1, 7))
        if headings == 0:
            issues.append({
                "type": "⚠️ No Headings Found",
                "element": "<h1> to <h6> not found"
            })

        # 3. Missing Page Title
        if not soup.title or not soup.title.string.strip():
            issues.append({
                "type": "❌ Missing <title>",
                "element": "<title> tag missing or empty"
            })

        # 4. Form elements without labels
        for form in soup.find_all('form'):
            inputs = form.find_all(['input', 'select', 'textarea'])
            for input_tag in inputs:
                label = form.find('label', attrs={"for": input_tag.get('id')})
                if not label and not input_tag.get('aria-label'):
                    issues.append({
                        "type": "⚠️ Form Input Missing Label",
                        "element": str(input_tag).strip()
                    })

    except Exception as e:
        issues.append({
            "type": "🚫 Error",
            "element": str(e)
        })

    return issues
