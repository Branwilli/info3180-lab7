from . import db
from datetime import datetime


class Movies(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(128))
    poster = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
# Add any model classes for Flask-SQLAlchemy here