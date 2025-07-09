import json
import os

class FavoritesManager:
    def __init__(self):
        # Utiliser un chemin absolu pour le fichier de favoris
        self.favorites_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "favorites.json")
        # Créer le dossier database s'il n'existe pas
        os.makedirs(os.path.dirname(self.favorites_file), exist_ok=True)
        self.favorites = self.load_favorites()

    def load_favorites(self):
        """Charge les favoris depuis le fichier JSON"""
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_favorites(self):
        """Enregistre les favoris dans le fichier JSON"""
        with open(self.favorites_file, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=4)

    def add_favorite(self, manga_id, manga_data):
        """Ajoute un manga aux favoris"""
        manga_id = str(manga_id)
        self.favorites[manga_id] = {
            'title': manga_data['title'],
            'author': manga_data['author'],
            'genres': manga_data['genres'],
            'volumes': manga_data['volumes'],
            'image_url': manga_data['image_url'],
            'read_volumes': []  # Liste des tomes lus
        }
        self.save_favorites()

    def remove_favorite(self, manga_id):
        """retire un manga des favoris"""
        manga_id = str(manga_id)  # Convertir en string pour être sûr
        if manga_id in self.favorites:
            del self.favorites[manga_id]
            self.save_favorites()
    
    def is_favorite(self, manga_id):
        """Vérifie si un manga est dans les favoris"""
        return str(manga_id) in self.favorites
    
    def get_all_favorites(self):
        """Retourne tous les favoris"""
        return self.favorites

    def toggle_volume_read(self, manga_id, volume_number):
        """Marque un tome comme lu ou non lu"""
        manga_id = str(manga_id)
        if manga_id in self.favorites:
            if volume_number in self.favorites[manga_id]['read_volumes']:
                self.favorites[manga_id]['read_volumes'].remove(volume_number)
            else:
                self.favorites[manga_id]['read_volumes'].append(volume_number)
            self.save_favorites()

    def is_volume_read(self, manga_id, volume_number):
        """Vérifie si un tome est marqué comme lu"""
        manga_id = str(manga_id)
        return manga_id in self.favorites and volume_number in self.favorites[manga_id]['read_volumes']
  