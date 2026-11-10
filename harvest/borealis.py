"""Client minimal pour l'API Dataverse de Borealis (https://borealisdata.ca).

Centralise l'appel HTTP et l'analyse des métadonnées pour que le moissonnage
(harvest.tasks) et l'API GraphQL (api_graphql.schema) utilisent le même code.
"""
import logging
from datetime import date

import requests

logger = logging.getLogger(__name__)

BOREALIS_URL = "https://borealisdata.ca"
DATAVERSE_ID = "daviddeslauriers"
TIMEOUT = 15  # secondes


def _field(citation_fields, name, default=""):
    for field in citation_fields:
        if field.get("typeName") == name:
            return field.get("value", default)
    return default


def _parse_date(value):
    try:
        return date.fromisoformat(value[:10]) if value else None
    except ValueError:
        return None


def parse_dataset(doi, metadata):
    """Transforme la réponse JSON d'un jeu de données en dictionnaire simple."""
    citation = metadata["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"]

    descriptions = _field(citation, "dsDescription", [])
    description = descriptions[0]["dsDescriptionValue"]["value"] if descriptions else ""

    keywords = [
        k["keywordValue"]["value"]
        for k in _field(citation, "keyword", [])
        if isinstance(k, dict) and "keywordValue" in k
    ]

    authors = ", ".join(
        a["authorName"]["value"] for a in _field(citation, "author", []) if "authorName" in a
    )

    return {
        "title": _field(citation, "title"),
        "doi": doi,
        "url": f"{BOREALIS_URL}/dataset.xhtml?persistentId={doi}",
        "description": description,
        "keywords": keywords,
        "authors": authors,
        "publication_date": _parse_date(_field(citation, "dateOfDeposit")),
    }


def fetch_datasets(limit=None):
    """Retourne la liste des jeux de données du dataverse, sous forme de dictionnaires."""
    response = requests.get(
        f"{BOREALIS_URL}/api/dataverses/{DATAVERSE_ID}/contents", timeout=TIMEOUT
    )
    response.raise_for_status()
    items = [i for i in response.json().get("data", []) if i.get("type") == "dataset"]
    if limit:
        items = items[:limit]

    results = []
    for item in items:
        doi = f"{item.get('protocol', 'doi')}:{item['authority']}/{item['identifier']}" \
            if "authority" in item else item["identifier"]
        meta = requests.get(
            f"{BOREALIS_URL}/api/datasets/:persistentId/",
            params={"persistentId": doi},
            timeout=TIMEOUT,
        )
        if meta.status_code != 200:
            logger.warning("Métadonnées introuvables pour %s (HTTP %s)", doi, meta.status_code)
            continue
        try:
            results.append(parse_dataset(doi, meta.json()))
        except (KeyError, IndexError, TypeError) as exc:
            logger.warning("Métadonnées mal formées pour %s : %s", doi, exc)
    return results
