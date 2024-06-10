# Spécifier l'image de base
FROM python:3.11-slim

# Ajouter un utilisateur (changez selon vos besoins)
# Empêche l'exécution de commandes sudo
RUN useradd -r -s /bin/bash sora

# Définir l'environnement courant
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

# Mise à jour et installation de libgomp1
RUN apt-get update && apt-get install -y libgomp1

# Changer le propriétaire du répertoire /app à l'utilisateur 'sora'
RUN chown -R sora:sora /app
USER sora

# Définir l'option de configuration de l'application
ENV FLASK_ENV=production

# Définir les variables d'argument dans la commande docker-run
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# Installer les dépendances
ADD ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt --user

# Copier le contenu du répertoire courant dans le conteneur
COPY . /app
WORKDIR /app

# Exécuter les tests unitaires
RUN python -m unittest discover -s /app -p "test_unitaire_api.py"


# Exposer le port sur lequel l'application Flask écoute
EXPOSE 5000

# Commande pour exécuter l'application Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=5"]



