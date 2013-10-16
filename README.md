Projet Web Master 2
===================

Mise en place du code
---------------------

    :::console
    sudo apt-get install python-dev python-virtualenv
    virtualenv pweb-env
    cd pweb-env
    source bin/activate
    git clone https://github.com/poulp/projetwebm2.git
    cd projetwebm2/pweb
    pip install -r req.txt
    ./manage.py syncdb
    ./manage.py migrate
    
Pour lancer le serveur (http://localhost:8000):

    :::console
    ./manage.py runserver


