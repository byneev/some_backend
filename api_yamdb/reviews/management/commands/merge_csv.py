from django.core.management.base import BaseCommand
import pandas
from reviews.models import Genre

CSV_PATHS = (
    "static/data/category.csv",
    "static/data/comments.csv",
    "static/data/genre_title.csv",
    "static/data/genre.csv",
    "static/data/review.csv",
    "static/data/titles.csv",
    "static/data/users.csv",
)


class Command(BaseCommand):
    help = "Merge .csv to db"

    def handle(self, *args, **options):
        print("reading csv...")
        data = pandas.read_csv("static/data/category.csv")
        data_dict = data.to_dict(orient="records")
        for entry in data_dict:
            item = Genre(
                id=entry["id"], name=entry["name"], slug=entry["slug"]
            )
            item.save()
        print("data has successfully saved in db")
        return
