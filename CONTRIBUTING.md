# Avant toute chose...
 1. Vérifiez que vous disposez d'[un compte Github](https://github.com/signup/free)
 2. Créez votre _issue_ si elle n'existe pas
     * Vérifiez que vous possédez bien la dernière version du code
     * Décrivez clairement votre problème, avec toutes les étapes pour le reproduire
 3. **Attribuez-vous** votre _issue_. C'est important pour éviter de se marcher dessus. Si vous n'êtes pas dans l'organisation et donc que vous ne pouvez pas vous attribuer directement l'_issue_, il vous suffit d'ajouter un commentaire clair dans celle-ci (comme _"Je prends"_), et est sera marquée comme "en cours").
 4. _Forkez_ le dépôt
 5. Installez l'environnement. Pour cela, lisez le fichier README.md et suivez la doc.
 
# Contribuer à PortailVA
1. Sur votre *fork*, créez une branche pour contenir votre travail
2. Faites vos modifications
3. Assurez-vous que le code suit les bonnes pratiques (la [PEP-8](http://legacy.python.org/dev/peps/pep-0008/))
4. Si vous modifiez le modèle (les fichiers models.py), n'oubliez pas de créer les fichiers de migration : `python manage.py makemigrations`
5. Si votre travail nécessite des actions spécifiques lors du déploiement, précisez-les dans votre _issue_
6. Poussez votre travail et faites une _Pull Request_

# Quelques bonnes pratiques
* Respectez [les conventions de code de Django](https://docs.djangoproject.com/en/1.10/internals/contributing/writing-code/coding-style/), ce qui inclut la [PEP 8 de Python](http://legacy.python.org/dev/peps/pep-0008/)
* Le code et les commentaires sont en anglais
* Le _workflow_ Git utilisé est le [Git flow](http://nvie.com/posts/a-successful-git-branching-model/). En détail :
    * Les arrivées de fonctionnalités et corrections de gros bugs se font via des PR.
    * Ces PR sont unitaires. Aucune PR qui corrige plusieurs problèmes ou apporte plusieurs fonctionnalité ne sera logiquement accepté ; la règle est : une fonctionnalité ou une correction = une PR.
    * Ces PR sont mergées dans la branche `dev` (appelée `develop` dans le git flow standard), après une revenue de code légère.
    * Pensez à préfixer vos branches selon l'objet de votre PR : `hotfix-XXX`, `feature-XXX`, etc.
    * La branche `master` contient exclusivement le code en production, vous ne devez donc pas faire vos _commit_ dessus !
    
Tous les détails sur le workflow se trouvent [sur la page dédiée](http://portailva.readthedocs.org/fr/latest/workflow.html).

* Faites des messages de _commit_ clairs et en anglais si possible

# Les bonnes pratiques pour les PR et les commits
## Les Pull-Requests
* Lors de l'ouverture d'une PR, essayez de respecter le template suivant :

    ```markdown
    | Q                             | R
    | ----------------------------- | -------------------------------------------
    | Correction de bugs ?          | [oui|non]
    | Nouvelle Fonctionnalité ?     | [oui|non]
    | Tickets (_issues_) concernés  | [Liste de tickets séparés par des virgules]
    ```

## Les commits
* Pour les commits, nous suivons le même ordre d'idée des standards Git, à savoir :
    * La première ligne du commit ne doit pas faire plus de 50 caractères
    * Si besoin, complétez votre commit via des commentaires, en respectant une limite de 70 caractères par ligne
    * Vous pouvez également (c'est d'ailleurs conseillé) référencer l'_issue_ que vous fixez
    * Un commit doit être atomique ; il fixe / implémente **une** chose et le fait **bien**

* Essayez d'éviter les commits dits inutiles (`fix previous commit`, ...). Si vous en avez dans votre *Pull Request*,
  on vous demandera probablement de faire un `squash` de vos commits.

N'hésitez pas à demander de l'aide, et bon courage !