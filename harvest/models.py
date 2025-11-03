from django.db import models

class Dataset(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=100)  # OpenGouv, CanWin, etc.
    keywords = models.JSONField(default=list)
    theme = models.CharField(max_length=100, blank=True)
    producer = models.CharField(max_length=255, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.source})"


class BorealisDataset(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    doi = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.JSONField(default=list)
    publication_date = models.DateField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title