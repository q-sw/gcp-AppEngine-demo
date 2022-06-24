# gcp-AppEngine-demo

Application Flask de test pour Google App Engine Standard

L'objectif à travers ce repository est de déployer une application, développée avec le framework python Flask, sur [Google App Engine](https://cloud.google.com/appengine).  
L'application est une bibliothèque de slides.  Les slides sont sous la forme d'image, stocké dans [Cloud Storage](https://cloud.google.com/storage).  

## Mise en place de l'environnement Cloud

> l'ensemble des instructions supposent que vous soyer déjà en pocession d'un compte GCP fonctionnel.

- Lancez une [Cloud Shell](https://cloud.google.com/shell)
- Clone le repository dans votre espace de travail **Cloud Shell**

```bash
git clone https://github.com/q-sw/gcp-AppEngine-demo.git
```

- Création du projet GCP

```bash
gcloud projects create prj-demo-appeng
```

- Configuration du shell pour utiliser le projet précedement créé

```bash
gcloud config set project prj-demo-appeng
```

- Activation, des services nécessaires pour le bon fonctionnement de l'application.

```bash
gcloud services enable iamcredentials.googleapis.com
```

## Création des Buckets Cloud Storage

> Pour les besoins de l'application, il faut créer des buckets pour stocker les slides et les thumbnails.

- Création du bucket pour le thumbnails

```bash
gsutil mb -l EUROPE-WEST9 -b on gs://<bucket-prefix>-demo-thumbnails 
```

Pour que l'application accès aux images, il faut faire en sorte que les objets du bucket soient public mais uniquement accessible pour les utilisateurs authentifiées.
> dans la cadre de l'application, ca sera le service account de App Engine qui fera les appels aux objets

- Changement des permissions du bucket

```bash
gsutil iam ch allAuthenticatedUsers:objectViewer gs://<bucket-prefix>-demo-thumbnails
```

Répetez les mêmes actions pour créer le bucket qui stockera les images des slides. On remplacera `<bucket-prefix>-demo-thumbnails` par `<bucket-prefix>-demo-slides1`  

Pour télécharger les images vers **Cloud Storage** utilisez la commande ci-dessous

```bash
gsutil rsync <chemin du dossier avec les images> gs://<bucket-prefix>-demo-thumbnails
```  

## Déploiement de l'application  

Ce mettre dans le dossier **gcp-AppEngine-demo**  
Pour faire donner les informations à App-Engine de quel sont les buckets utilisés, on utilise le paramètre `env_variables` du fichier [app.yaml](app.yaml). Les informations seront donc passées en variables d'environnement.  
Les variables suivantes sont à remplir de la manière suivantes:  

- thumbnail_bucket: `<bucket-prefix>-demo-thumbnails`  
- prez_cloud_bucket: `<bucket-prefix>-demo-slides1`  

Une fois le fichier mis à jour, on peut déployer l'application.

```bash
gcloud app deploy
```

Une fois l'application déployée, il faut donner l'authorisation au service account APP Engine le droit de créer des token pour s'authentifier à Cloud Storage.

```bash
gcloud projects add-iam-policy-binding --member=serviceAccount:<service account email> --role=roles/iam.serviceAccountTokenCreator <project-id>
```

## Accéder à l'application

```bash
gcloud app broswe
```
