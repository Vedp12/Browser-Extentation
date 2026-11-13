from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class URLmodal(db.Model):
    __tablename__ = "url_modal"

    id = db.Column(db.Integer, primary_key=True)
    site_url = db.Column(db.String(500), nullable=False)
    site_name = db.Column(db.String(200), nullable=False)
    logo_url = db.Column(db.String(500), nullable=True)


class NOTEmodal(db.Model):
    __tablename__ = "note_modal"
    id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(90),nullable=False)
    note_content = db.Column(db.String(),nullable=False)
    
