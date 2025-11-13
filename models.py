from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    rating = db.Column(db.Float)
    url = db.Column(db.String(255))

    def __repr__(self):
        return f"<Movie {self.title}>"
