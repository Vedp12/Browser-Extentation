
from flask import Blueprint, request, jsonify, url_for, current_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from urllib.parse import urlparse

from app.extensions import db
from app.models import URLmodal, NOTEmodal, QRmodal

from app.services.website_service import (
    normalize_url,
    site_label,
    extract_logo
)

from app.services.qr_service import generate_qr_image


api = Blueprint("api", __name__, url_prefix="/api")


# =========================================
# COMMON RESPONSE FUNCTIONS
# =========================================

def success(message, data=None, status=200):

    response = {
        "success": True,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status


def error(message, status=400):

    return jsonify({
        "success": False,
        "message": message
    }), status


def commit_changes():

    try:
        db.session.commit()
        return None

    except IntegrityError:
        db.session.rollback()
        return error("Duplicate record or database constraint violation", 409)

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Database operation failed")
        return error("Database operation failed", 500)


# =========================================
# HOME / API INFORMATION
# =========================================

@api.route("/", methods=["GET"])
def api_home():

    return success(
        "Flask REST API is running",
        {
            "version": "1.0",
            "resources": [
                "/api/sites",
                "/api/notes",
                "/api/qr"
            ]
        }
    )


# =========================================
# WEBSITE API
# =========================================

# GET ALL WEBSITES

@api.route("/sites", methods=["GET"])
def get_sites():

    sites = db.session.execute(
        select(URLmodal).order_by(URLmodal.id.desc())
    ).scalars().all()

    return success(
        "Websites retrieved successfully",
        {
            "total": len(sites),
            "websites": [site.to_dict() for site in sites]
        }
    )


# ADD WEBSITE

@api.route("/sites", methods=["POST"])
def add_site():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("Request body must be a JSON object")

    raw_url = data.get("site_url")

    if not isinstance(raw_url, str) or not raw_url.strip():
        return error("site_url is required")

    try:
        url = normalize_url(raw_url)
    except ValueError as exc:
        return error(str(exc))

    site = URLmodal(
        site_url=url,
        site_name=site_label(url),
        logo_url=extract_logo(url)
    )

    db.session.add(site)

    result = commit_changes()

    if result:
        return result

    return success(
        "Website added successfully",
        site.to_dict(),
        201
    )


# GET WEBSITE BY ID

@api.route("/sites/<int:site_id>", methods=["GET"])
def get_site(site_id):

    site = db.session.get(URLmodal, site_id)

    if not site:
        return error("Website not found", 404)

    return success("Website retrieved", site.to_dict())


# UPDATE WEBSITE

@api.route("/sites/<int:site_id>", methods=["PUT"])
def update_site(site_id):

    site = db.session.get(URLmodal, site_id)

    if not site:
        return error("Website not found", 404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("Request body must be a JSON object")

    if "site_url" in data:

        if not isinstance(data["site_url"], str) or not data["site_url"].strip():
            return error("Invalid site_url")

        try:
            url = normalize_url(data["site_url"])
        except ValueError as exc:
            return error(str(exc))

        site.site_url = url
        site.site_name = site_label(url)
        site.logo_url = extract_logo(url)

    if "site_name" in data:
        if not isinstance(data["site_name"], str) or not data["site_name"].strip():
            return error("Invalid site_name")
        site.site_name = data["site_name"].strip()

    result = commit_changes()

    if result:
        return result

    return success("Website updated successfully", site.to_dict())


# DELETE WEBSITE

@api.route("/sites/<int:site_id>", methods=["DELETE"])
def delete_site(site_id):

    site = db.session.get(URLmodal, site_id)

    if not site:
        return error("Website not found", 404)

    db.session.delete(site)

    result = commit_changes()

    if result:
        return result

    return success("Website deleted successfully")


# =========================================
# NOTES API
# =========================================

# GET ALL NOTES

@api.route("/notes", methods=["GET"])
def get_notes():

    notes = db.session.execute(
        select(NOTEmodal).order_by(NOTEmodal.id.desc())
    ).scalars().all()

    return success(
        "Notes retrieved successfully",
        {
            "total": len(notes),
            "notes": [note.to_dict() for note in notes]
        }
    )


# CREATE NOTE

@api.route("/notes", methods=["POST"])
def create_note():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("Request body must be a JSON object")

    title = data.get("note_title")
    content = data.get("note_content")

    if not isinstance(title, str) or not title.strip():
        return error("note_title is required")

    if not isinstance(content, str) or not content.strip():
        return error("note_content is required")

    note = NOTEmodal(
        note_title=title.strip()[:90],
        note_content=content.strip()
    )

    db.session.add(note)

    result = commit_changes()

    if result:
        return result

    return success(
        "Note created successfully",
        note.to_dict(),
        201
    )


# GET NOTE BY ID

@api.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):

    note = db.session.get(NOTEmodal, note_id)

    if not note:
        return error("Note not found", 404)

    return success("Note retrieved successfully", note.to_dict())


# UPDATE NOTE

@api.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):

    note = db.session.get(NOTEmodal, note_id)

    if not note:
        return error("Note not found", 404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("Request body must be a JSON object")

    if "note_title" in data:

        if not isinstance(data["note_title"], str) or not data["note_title"].strip():
            return error("Invalid note_title")

        note.note_title = data["note_title"].strip()[:90]

    if "note_content" in data:

        if not isinstance(data["note_content"], str) or not data["note_content"].strip():
            return error("Invalid note_content")

        note.note_content = data["note_content"].strip()

    result = commit_changes()

    if result:
        return result

    return success("Note updated successfully", note.to_dict())


# DELETE NOTE

@api.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):

    note = db.session.get(NOTEmodal, note_id)

    if not note:
        return error("Note not found", 404)

    db.session.delete(note)

    result = commit_changes()

    if result:
        return result

    return success("Note deleted successfully")


