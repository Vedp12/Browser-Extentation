from flask import Blueprint, request, jsonify
from app import db, URLmodal, NOTEmodal
from datetime import datetime
from app import normalize_url, site_label, extract_logo

api = Blueprint("api", __name__, url_prefix="/api")


# =====================================
# WEBSITE API
# =====================================




# GET ALL WEBSITES
@api.route("/sites", methods=["GET"])
def get_sites():

    sites = URLmodal.query.all()

    return (
        jsonify(
            {
                "success": True,
                "total": len(sites),
                "data": [
                    {
                        "id": site.id,
                        "site_url": site.site_url,
                        "site_name": site.site_name,
                        "logo_url": site.logo_url,
                    }
                    for site in sites
                ],
            }
        ),
        200,
    )


# ADD WEBSITE
@api.route("/sites", methods=["POST"])
def add_site():

    data = request.get_json(silent=True) or {}

    raw_url = data.get("site_url", "").strip()

    if not raw_url:
        return jsonify({"success": False, "message": "site_url is required"}), 400

    url = normalize_url(raw_url)

    site = URLmodal(site_url=url, site_name=site_label(url), logo_url=extract_logo(url))

    db.session.add(site)
    db.session.commit()

    return (
        jsonify(
            {
                "success": True,
                "message": "Website added successfully",
                "data": {
                    "id": site.id,
                    "site_url": site.site_url,
                    "site_name": site.site_name,
                    "logo_url": site.logo_url,
                },
            }
        ),
        201,
    )


# GET WEBSITE BY ID
@api.route("/sites/<int:site_id>", methods=["GET"])
def get_site(site_id):

    site = db.session.get(URLmodal, site_id)

    if not site:
        return jsonify({"success": False, "message": "Website not found"}), 404

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "id": site.id,
                    "site_url": site.site_url,
                    "site_name": site.site_name,
                    "logo_url": site.logo_url,
                },
            }
        ),
        200,
    )


# UPDATE WEBSITE
@api.route("/sites/<int:site_id>", methods=["PUT"])
def update_site(site_id):

    site = db.session.get(URLmodal, site_id)

    if not site:
        return jsonify({"success": False, "message": "Website not found"}), 404

    data = request.get_json(silent=True) or {}

    if "site_url" in data:

        url = normalize_url(data["site_url"].strip())

        site.site_url = url
        site.site_name = site_label(url)
        site.logo_url = extract_logo(url)

    db.session.commit()

    return jsonify({"success": True, "message": "Website updated successfully"}), 200


# DELETE WEBSITE
@api.route("/sites/<int:site_id>", methods=["DELETE"])
def delete_site(site_id):

    site = db.session.get(URLmodal, site_id)

    if not site:
        return jsonify({"success": False, "message": "Website not found"}), 404

    db.session.delete(site)
    db.session.commit()

    return jsonify({"success": True, "message": "Website deleted successfully"}), 200


# =====================================
# NOTES API
# =====================================


# GET ALL NOTES
@api.route("/notes", methods=["GET"])
def get_notes():

    notes = NOTEmodal.query.all()

    return (
        jsonify(
            {
                "success": True,
                "total": len(notes),
                "data": [
                    {
                        "id": note.id,
                        "note_title": note.note_title,
                        "note_content": note.note_content,
                        "created_at": (
                            note.created_at.isoformat() if note.created_at else None
                        ),
                    }
                    for note in notes
                ],
            }
        ),
        200,
    )


# CREATE NOTE
@api.route("/notes", methods=["POST"])
def create_note():

    data = request.get_json(silent=True) or {}

    title = data.get("note_title", "").strip()
    content = data.get("note_content", "").strip()

    if not title or not content:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "note_title and note_content are required",
                }
            ),
            400,
        )

    note = NOTEmodal(
        note_title=title[:90], note_content=content, created_at=datetime.now()
    )

    db.session.add(note)
    db.session.commit()

    return (
        jsonify(
            {
                "success": True,
                "message": "Note created successfully",
                "data": {
                    "id": note.id,
                    "note_title": note.note_title,
                    "note_content": note.note_content,
                    "created_at": note.created_at.isoformat(),
                },
            }
        ),
        201,
    )


# GET NOTE BY ID
@api.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):

    note = db.session.get(NOTEmodal, note_id)

    if not note:
        return jsonify({"success": False, "message": "Note not found"}), 404

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "id": note.id,
                    "note_title": note.note_title,
                    "note_content": note.note_content,
                    "created_at": (
                        note.created_at.isoformat() if note.created_at else None
                    ),
                },
            }
        ),
        200,
    )


# UPDATE NOTE
@api.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):

    note = db.session.get(NOTEmodal, note_id)

    if not note:
        return jsonify({"success": False, "message": "Note not found"}), 404

    data = request.get_json(silent=True) or {}

    if "note_title" in data:
        note.note_title = data["note_title"].strip()[:90]

    if "note_content" in data:
        note.note_content = data["note_content"].strip()

    db.session.commit()

    return jsonify({"success": True, "message": "Note updated successfully"}), 200


# DELETE NOTE
@api.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):

    note = db.session.get(NOTEmodal, note_id)

    if not note:
        return jsonify({"success": False, "message": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"success": True, "message": "Note deleted successfully"}), 200


