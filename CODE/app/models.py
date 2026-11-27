from datetime import datetime, timezone
from app.extensions import db
def current_time():
    return datetime.now(timezone.utc)



class URLmodal(db.Model):
    __tablename__ = "websites"
    id = db.Column(db.Integer, primary_key=True)
    site_url = db.Column(db.String(500), unique=True, nullable=False)
    site_name = db.Column(db.String(150), nullable=False)
    logo_url = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=current_time, nullable=False
    )
    def to_dict(self):
        return {
            "id": self.id,
            "site_url": self.site_url,
            "site_name": self.site_name,
            "logo_url": self.logo_url,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }



class NOTEmodal(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(90), nullable=False)
    note_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=current_time, nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=current_time,
        onupdate=current_time,
        nullable=False,
    )
    def to_dict(self):
        return {
            "id": self.id,
            "note_title": self.note_title,
            "note_content": self.note_content,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
            "updated_at": (self.updated_at.isoformat() if self.updated_at else None),
        }



class QRmodal(db.Model):
    __tablename__ = "qr_codes"
    id = db.Column(db.Integer, primary_key=True)
    qr_data = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), default=current_time, nullable=False
    )
    def to_dict(self):
        return {
            "id": self.id,
            "qr_data": self.qr_data,
            "image_path": self.image_path,
            "created_at": (self.created_at.isoformat() if self.created_at else None),
        }