# =========================================
# QR CODE API
# =========================================

# GET ALL QR CODES

@api.route("/qr", methods=["GET"])
def get_qr_codes():

    codes = db.session.execute(
        select(QRmodal).order_by(QRmodal.id.desc())
    ).scalars().all()

    results = []

    for code in codes:

        item = code.to_dict()

        item["image_url"] = url_for(
            "static",
            filename=code.image_path,
            _external=True
        )

        results.append(item)

    return success(
        "QR codes retrieved successfully",
        {
            "total": len(results),
            "qr_codes": results
        }
    )


# GENERATE QR CODE

@api.route("/qr", methods=["POST"])
def create_qr():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error("Request body must be a JSON object")

    qr_data = data.get("data")

    if not isinstance(qr_data, str) or not qr_data.strip():
        return error("QR data is required")

    qr_data = qr_data.strip()

    if len(qr_data) > 10000:
        return error("QR data is too large")

    image_path = generate_qr_image(qr_data)

    qr = QRmodal(
        qr_data=qr_data,
        image_path=image_path
    )

    db.session.add(qr)

    result = commit_changes()

    if result:
        import os
        filepath = os.path.join(
            current_app.static_folder,
            image_path
        )
        if os.path.exists(filepath):
            os.remove(filepath)

        return result

    return success(
        "QR code generated successfully",
        {
            **qr.to_dict(),
            "image_url": url_for(
                "static",
                filename=image_path,
                _external=True
            )
        },
        201
    )


# GET QR CODE BY ID

@api.route("/qr/<int:qr_id>", methods=["GET"])
def get_qr(qr_id):

    qr = db.session.get(QRmodal, qr_id)

    if not qr:
        return error("QR code not found", 404)

    return success(
        "QR code retrieved successfully",
        {
            **qr.to_dict(),
            "image_url": url_for(
                "static",
                filename=qr.image_path,
                _external=True
            )
        }
    )


# DELETE QR CODE

@api.route("/qr/<int:qr_id>", methods=["DELETE"])
def delete_qr(qr_id):

    import os

    qr = db.session.get(QRmodal, qr_id)

    if not qr:
        return error("QR code not found", 404)

    filepath = os.path.join(
        current_app.static_folder,
        qr.image_path
    )

    db.session.delete(qr)

    result = commit_changes()

    if result:
        return result

    if os.path.isfile(filepath):
        os.remove(filepath)

    return success("QR code deleted successfully")
