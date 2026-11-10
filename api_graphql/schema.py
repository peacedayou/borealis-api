import logging

import graphene
from graphene_django.types import DjangoObjectType

from harvest.borealis import fetch_datasets
from harvest.models import BorealisDataset

logger = logging.getLogger(__name__)


class BorealisDatasetType(DjangoObjectType):
    class Meta:
        model = BorealisDataset
        fields = "__all__"


class Query(graphene.ObjectType):
    # Jeux de données déjà moissonnés (base locale)
    borealis = graphene.List(BorealisDatasetType, q=graphene.String())
    # Lecture en direct depuis Borealis, sans enregistrement
    borealis_live = graphene.List(BorealisDatasetType, limit=graphene.Int())

    def resolve_borealis(root, info, q=None):
        return BorealisDataset.search(q)

    def resolve_borealis_live(root, info, limit=None):
        try:
            return [BorealisDataset(**d) for d in fetch_datasets(limit=limit)]
        except Exception:
            logger.exception("Erreur Borealis GraphQL")
            return []


schema = graphene.Schema(query=Query)
