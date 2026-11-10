from django.core.management.base import BaseCommand
from harvest.tasks import run_all_sources

class Command(BaseCommand):
    help = "Moissonne les jeux de données Borealis et les enregistre en base"

    def handle(self, *args, **kwargs):
        count = run_all_sources()
        self.stdout.write(self.style.SUCCESS(f"Moissonnage terminé : {count} jeu(x) de données."))
