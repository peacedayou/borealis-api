from django.test import SimpleTestCase, TestCase

from .borealis import parse_dataset
from .models import BorealisDataset

SAMPLE = {
    "data": {"latestVersion": {"metadataBlocks": {"citation": {"fields": [
        {"typeName": "title", "value": "Température de l'eau du Saint-Laurent"},
        {"typeName": "author", "value": [{"authorName": {"value": "Tremblay, Marie"}}]},
        {"typeName": "dsDescription", "value": [{"dsDescriptionValue": {"value": "Mesures 2020-2024"}}]},
        {"typeName": "keyword", "value": [{"keywordValue": {"value": "océanographie"}}]},
        {"typeName": "dateOfDeposit", "value": "2024-05-12"},
    ]}}}}
}


class ParseDatasetTests(SimpleTestCase):
    def test_parse_complet(self):
        d = parse_dataset("doi:10.5683/SP3/ABC", SAMPLE)
        self.assertEqual(d["title"], "Température de l'eau du Saint-Laurent")
        self.assertEqual(d["authors"], "Tremblay, Marie")
        self.assertEqual(d["keywords"], ["océanographie"])
        self.assertEqual(str(d["publication_date"]), "2024-05-12")
        self.assertIn("doi:10.5683/SP3/ABC", d["url"])

    def test_champs_manquants(self):
        vide = {"data": {"latestVersion": {"metadataBlocks": {"citation": {"fields": []}}}}}
        d = parse_dataset("doi:x", vide)
        self.assertEqual(d["keywords"], [])
        self.assertIsNone(d["publication_date"])


class SearchTests(TestCase):
    def setUp(self):
        BorealisDataset.objects.create(
            title="Glace de mer", authors="A", doi="doi:1", description="Arctique",
            keywords=["glace"], url="https://example.org/1",
        )
        BorealisDataset.objects.create(
            title="Salinité", authors="B", doi="doi:2", description="Estuaire",
            keywords=["sel"], url="https://example.org/2",
        )

    def test_recherche_titre(self):
        self.assertEqual(BorealisDataset.search("glace").count(), 1)

    def test_recherche_vide_retourne_tout(self):
        self.assertEqual(BorealisDataset.search("").count(), 2)
