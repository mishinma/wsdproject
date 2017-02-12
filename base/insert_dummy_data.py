from community.models import Game, Game_Category
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


# Helper function to deal with existing usernames
def get_or_create_user(username, email, password):
    try:
        new_user = User.objects.create(username, email)
    except IntegrityError:
        return User.objects.get(username=username)
    else:
        new_user.set_password(password)
        new_user.save()

    return new_user


# Helper function to deal with existing game names
def get_or_create_game(dev, cat, url, price, name, desc, rating, sale=None):
    try:
        new_game = Game.objects.create(
            developer=dev,
            category=cat,
            source_url=url,
            price=price,
            sales_price=sale,
            name=name,
            description=desc,
            rating=rating
        )
    except IntegrityError:
        return Game.objects.get(name=name)
    else:
        new_game.save()

    return new_game


# Helper function to deal with existing category names
def get_or_create_game_cat(name):
    try:
        new_cat = Game_Category.objects.create(name=name)
    except IntegrityError:
        return Game_Category.get(name=name)
    else:
        new_cat.save()

    return new_cat
