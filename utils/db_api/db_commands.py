from asgiref.sync import sync_to_async

from django.db.models import Q
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.telegrambot.telegrambot.settings')
import django

django.setup()
from django_project.telegrambot.usersmanage.models import User


@sync_to_async
def select_user(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).values().first()
    return user


@sync_to_async
def add_user(telegram_id, name, username):
    return User(telegram_id=int(telegram_id), name=name, username=username).save()


@sync_to_async
def delete_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).delete()


@sync_to_async
def select_all_users():
    users = User.objects.all().values()
    return users


@sync_to_async
def select_all_users_id(telegram_id: int):
    users = User.objects.filter(telegram_id=telegram_id).all().values()
    return users


@sync_to_async
def count_users():
    return User.objects.all().count()


@sync_to_async
def update_user_data(telegram_id, **kwargs):
    return User.objects.filter(telegram_id=telegram_id).update(**kwargs)


@sync_to_async
def select_user_username(username: str):
    user = User.objects.filter(username=username).values().first()
    return user


@sync_to_async
def search_users(need_partner_sex, need_age_min, need_age_max, need_region):
    lst = User.objects.filter(
        Q(sex=need_partner_sex) & Q(age__gte=need_age_min) & Q(age__lte=need_age_max) & Q(region=need_region)
    ).all()


    if lst.count() < 10:
        lst = User.objects.filter(
            Q(sex=need_partner_sex) & Q(age__gte=need_age_min) & Q(age__lte=need_age_max)
        ).all()

    if lst.count() < 100:
        lst = User.objects.filter(
            Q(sex=need_partner_sex) & Q(age__gte=need_age_min)
        ).all()

    return lst.values()


@sync_to_async
def count_all_users_kwarg(**kwarg):
    return User.objects.filter(**kwarg).all().values().count()
