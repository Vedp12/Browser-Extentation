from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app
)

from app.extensions import db
from app.models import URLmodal, NOTEmodal, QRmodal

from app.services.website_service import (
    normalize_url,
    site_label,
    extract_logo
)

from app.services.qr_service import generate_qr_image


web = Blueprint("web", __name__)


@web.route("/", methods=["GET", "POST"])
def index():

    qr_code_url = None

    if request.method == "POST":

        form_type = request.form.get("form_type")

        # ADD WEBSITE
        if form_type == "add_site":

            raw = request.form.get("site_url", "").strip()

            if raw:

                try:
                    url = normalize_url(raw)

                    site = URLmodal(
                        site_url=url,
                        site_name=site_label(url),
                        logo_url=extract_logo(url)
                    )

                    db.session.add(site)
                    db.session.commit()

                except ValueError:
                    db.session.rollback()

                except Exception:
                    db.session.rollback()
                    current_app.logger.exception("Website creation failed")

            return redirect(url_for("web.index"))

        # GENERATE QR CODE
        elif form_type == "generate_qr":

            data = request.form.get("data", "").strip()

            if data and len(data) <= 10000:

                image_path = generate_qr_image(data)

                qr = QRmodal(
                    qr_data=data,
                    image_path=image_path
                )

                try:
                    db.session.add(qr)
                    db.session.commit()

                    qr_code_url = url_for(
                        "static",
                        filename=image_path,
                        v=qr.id
                    )

                except Exception:
                    db.session.rollback()
                    current_app.logger.exception("QR generation failed")

        # SAVE NOTE
        elif form_type == "take_notes":

            title = request.form.get("note_title", "").strip()
            content = request.form.get("note_content", "").strip()

            if title and content:

                note = NOTEmodal(
                    note_title=title[:90],
                    note_content=content
                )

                try:
                    db.session.add(note)
                    db.session.commit()

                    return redirect(url_for("web.index"))

                except Exception:
                    db.session.rollback()
                    current_app.logger.exception("Note creation failed")

    return render_template(
        "index.html",
        url_reads=URLmodal.query.all(),
        notes_modals=NOTEmodal.query.all(),
        qr_code=qr_code_url
    )