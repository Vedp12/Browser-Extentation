from flask import Flask, redirect, render_template, request, url_for
import os
import re
import time
from urllib.parse import urljoin, urlparse
from flask_moment import Moment
import qrcode
import requests
import tldextract
from bs4 import BeautifulSoup

import flask_sqlalchemy
from templates.models import db, URLmodal, NOTEmodal
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


def normalize_url(raw):
    raw = raw.strip()
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    return raw


def site_label(url):
    name = tldextract.extract(url).domain
    return (name or urlparse(url).netloc)[:200]


def extract_logo(url):
    parsed = urlparse(url)
    if not parsed.netloc:
        return None

    fallback = f"https://www.google.com/s2/favicons?domain={parsed.netloc}&sz=128"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        tag = soup.find("link", rel=re.compile(r"icon", re.I)) or soup.find(
            "meta", property="og:image"
        )
        if tag:
            href = tag.get("href") or tag.get("content")
            if href:
                return urljoin(resp.url, href)
    except Exception:
        # Network or parsing failure: fall back to the Google favicon service.
        pass
    return fallback


@app.route("/", methods=["GET", "POST"])
def index():
    qr_code_url = None
    if request.method == "GET":
        form_type = request.form.get("form_type")
        
    elif request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "add_site":
            raw = request.form.get("site_url", "").strip()
            if raw:
                url = normalize_url(raw)
                db.session.add(
                    URLmodal(
                        site_url=url,
                        site_name=site_label(url),
                        logo_url=extract_logo(url),
                    )
                )
                db.session.commit()
            return redirect(url_for("index"))
        elif form_type == "browser_search_result":
            # browser_search = request.form.get("browser_search")
            provider = request.form.get("provider")
            raw_search = request.form.get("browser_search").replace(' ','+')
            if provider == "Google":
                url = f"https://www.google.com/search?q={raw_search}"
                return redirect(url)
            elif provider == "DuckDuckGo":
                url = f"https://duckduckgo.com/?q={raw_search}"
                return redirect(url)
            elif provider == "Perplexity":
                url = f"https://www.perplexity.ai?q={raw_search}"
                return redirect(url)
            
        elif form_type == "generate_qr":
            data = request.form.get("data", "").strip()
            if data:
                qr_dir = os.path.join(app.static_folder, "image")
                os.makedirs(qr_dir, exist_ok=True)
                qrcode.make(data).save(os.path.join(qr_dir, "qr_code.png"))
                # Timestamp busts the browser cache so a new QR shows immediately.
                qr_code_url = url_for(
                    "static", filename="image/qr_code.png", v=int(time.time())
                )

        elif form_type == "take_notes":
            title = request.form.get("note_title", "").strip()
            content = request.form.get("note_content", "").strip()

            if title and content:
                DateTime = datetime.now()
                db.session.add(
                    NOTEmodal(
                        note_title=title[:90], note_content=content, created_at=DateTime
                    )
                )
                db.session.commit()
                return redirect(url_for("index"))

           
    return render_template(
        "index.html",
        url_reads=URLmodal.query.all(),
        notes_modals=NOTEmodal.query.all(),
        qr_code=qr_code_url,
    )


# @app.route("/add_site/<int:id>/edit",methods="GET")
# def edit_add_site(id):
#     add_site = db.get_or_404(URLmodal, id)
    



@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    bookmark = db.get_or_404(URLmodal, id)
    db.session.delete(bookmark)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/notes/<int:id>/edit", methods=["GET"])
def edit_notes(id):
    note = db.get_or_404(NOTEmodal, id)
    if request.headers.get("HX-Request"):
        return render_template("_note_form.html", edit_notes=note)
    return render_template(
        "index.html",
        url_reads=URLmodal.query.all(),
        notes_modals=NOTEmodal.query.all(),
        edit_notes=note,
        qr_code=None,
    )


@app.route("/notes/<int:id>/update", methods=["POST"])
def update_notes(id):
    note = db.get_or_404(NOTEmodal, id)
    title = request.form.get("note_title", "").strip()
    content = request.form.get("note_content", "").strip()
    if title and content:
        note.note_title = title[:90]
        note.note_content = content
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/notes/<int:id>/delete", methods=["POST"])
def delete_note(id):
    note = db.get_or_404(NOTEmodal, id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Set debug=False when deploying.
    app.run(debug=True, port=9000)
