Manga Tracker

Manga Tracker est une application Python avec interface graphique (Tkinter) permettant de rechercher des mangas, d’afficher leurs informations, de gérer ses favoris et de suivre les tomes lus.

Fonctionnalités

🔎 Recherche de mangas via l’API Jikan (MyAnimeList)
📖 Affichage : titre, auteur, genres, nombre de tomes, image, synopsis, statut
⭐ Ajout/suppression de mangas dans les favoris
✅ Suivi des tomes lus (checkbox)
🎨 Interface graphique moderne et intuitive
💾 Gestion locale des favoris (pas de compte requis)

Installation

git clone https://github.com/MatthieuGoncalves/manga-tracker.git
cd manga-tracker
pip install -r requirements.txt
python src/gui/main_window.py

Dépendances

Python 3.8+
Tkinter (inclus avec Python)
Pillow (pour l’affichage des images)
requests (pour les requêtes API)

Améliorations futures

[ ] Utiliser une base de données plus complète et fiable
(Ex : récupération d’informations plus précises sur les auteurs, le nombre de tomes, les couvertures, etc.)
[ ] Amélioration graphique de l’interface
(Design plus moderne, couleurs personnalisables, polices stylées, animations, etc.)
[ ] Ajout de fonctionnalités visuelles avancées
(Mode sombre, thèmes personnalisables, transitions, effets visuels)
[ ] Affichage de plusieurs résultats de recherche en grille
[ ] Filtrage et tri avancés
(par genre, statut, nombre de tomes, popularité…)
[ ] Export/Import des favoris
[ ] Notifications ou rappels pour les nouveaux tomes
[ ] Packaging en exécutable (.exe, .app) pour une installation facile
