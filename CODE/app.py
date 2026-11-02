import urllib.parse
import requests
from bs4 import BeautifulSoup
from flask import redirect, render_template, request, url_for, Flask
from templates.models import URLmodal, db 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()
def extract_logo(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        icon_tag = (
            soup.find("link", rel=lambda x: x and "icon" in x.lower())
            or soup.find("link", rel="apple-touch-icon")
            or soup.find("meta", property="og:image")
        )
        if icon_tag:
            href = icon_tag.get("href") or icon_tag.get("content")
            return urllib.parse.urljoin(url, href)
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
    except Exception:
        return None  
@app.route("/", methods=["GET", "POST"])
def index():
    getnerateQR_result = None
    logo_url = None
    target_url = ""
    if request.method == "POST":
        if request.form.get("form_type") == "add_site":
            site_url = request.form.get("site_url")
            site_name = request.form.get("site_name")
            if site_url and site_name:
                target_url = site_url
                if not target_url.startswith(("http://", "https://")):
                    target_url = "https://" + target_url
                logo_url = extract_logo(target_url)
                new_url = URLmodal(
                    site_url=target_url,
                    site_name=site_name,
                    logo_url=logo_url
                )
                db.session.add(new_url)
                db.session.commit()
            return redirect(url_for("index"))
        elif request.form.get("form_type") == "generate_qr":
            QrCode_text = request.form.get("QrCode_text")
            if QrCode_text:
                getnerateQR_result = getnerateQR(QrCode_text)
            else:
                getnerateQR_result = "Enter URL to get QR"
    url_reads = URLmodal.query.all()
    return render_template(
        "index.html",
        url_reads=url_reads,
        getnerateQR=getnerateQR_result
    )
if __name__ == "__main__":
    app.run(debug=True, port=5000)
