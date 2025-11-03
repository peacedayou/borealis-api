import graphene
from graphene_django.types import DjangoObjectType
from harvest.models import BorealisDataset
import requests

class BorealisDatasetType(DjangoObjectType):
    class Meta:
        model = BorealisDataset

class Query(graphene.ObjectType):
    borealis_live = graphene.List(BorealisDatasetType)

    def resolve_borealis_live(root, info):
        base_url = "https://borealisdata.ca"
        dataverse_id = "daviddeslauriers"
        list_url = f"{base_url}/api/dataverses/{dataverse_id}/contents"

        try:
            response = requests.get(list_url)
            response.raise_for_status()
            items = response.json().get("data", [])
            results = []

            for item in items:
                if item["type"] != "dataset":
                    continue

                doi = item["identifier"]
                meta_url = f"{base_url}/api/datasets/:persistentId/?persistentId={doi}"
                meta = requests.get(meta_url)
                if meta.status_code != 200:
                    continue

                citation = meta.json()["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"]

                def get_field(name):
                    for field in citation:
                        if field["typeName"] == name:
                            return field.get("value", "")
                    return ""

                # Création d'une instance non enregistrée
                dataset = BorealisDataset(
                    title=get_field("title"),
                    doi=doi,
                    url=f"https://borealisdata.ca/dataset.xhtml?persistentId={doi}",
                    description=get_field("dsDescription")[0]["dsDescriptionValue"]["value"] if get_field("dsDescription") else "",
                    keywords=get_field("keyword"),
                    publication_date=get_field("dateOfDeposit"),
                    authors=", ".join(a["authorName"]["value"] for a in get_field("author")) if get_field("author") else ""
                )
                results.append(dataset)

            return results

        except Exception as e:
            print(f"Erreur Borealis GraphQL : {e}")
            return []

schema = graphene.Schema(query=Query)