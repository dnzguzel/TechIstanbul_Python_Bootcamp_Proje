from flask import Flask, render_template, redirect, url_for, flash
from models import db, Movie
from scraper import update_database
import os

# Flask uygulamasını ve veritabanı yapılandırmasını ayarlamak için
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'movies.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ru5TXhl7CjWCuUr2INoKQPBdLmbIPMQX'
app.config[f'SQLALCHEMY_DATABASE_URI'] = f'{SQLALCHEMY_DATABASE_URI}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ORM nesnesini uygulamaya bağlamak için
db.init_app(app)

# Uygulama bağlamında veritabanını oluşturmak için
with app.app_context():
    db.create_all()


# Ana sayfa rotası
@app.route("/")
def index():
    movies = Movie.query.order_by(Movie.rating.desc()).all()
    # for movie in movies:
    #     print(f"{movie.title} - Rating: {movie.rating} - URL: {movie.url}")
    return render_template("index.html", movies=movies)


# Güncelleme rotası
@app.route("/update")
def update():
    update_database()
    flash("IMDb verileri başarıyla güncellendi!", "success")
    return redirect(url_for("index"))


# Uygulamayı çalıştır
if __name__ == "__main__":
    app.run(debug=True)
