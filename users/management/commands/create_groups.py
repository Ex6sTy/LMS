from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create default user groups"

    def handle(self, *args, **options):
        Group.objects.get_or_create(name="moderators")
        self.stdout.write(self.style.SUCCESS("Groups created or already exist"))
