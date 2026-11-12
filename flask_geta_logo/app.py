import urllib.parse
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with the app
db.init_app(app)

# Create database tables if they don't exist yet
with app.app_context():
    db.create_all()


def extract_logo(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Search for shortcut icons or touch icons
        icon_tag = (
            soup.find("link", rel=lambda x: x and "icon" in x.lower())
            or soup.find("link", rel="apple-touch-icon")
            or soup.find("meta", property="og:image")
        )

        if icon_tag:
            href = icon_tag.get("href") or icon_tag.get("content")
            # Join relative paths with base URL
            return urllib.parse.urljoin(url, href)

        # 2. Fallback to standard root favicon if nothing is declared in HTML
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"

    except Exception:
        return None


@app.route("/", methods=["GET", "POST"])
def home():
    logo_url = None
    target_url = ""

    if request.method == "POST":
        target_url = request.form.get("url")
        if target_url:
            if not target_url.startswith(("http://", "https://")):
                target_url = "https://" + target_url
            logo_url = extract_logo(target_url)

    return render_template("index.html", logo_url=logo_url, target_url=target_url)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
