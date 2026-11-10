import logging

from .borealis import fetch_datasets
from .models import BorealisDataset

logger = logging.getLogger(__name__)


def fetch_borealis_data(limit=None):
    """Moissonne Borealis et enregistre les jeux de données (clé : DOI).

    Retourne le nombre de jeux de données créés ou mis à jour.
    """
    try:
        datasets = fetch_datasets(limit=limit)
    except Exception:
        logger.exception("Erreur lors du moissonnage Borealis")
        return 0

    for data in datasets:
        doi = data.pop("doi")
        BorealisDataset.objects.update_or_create(doi=doi, defaults=data)
    return len(datasets)


def run_all_sources():
    return fetch_borealis_data()
