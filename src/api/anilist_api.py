import requests

class JikanAPI:
    def __init__(self):
        self.base_url = "https://api.jikan.moe/v4"

    def search_manga(self, query):
        url = f"{self.base_url}/manga"
        params = {"q": query, "limit": 1}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data["data"]:
                return None
            manga = data["data"][0]
            # Récupérer les genres
            genres = [g["name"] for g in manga.get("genres", [])] if manga.get("genres") else ["Not specified"]
            # Récupérer l'auteur
            author = manga.get("authors", [{}])[0].get("name", "Unknown")
            # Nombre de tomes
            num_volumes = manga.get("volumes") or 0
            # Créer la liste des tomes (si info dispo)
            volumes = []
            if num_volumes and isinstance(num_volumes, int):
                for i in range(num_volumes):
                    volumes.append({"number": i+1, "title": f"Volume {i+1}"})
            return {
                "id": manga["mal_id"],
                "title": manga.get("title", "Unknown title"),
                "author": author,
                "genres": genres,
                "volumes": num_volumes if num_volumes else "Not specified",
                "volumes_list": volumes,
                "image_url": manga.get("images", {}).get("jpg", {}).get("large_image_url"),
                "synopsis": manga.get("synopsis", "No synopsis available"),
                "status": manga.get("status", "Unknown")
            }
        except Exception as e:
            print(f"Error during Jikan search: {e}")
            return None 