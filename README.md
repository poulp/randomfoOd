# Projet Web Master 2

## Installation

### 1. Récupérer le code du projet
    
    $ git clone https://github.com/poulp/projetwebm2.git

### 2. Installer `virtualenvwrapper` et créer un environnement `pweb-env`
Voir la [doc](http://virtualenvwrapper.readthedocs.org/en/latest/) pour l'installation.

Pour créer l'environnement : 

    $ mkvirtualenv pweb-env --python=python2.7

### 3. Installer les prérequis et configurer
    
    $ workon pweb-env
    $ cd projetwebm2/pweb
    $ pip install -r req.txt
    $ ./manage.py syncdb
    $ ./manage.py migrate


## Mise en route

Lancer le serveur

    ./manage.py runserver


Aller à l'adresse [http://localhost:8000](http://localhost:8000)