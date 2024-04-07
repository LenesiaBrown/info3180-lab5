from . import db
from sqlalchemy import func


class Movie(db.Model):    
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    poster = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, title, description, poster, created_at):
        self.title = title
        self.description = description
        self.poster = poster
        self.created_at = created_at
        
    def __repr__(self):
        return f'<Movie {self.title}>'

    
    
    