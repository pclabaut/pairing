## Logiciel de pairing en équipe de 8 joueurs (format worlds)

Cet outil a pour but de :
- [manuel] gérer la mécanique de pairing pour des essais effectués par une seule personne (il entre ses choix et ceux de l'adversaire.
- [training] simuler un partenaire de pairing pour le jeu en équipe de 8 AOS (work in progress).
- [bot] conseiller les meilleurs mouvements à un capitaine pour le pairing du jeu en équipe de 8 AOS (work in progress).

### Obtention

Il suffit de télécharger le dossier (onglet code -> download zip) puis de le dézipper à l'endroit souhaité.

### Pré-requis :

- python3
- jupyter 
- pandas

Python et jupyter peuvent être installés et obtenus facilement via Anaconda :
https://www.anaconda.com/products/distribution 

Le tutorial suivant guidera l'utilisateur pour :
- l'obtention d'Anaconda (et, inclus, de python et jupyter)
- l'instalation d'un module (ici : pandas)
- le lancement de jupyter et l'ouverture d'un notebook (il faudra naviguer dans ses répertoires pour se placer dans celui où se trouvent les fichiers de ce logiciel)
https://www.data-transitionnumerique.com/anaconda-python/

NB: Bien que jupyter ouvre un notebook sur votre navigateur web, il n'est PAS en ligne mais bien sur votre machine (localhost).

### Fichiers

Le fichier mypairing.xlsx est utilisé pour passer les estimés de l'équipe au programme.
Il est structuré en 4 feuilles (noms indifférents), comprenant les tableaux de pairing avec les factions du capitaine en tête de lignes et celles de son opposant en colonne.
Les noms des BT des deux équipes sont lues par le logiciel dans les premières lignes et colonnes de la première feuille uniquement. 
Ils sont répliqués sur les feuilles suivantes uniquement pour une plus grande facilité de lecture humaine et garder les cellules des pairings aux mêmes coordonées entre les pages.

Le fichier "Pairing.ipynb" contient le code python du programme et est à lancer via jupyter.

### Utilisation

Il suffit de lancer l'execution de la totalité des cellules (bouton en double chevron) et de ce laisser guider par les instructions.
Le mode le plus abouti pour le moment est le mode 'manuel'.
Pour relancer un pairing, relancer la dernière cellule seulement suffit, pas besoin de relancer tout le notebook.

### Licence 
Ce logiciel est distribué sous la licence EUPL dont une copie est fournie dans le fichiers licence.md
