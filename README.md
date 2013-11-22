# Random recipe generator

## Installation

### 1. Récupérer le code du projet
    
    $ git clone https://github.com/poulp/projetwebm2.git

### 2. Installer `virtualenvwrapper` et créer un environnement `pweb-env`
Voir la [doc](http://virtualenvwrapper.readthedocs.org/en/latest/) pour l'installation.

Pour créer l'environnement : 

    $ mkvirtualenv pweb-env --python=python2.7

### 3. Installer les prérequis et configurer
#### 3.1. Pour l'api
    $ workon pweb-env
    $ cd api
    $ pip install -r req.txt

#### 3.2. Pour l'app
    $ workon pweb-env
    $ cd pweb
    $ pip install -r req.txt
    $ ./manage.py syncdb
    $ ./manage.py migrate


## Mise en route

### 1. Lancer l'api
    $ python api/runserver.py

### 2. Lancer l'app
    $ cd pweb
    $ ./manage.py runserver


Aller à l'adresse [http://localhost:8000](http://localhost:8000) et régalez vous.