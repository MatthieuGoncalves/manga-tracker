from src.api.jikan_api import JikanAPI

# Créer une instance de l'API
api = JikanAPI()

# Chercher un manga
result = api.search_manga("One Piece")

# Afficher le résultat
if result:
    print("Manga trouvé :")
    print(f"Titre : {result['title']}")
    print(f"Auteur : {result['author']}")
    print(f"Genres : {', '.join(result['genres'])}")
    print(f"Nombre de tomes : {result['volumes']}")
    print(f"Image : {result['image_url']}")
else:
    print("Aucun manga trouvé")