from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URLmodal(db.Model):
    __tablename__ = "url_modal"
    
    id = db.Column(db.Integer, primary_key=True)
    site_url = db.Column(db.String(500), nullable=False)
    site__name = db.Column(db.String(200), nullable=False)