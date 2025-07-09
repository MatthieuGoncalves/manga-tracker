import requests
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import ttk
import sys
import os

# Ajouter le dossier parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.api.anilist_api import JikanAPI
from src.database.favorites_manager import FavoritesManager

# Classe principale de l'interface graphique
class MangaTrackerGUI:
    def __init__(self, root):
        # Configuration de la fenêtre principale
        self.root = root
        self.root.title("Manga Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')    # Fond gris clair
        
        # Initialisation de l'API
        self.api = JikanAPI()
        # Initialisation du gestionnaire de favoris
        self.favorites_manager = FavoritesManager()
        
        # Création de l'interface
        self.create_widgets()
        
    def create_widgets(self):
        # Style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 16, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Volume.TButton', font=('Arial', 9))
        style.configure('Volume.TCheckbutton', font=('Arial', 9))
        
        # Titre de l'application
        title_label = tk.Label(
            self.root,
            text="Manga Tracker",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#222222'
        )
        title_label.pack(pady=(20, 20))
        
        # Zone de recherche
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill=tk.X)
        
        # Champ de texte pour la recherche
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40, font=('Arial', 12))
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Bouton de recherche
        search_button = ttk.Button(search_frame, text="Rechercher", command=self.search_manga)
        search_button.pack(side=tk.LEFT, padx=5)

        # Bouton favoris
        favorites_button = ttk.Button(search_frame, text="Favoris", command=self.show_favorites)
        favorites_button.pack(side=tk.LEFT, padx=5)
        
        # Zone d'affichage des résultats
        self.result_frame = ttk.Frame(self.root, padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True)

    def create_manga_display(self, parent, manga_data, manga_id=None):
        """Crée l'affichage d'un manga avec ses informations et tomes"""
        # Frame pour l'image et les infos
        content_frame = ttk.Frame(parent, style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Image du manga
        if manga_data.get('image_url'):
            try:
                response = requests.get(manga_data['image_url'])
                image_data = Image.open(BytesIO(response.content))
                # Redimensionner l'image
                image_data = image_data.resize((200, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image_data)
                
                image_label = ttk.Label(content_frame, image=photo)
                image_label.image = photo  # Garder une référence
                image_label.pack(side=tk.LEFT, padx=20)
            except Exception as e:
                print(f"Error loading image: {e}")
        
        # Frame pour les informations textuelles
        text_frame = ttk.Frame(content_frame, style='TFrame')
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Titre en gras
        title_label = ttk.Label(text_frame, text=manga_data.get('title', 'Unknown title'), style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Auteur
        author_label = ttk.Label(text_frame, text=f"Author: {manga_data.get('author', 'Unknown')}")
        author_label.pack(pady=2)
        
        # Genres
        genres = manga_data.get('genres', ['Not specified'])
        genres_label = ttk.Label(text_frame, text=f"Genres: {', '.join(genres)}")
        genres_label.pack(pady=2)
        
        # Statut
        status_label = ttk.Label(text_frame, text=f"Status: {manga_data.get('status', 'Unknown')}")
        status_label.pack(pady=2)
        
        # Synopsis (uniquement dans la vue recherche)
        if not hasattr(self, 'current_view') or self.current_view != 'favorites':
            synopsis_frame = ttk.LabelFrame(text_frame, text="Synopsis")
            synopsis_frame.pack(fill=tk.X, pady=10)
            synopsis_label = ttk.Label(synopsis_frame, text=manga_data.get('synopsis', 'No synopsis available'), wraplength=400)
            synopsis_label.pack(padx=5, pady=5)
        
        # Bouton pour ajouter/retirer des favoris
        if manga_id is None:
            manga_id = manga_data.get('id')
        favorite_text = "Remove from favorites" if self.favorites_manager.is_favorite(manga_id) else "Add to favorites"
        add_button = ttk.Button(text_frame, text=favorite_text,
                              command=lambda: self.toggle_favorite(manga_id, manga_data))
        add_button.pack(pady=10)

        # Afficher les tomes
        volumes_frame = ttk.LabelFrame(text_frame, text="Volumes")
        volumes_frame.pack(fill=tk.X, pady=10)
        
        # Créer une grille de tomes
        volumes = manga_data.get('volumes_list', [])
        if not volumes:
            vol = manga_data.get('volumes')
            if vol is None or vol == "Not specified":
                num_volumes = 0
            else:
                num_volumes = int(vol)
            volumes = [{"number": i+1, "title": f"Volume {i+1}"} for i in range(num_volumes)]
        
        if volumes:
            # Créer un canvas avec scrollbar pour les tomes
            canvas = tk.Canvas(volumes_frame)
            scrollbar = ttk.Scrollbar(volumes_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Packer le canvas et la scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Créer une grille de tomes dans le frame scrollable
            for i, volume in enumerate(volumes):
                volume_frame = ttk.Frame(scrollable_frame)
                volume_frame.grid(row=i//6, column=i%6, padx=5, pady=5)
                
                # Checkbox pour marquer le tome comme lu
                is_read = self.favorites_manager.is_volume_read(manga_id, volume['number'])
                var = tk.BooleanVar(value=is_read)
                checkbox = ttk.Checkbutton(volume_frame, text=volume['title'],
                                         variable=var,
                                         command=lambda v=volume['number']: self.toggle_volume_read(manga_id, v),
                                         style='Volume.TCheckbutton')
                checkbox.pack()

    def search_manga(self):
        # Effacer les résultats précédents
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        # Définir la vue courante
        self.current_view = 'search'
            
        # Rechercher le manga
        query = self.search_var.get()
        result = self.api.search_manga(query)
        
        if result:
            # Afficher les informations du manga
            info_frame = ttk.Frame(self.result_frame)
            info_frame.pack(fill=tk.BOTH, expand=True)
            self.create_manga_display(info_frame, result)
        else:
            # Message si aucun manga trouvé
            no_result_label = ttk.Label(self.result_frame, text="Aucun manga trouvé")
            no_result_label.pack(pady=20)

    def show_favorites(self):
        # effacer les resultats precedents
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Définir la vue courante
        self.current_view = 'favorites'

        # Cree un titre pour la section favoris
        title_label = ttk.Label(self.result_frame, text="Mes manga favoris", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Créer un canvas avec scrollbar
        canvas = tk.Canvas(self.result_frame)
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Packer le canvas et la scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Recupere tous les favoris
        favorites = self.favorites_manager.get_all_favorites()

        # SI pas de favoris, afficher un message
        if not favorites:
            # message si aucun favoris
            no_favorites_label = ttk.Label(scrollable_frame, text="Vous n'avez aucun manga favoris")
            no_favorites_label.pack(pady=20)
            return
        
        # Pour chaque manga favoris
        for manga_id, manga_data in favorites.items():
            # Cree un frame pour chaque manga
            manga_frame = ttk.Frame(scrollable_frame)
            manga_frame.pack(fill=tk.X, pady=10)
            self.create_manga_display(manga_frame, manga_data, manga_id)

    def toggle_favorite(self, manga_id, manga_data):
        if self.favorites_manager.is_favorite(manga_id):
            self.favorites_manager.remove_favorite(manga_id)
        else:
            self.favorites_manager.add_favorite(manga_id, manga_data)
        # Rafraîchir l'affichage en fonction du contexte
        if hasattr(self, 'current_view') and self.current_view == 'favorites':
            self.show_favorites()
        else:
            self.search_manga()

    def toggle_volume_read(self, manga_id, volume_number):
        """Marque un tome comme lu ou non lu"""
        self.favorites_manager.toggle_volume_read(manga_id, volume_number)
        # Rafraîchir l'affichage
        if hasattr(self, 'current_view') and self.current_view == 'favorites':
            self.show_favorites()
        else:
            self.search_manga()

# Point d'entrée de l'application
def main():
    root = tk.Tk()
    app = MangaTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


        
            
            





        