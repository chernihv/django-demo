from django.core.management.base import BaseCommand
from django.contrib.auth.models import ContentType, Group, User
from django.conf import settings

from ... import models
from ... import constants
from ... import helpers


class Command(BaseCommand):
    def handle(self, *args, **options):
        add_regular_user_group()
        create_main_superuser()
        helpers.colorprint('App ready', helpers.colorprint.OKBLUE)


def add_regular_user_group():
    models_for_import_permissions = [
        models.Post,
        models.Feedback,
        models.PostFile,
        models.PostComment,
    ]

    def get_permissions(models_list):
        permissions_list = []
        for model in models_list:
            model_name = model.__name__.lower()
            content_type, created = ContentType.objects.get_or_create(app_label='blog', model=model_name)
            for permission in content_type.permission_set.all():
                permissions_list.append(permission)
        return permissions_list

    group, created = Group.objects.get_or_create(name=constants.Group.REGULAR_USER)
    if created:
        group.save()
        for permission in get_permissions(models_for_import_permissions):
            group.permissions.add(permission)
        helpers.colorprint('Group {g} created'.format(g=constants.Group.REGULAR_USER), helpers.colorprint.HEADER)


def create_main_superuser():
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_superuser('admin', settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)
        helpers.colorprint('Superuser: admin created', helpers.colorprint.HEADER)
