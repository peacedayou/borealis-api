import requests
from .models import Dataset

BOREALIS_URL = "https://borealisdata.ca"
DATAVERSE_ID = "daviddeslauriers"

def fetch_borealis_data(limit=10):
    try:
        list_url = f"{BOREALIS_URL}/api/dataverses/{DATAVERSE_ID}/contents"
        response = requests.get(list_url)
        response.raise_for_status()
        items = response.json().get("data", [])[:limit]

        for item in items:
            if item["type"] != "dataset":
                continue

            doi = item["identifier"]
            meta_url = f"{BOREALIS_URL}/api/datasets/:persistentId/?persistentId={doi}"
            meta = requests.get(meta_url)
            if meta.status_code != 200:
                continue

            citation = meta.json()["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"]

            def get_field(name):
                for field in citation:
                    if field["typeName"] == name:
                        return field.get("value", "")
                return ""

            Dataset.objects.update_or_create(
                title=get_field("title"),
                defaults={
                    "description": get_field("dsDescription")[0]["dsDescriptionValue"]["value"] if get_field("dsDescription") else "",
                    "source": "Boréalis",
                    "keywords": get_field("keyword"),
                    "theme": "",  # Pas de thème dans Borealis
                    "producer": ", ".join(a["authorName"]["value"] for a in get_field("author")) if get_field("author") else "",
                }
            )
    except Exception as e:
        print(f"Erreur lors du moissonnage Borealis : {e}")

def run_all_sources():
    fetch_borealis_data()
