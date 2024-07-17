from django.core.management.base import BaseCommand
from subscriptions.models import SubModel


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        qs = SubModel.objects.filter(active=True)
        for objs in qs:
            print(objs.groups.all(), end="\n")
            print(objs.permissions.all())
            print("\n")
