## Logiciel de pairing en équipe de 8 joueurs

Cet outil a pour but de :
- simuler un partenaire de pairing pour le jeu en équipe de 8 AOS (format Worlds)
- conseiller les meilleurs mouvements à un capitaine pour le pairing du jeu en équipe de 8 AOS (format Worlds)

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

NB: Bien que jupyter ouvre un notebook sur votre navigateur web, il n'est PAS en ligne mais bien sur votre machine.

### Fichiers

Le fichier mypairing.xlsx est utilisé pour passer les estimés de l'équipe au programme.
Il est structuré en 4 feuilles (noms indifférents), comprenant les tableaux de pairing avec les listes du capitaine en lignes et celles de son opposant en colonne.
Les noms des BT des deux équipes sont lues par le logiciel dans les premières lignes et colonnes de la première feuille uniquement. 
Ils sont répliqués sur les feuilles suivantes uniquement pour une plus grande facilité de lecture humaine.

Le fichier "Pairing.ipynb" contient le code python du programme et est à lancer via jupyter.

### Utilisation

Il suffit de lancer l'execution de la totalité des cellules (bouton en double chevron) et de ce laisser guider par les instructions.
Pour relancer un pairing, relancer la dernière cellule seulement suffit.

### Licence 
Ce logiciel est distribué sous la licence EUPL dont une copie est fournie dans le fichiers licence.md