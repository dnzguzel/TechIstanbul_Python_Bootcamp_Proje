import requests
from bs4 import BeautifulSoup
from models import db, Movie


# IMDb Top 25 filmlerini çekme fonksiyonu
def fetch_imdb_top25():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []
    rows = soup.select("li.ipc-metadata-list-summary-item")

    for row in rows:
        title_tag = row.select_one("h3")
        if title_tag:
            title_text = title_tag.text.strip()
            if ". " in title_text:
                title = title_text.split(". ", 1)[1]
            else:
                title = title_text
        else:
            title = None

        rating_tag = row.select_one("span.ipc-rating-star--rating")
        rating = float(rating_tag.text.strip()) if rating_tag else None

        film_url_tag = row.select_one("a.ipc-title-link-wrapper")
        film_url = "https://www.imdb.com" + film_url_tag['href'] if film_url_tag else None
        # print(f"Fetched: {title} - Rating: {rating} - URL: {film_url}")

        if title and rating:
            movies.append({"title": title, "rating": rating, "url": film_url})
    return movies


# Veritabanını güncelleme fonksiyonu
def update_database():
    movies = fetch_imdb_top25()
    current_titles = []

    for data in movies:
        current_titles.append(data["title"])
        existing = Movie.query.filter_by(title=data["title"]).first()

        if existing:
            existing.rating = data["rating"]
        else:
            db.session.add(Movie(**data))

    # Listede olmayanları siler
    Movie.query.filter(~Movie.title.in_(current_titles)).delete(synchronize_session=False)
    db.session.commit()
