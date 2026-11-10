# Borealis API

API Django qui moissonne les jeux de données scientifiques du dépôt
[Borealis](https://borealisdata.ca) (Dataverse canadien) et les expose en **REST**,
en **GraphQL** et dans un **tableau de bord web**.

## Fonctionnalités

- **Moissonnage** des métadonnées Borealis (titre, auteurs, DOI, mots-clés, date) avec
  mise à jour idempotente par DOI, par commande ou depuis le tableau de bord.
- **API REST** (Django REST Framework) avec authentification par jeton et recherche plein texte.
- **API GraphQL** (Graphene) : données en base ou lecture en direct depuis Borealis.
- **Documentation interactive** Swagger et ReDoc générée automatiquement.
- **Tableau de bord** : recherche et statistiques par année de publication.

## Architecture

```
ogsl_project/   configuration Django (paramètres lus dans les variables d'environnement)
harvest/        modèle BorealisDataset, client Borealis, moissonnage, API REST
api_graphql/    schéma GraphQL
dashboard/      pages web (accueil, recherche, statistiques)
users/          authentification par jeton
```

## Démarrage rapide

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # puis adapter les valeurs
export $(grep -v '^#' .env | xargs)
python manage.py migrate
python manage.py createsuperuser
python manage.py moissonner   # importe les jeux de données Borealis
python manage.py runserver
```

Sans `DB_NAME`, le projet utilise SQLite. Avec `DB_NAME`, il se connecte à MySQL.

## Points d'accès

| URL | Description |
| --- | --- |
| `/` | Tableau de bord |
| `/api/borealis/` | Liste REST des jeux de données (jeton requis) |
| `/api/borealis/search/?q=glace` | Recherche plein texte |
| `/auth/login/` | Obtenir un jeton (`POST username`, `password`) |
| `/graphql/` | GraphiQL |
| `/swagger/` · `/redoc/` | Documentation de l'API |

Exemple GraphQL :

```graphql
{ borealis(q: "glace") { title authors doi publicationDate } }
```

## Tests

```bash
python manage.py test
```

## Déploiement

Le fichier `render.yaml` déploie l'application sur [Render](https://render.com) avec Gunicorn.
Les secrets (`DJANGO_SECRET_KEY`, identifiants MySQL) sont définis comme variables
d'environnement dans Render et ne sont jamais versionnés.

## Technologies

Python · Django · Django REST Framework · Graphene-Django · drf-yasg · MySQL / SQLite · Gunicorn · Render
