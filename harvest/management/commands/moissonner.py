from django.core.management.base import BaseCommand
from harvest.tasks import run_all_sources

class Command(BaseCommand):
    help = "Moissonne les données CKAN depuis les sources définies"

    def handle(self, *args, **kwargs):
        run_all_sources()
        self.stdout.write(self.style.SUCCESS("Moissonnage terminé avec succès."))
