
from flask import Flask, render_template, request, redirect, url_for
from templates.models import db, URLmodal
from qr_main import getnerateQR

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///extentation.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():

    getnerateQR_result = None

    if request.method == "POST":

        # Form 1: Add website
        if request.form.get("form_type") == "add_site":

            site_url = request.form.get("site_url")
            site_name = request.form.get("site_name")

            if site_url and site_name:

                new_url = URLmodal(
                    site_url=site_url,
                    site_name=site_name
                )

                db.session.add(new_url)
                db.session.commit()

            return redirect(url_for("index"))

        # Form 2: Generate QR code
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
