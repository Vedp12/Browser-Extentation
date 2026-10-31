import urllib.parse
from flask import Flask, render_template, request, redirect , abort
from templates.models import db, URLmodal
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///extentation.db"  # ^ It creates the database name extentation.db in an instance file
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Directly call create_all() here

    
# ! 1. Create
@app.route("/", methods=["GET","POST"])
def create():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        site_url = request.form["site_url"]
        site__name = request.form["site__name"]

        URL_add = URLmodal(
            site_url=site_url,
            site__name=site__name
        )  # * Insters URL to the database
        db.session.add(URL_add)
        db.session.commit()
        return redirect("/")
    
# ! 2. Read
@app.route("/", methods=["GET"])
def read():
    Url_reads = URLmodal.query.all()
    return render_template('index.html',Url_reads=Url_reads)
    
if __name__ == "__main__":
    app.run(debug=True)