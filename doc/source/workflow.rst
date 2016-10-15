===============================
*Workflow* et détails pratiques
===============================

Cette page, fortement inspirée du projet [Zeste de Savoir](https://github.com/zestedesavoir/zds-site/), détaille le
*workflow* utilisé lors du développement de PortailVA. La `page de contribution <https://github.com/VAINSALyon/portailva/blob/dev/CONTRIBUTING.md>`__
devrait répondre à vos questions quant au processus de développement. Ici seront aussi décrits quelques détails sur la
gestion des tickets sur Github (*tagging* et priorité).

Ce *workflow* est très fortement basé sur le `Git flow <http://nvie.com/posts/a-successful-git-branching-model/>`__.

*Workflow* général
==================

Le dépôt de PortailVA est organisé comme suit :

- Le développement se fait sur la branche ``dev`` ;
- La branche ``master`` contient la version en production ;
- En cas de bug très urgent à corriger en production, une branche spéciale est créée (`hotfix <http://nvie.com/posts/a-successful-git-branching-model/#hotfix-branches>`__).

Une version de pré-production (ou bêta) sera bientôt disponible en ligne.

*Workflow* de développement
===========================

Description
-----------

1. Les fonctionnalités et corrections de bugs se font via des *Pull Requests* (PR) depuis des *forks* via `Github <https://github.com/VAINSALyon/portailva>`_.
2. Ces PR doivent être autant que possible unitaires. C'est-à-dire qu'une PR ne doit corriger qu'un seul problème ou
n'apporter qu'une seule fonctionnalité. La règle est : une PR = une fonctionnalité ou une correction.
3. Ces PR sont mergées dans la branche ``dev`` (appelée ``develop`` dans le git flow standard), après une revue rapide.
4. La branche ``master`` contient exclusivement le code en production, aucun *commit* n'est donc autorisé sur cette branche
en temps normal !
5. Les branches du dépôt principal (``dev`` et ``master``) ne devraient contenir que des merges de PR, aucun *commit*
direct.

Milestone
---------

Pour avoir une vue d'ensemble des modifications inclues ou à inclure dans chaque phase de mise en production, nous utilisons
des *milestones*. Il existe une *milestone* par release majeure ; les PRs mergées dans une version mineure appartement à
la *milestone* de la version majeure correspondante.

Toute PR se voit attribuer une *milestone*. Elle est attribuée au plus tôt à l'ouverture de la PR si cette PR doit impérativement
passer dans la prochaine release, au plus tard par la personne qui merge la PR lors de son merge. Bien qu'une PR doit généralement
être atomique, il arrive qu'elle ait pour effet secondaire de régler plusieurs bugs et d'introduire plusieurs fonctionnalités.
Dans ces rares cas, chaque ticket fermé par effet secondaire d'une PR peut également recevoir une *milestone*.

* Toute PR mergée dans ``dev`` doit porter la *milestone* « Version de développement »
* Toute PR mergée ailleurs (``prod`` en cas de hotfix par exemple) doit porter la *milestone* « Version N »

La *milestone* « Version de développement » s'appelle comme ça parce qu'elle contient les modifications apportées depuis
la dernière mise en production. Cette *milestone* étant largement la plus utilisée, son nom a l'avantage qu'on voit immédiatement
si l'on attribue ou non la bonne *milestone*, sans avoir à réfléchir au numéro de version.

Lors de la clôture de chaque release, la *milestone* « Version de développement » est renommée « Version N » et une nouvelle
*milestone* « Version de développement » est créée.

Stratégie de *tagging* des tickets
==================================

Les étiquettes (ou *labels* ou *tags*) utilisées pour classifier les tickets sont classées en 4 catégories (seuls les niveaux
2 représentent les tags utilisables) :

-  C: Compétence

   -  C-Back
   -  C-Front
   -  C-API
   -  C-Documentation
   -  C-Infra

-  P: Priorité

   -  P-Bloquant
   -  P-Haute
   -  P-Basse

-  S: Statut

   -  S-Evolution
   -  S-Bug
   -  S-Régression
   -  S-Zombie

-  Autres

   -  Facile
   -  Feedback

Explications
------------

-  Compétence : Quelle(s) partie(s) du système est/sont impactée(s) ? Permet notamment aux développeurs de choisir de se
concentrer uniquement sur le front, aux admins de s'occuper de l'infra, etc.
-  Priorité : Un **bug** ou une **régression** est **bloquant**e si cela empêche une utilisation correcte du site (impossible
de se connecter, d'uploader un document ou forte atteinte aux performances, etc). Il s'agit d'un problème critique. Les
autres tickets ou PR peuvent être de **Haute** ou **Basse** priorité, ces étiquettes étant facultatives.
-  Statut : **Régression** ou **Bug** ? : Une régression est un retour en arrière en terme de qualité. Il s'agit d'un bug,
mais on le différencie parce que ce bug vient d'être introduit dans une partie du code qui auparavant fonctionnait comme
voulu. Un problème qui n'est pas une régression est indiqué *Bug*. Il s'agit par exemple d'un problème impactant une nouvelle
 fonctionnalité. Les tickets sous le tag **Zombie** sont des bugs mineurs n'ayant pas donnés signe de vie depuis longtemps.
 Ils sont donc non-résolus mais fermés et placés sous cette étiquette pour garder propre la pile des tickets actifs. Dans
 l'idéal il faudrait les rouvrir pour les résoudre un jour.
-  Le tag **Facile** : Ce tag est là uniquement pour guider les nouveaux contributeurs vers des tâches accessibles. Pour
pouvoir utiliser cette étiquette, une proposition de solution doit être écrite dans le ticket.
-  Le tag **Feedback** : Ce tag indique les tickets sur lesquels l'auteur souhaite recevoir un retour, discuter une approche,
proposer quelque chose, ouvrir le débat.

La priorité est mise sur ce qui est Bloquant, puis Haut. Les autres tickets ou PRs n'ont pas de priorité particulière. La
basse priorité vient en dernier. Chacun est invité à choisir ce sur quoi concentrer ses efforts en fonction de ces priorités
ou de ses intérêts.

