# Correcteur d'actes

Application web pour corriger sur iPhone, sans connexion, les lignes lues par Kraken.
Elle lit les fichiers ALTO et PAGE XML avec leurs images, et renvoie les XML corrigés.

## Mise en ligne (une seule fois)

1. Créer sur GitHub un dépôt **public** nommé `correcteur-actes`, car GitHub Pages
   n'est gratuit que pour les dépôts publics. Seul le code y figure, aucune image d'archive.
2. Y déposer `index.html`, `sw.js`, `manifest.webmanifest` et les trois icônes `.png`.
3. Dans Settings, puis Pages, choisir « Deploy from a branch », branche `main`, dossier `/ (root)`.
4. L'adresse sera de la forme `https://auxb.github.io/correcteur-actes/`.

## Installation sur l'iPhone

1. Ouvrir l'adresse dans Safari.
2. Bouton Partager, puis « Sur l'écran d'accueil ».
3. Ouvrir le Correcteur **depuis son icône** et importer les pages là, jamais dans Safari,
   car les deux ne partagent pas leurs données et seule l'icône fonctionne hors ligne.

Il faut iOS 16.4 ou plus récent pour ouvrir les archives zip.

## Préparer un lot sur le Mac

Dans le Finder, compresser le dossier qui contient les images et leurs XML (clic droit,
« Compresser »), puis l'envoyer par AirDrop. Sur l'iPhone, l'enregistrer dans Fichiers,
puis Importer dans l'application. On peut aussi sélectionner directement des XML et leurs images.

## Rapporter les corrections

1. Dans l'application, Exporter, puis Préparer le fichier, puis Partager (AirDrop vers le Mac).
2. Sur le Mac, depuis le dossier `actes` :

   ```bash
   python3 correcteur/integrer_corrections.py ~/Downloads/corrections_AAAA-MM-JJ_HHhMM.zip --essai
   python3 correcteur/integrer_corrections.py ~/Downloads/corrections_AAAA-MM-JJ_HHhMM.zip
   ```

   La première commande montre ce qui sera fait, la seconde remplace les XML et copie
   les anciennes versions dans `_sauvegardes_corrections/`.

Chaque export contient toutes les corrections faites jusqu'ici, donc le plus récent suffit.

## Mettre à jour l'application

Après une modification de `index.html`, changer `VERSION` dans `sw.js` avant de pousser.
L'iPhone affiche l'ancienne version au lancement suivant, puis la nouvelle au d'après.
