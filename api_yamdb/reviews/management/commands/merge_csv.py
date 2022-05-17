from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
import pandas
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = "Merge .csv to db"

    def handle(self, *args, **options):
        print("reading csv...")
        genre_dict = pandas.read_csv("static/data/genre.csv").to_dict(
            orient="records"
        )
        for entry in genre_dict:
            item = Genre(
                id=entry["id"], name=entry["name"], slug=entry["slug"]
            )
            item.save()
        print("Genre data has successfully saved in db")
        category_dict = pandas.read_csv("static/data/category.csv").to_dict(
            orient="records"
        )
        for entry in category_dict:
            item = Category(
                id=entry["id"], name=entry["name"], slug=entry["slug"]
            )
            item.save()
        print("Category data has successfully saved in db")
        title_dict = pandas.read_csv("static/data/titles.csv").to_dict(
            orient="records"
        )
        for entry in title_dict:
            item = Title(
                id=entry["id"],
                name=entry["name"],
                year=entry["year"],
                category=get_object_or_404(Category, id=entry["category"]),
            )
            item.save()
            title_genre_dict = pandas.read_csv(
                "static/data/genre_title.csv"
            ).to_dict(orient="records")
            for tg_entry in title_genre_dict:
                if tg_entry["title_id"] == entry["id"]:
                    item.genre.add(
                        get_object_or_404(Genre, id=tg_entry["genre_id"])
                    )
        print("Titles data has successfully saved in db")
        user_dict = pandas.read_csv("static/data/users.csv").to_dict(
            orient="records"
        )
        for entry in user_dict:
            item = User(
                id=entry["id"],
                username=entry["username"],
                email=entry["email"],
                role=entry["role"],
                bio=entry["bio"],
                first_name=entry["first_name"],
                last_name=entry["last_name"],
            )

            item.save()
        print("Users data has successfully saved in db")
        review_dict = pandas.read_csv("static/data/review.csv").to_dict(
            orient="records"
        )
        for entry in review_dict:
            item = Review(
                id=entry["id"],
                title=get_object_or_404(Title, id=entry["title_id"]),
                text=entry["text"],
                author=get_object_or_404(User, id=entry["author"]),
                score=entry["score"],
                pub_date=entry["pub_date"],
            )
            item.save()
        print("Review data has successfully saved in db")
        comment_dict = pandas.read_csv("static/data/comments.csv").to_dict(
            orient="records"
        )
        for entry in comment_dict:
            item = Comment(
                id=entry["id"],
                review=get_object_or_404(Review, id=entry["review_id"]),
                text=entry["text"],
                author=get_object_or_404(User, id=entry["author"]),
                pub_date=entry["pub_date"],
            )
            item.save()
        print("Comment data has successfully saved in db")
        return
