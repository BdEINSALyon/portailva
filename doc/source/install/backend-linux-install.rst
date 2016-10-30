====================================
Installation de PortailVA sous Linux
====================================

Pour installer une version locale de PortailVA sur GNU/Linux, veuillez suivre les instructions suivantes.

- Si une commande ne passe pas, essayez de savoir pourquoi avant de continuer.
- Si vous voulez savoir ce qui se cache derrière une commande ``make``, ouvrez le fichier nommé ``Makefile`` présent à la racine du projet.
- Si une erreur s'est glissée dans la doc, ou si la doc est obsolète, ouvrez `un ticket sur notre dépôt github <https://github.com/VAINSALyon/portailva/issues/new>`_
- Si malgré tout vous ne parvenez pas à installer PortailVA, n'hésitez pas à `nous contacter <dev-portailva@googlegroups.com>`_

**Attention** : la procédure décrite dans ce guide sert à l'installation d'une instance de développement de PortailVA. Si vous souhaitez déployer une instance de production, nous vous préconisons l'utilisation de Docker.

Prérequis
=========

Certaines des commandes d'installation (débutant par ``apt-get``) sont données ici pour Ubuntu et ses dérivés, pour lesquels il est sûr qu'elles fonctionnent. Si vous utilisez une distribution différente, le nom des paquets à installer devrait être fort semblables, n'hésitez dès lors pas à employer la fonction "recherche" de votre gestionnaire de paquet préféré. Les autres commandes sont génériques et indépendantes de la distribution utilisée.

PortailVA a besoin des dépendances suivantes :

- git : ``apt-get install git``
- python3 : ``apt-get install python3``
- python-dev : ``apt-get install python3-dev``
- pip : ``apt-get install python3-pip``
- libpq-dev : ``apt-get install libpq-dev``
- npm : ``apt-get install npm``

Récupération des sources et configuration de `virtualenv`
=========================================================

Nous vous conseillons de créer un utilisateur dédié à PortailVA (nommé ``portailva`` pour les besoins de cette documentation). Les sources seront téléchargées dans le répertoire de cet utilisateur.

.. sourcecode:: bash

    git clone https://github.com/VAINSALyon/portailva.git portailva
    cd portailva
    virtualenv venv # Création de l'environnement Python virtuel

**À chaque fois** que vous souhaitez travailler dans votre environnement, activez-le via la commande suivante :

.. sourcecode:: bash

    source venv/bin/activate # PAS sudo

Pour sortir de votre environnement, tapez ``deactivate``.

Une documentation plus complète de cet outil `est disponible ici <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.


Installation des dépendances
============================

Le projet fait appel au gestionnaire ``npm`` pour récupérer un certain nombre de dépendances. Il est donc nécessaire d'installer Node.js :

.. sourcecode:: bash

    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash - # Ajout des dépôts de Node.js au gestionnaire de packages
    sudo apt-get install nodejs

Nous pouvons ensuite poursuivre avec l'installation des dépendances :

.. sourcecode:: bash

    pip install -r requirements.txt
    npm install
    sudo npm install -g gulp # Installation du binaire de Gulp
    gulp build # Génération des css/js/sprites


Lancer PortailVA
================

Une fois dans votre environnement python (``source venv/bin/activate`` si vous utilisez virtualenv, très fortement conseillé), lancez ces deux commandes.

.. sourcecode:: bash

    python manage.py migrate # Permet la création ou mise à jour du schéma de base de données
    python manage.py runserver # Lance le serveur de développement

