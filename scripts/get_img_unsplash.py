import requests
import random

UNSPLASH_ACCESS_KEY = "tu_clave_de_acceso"


def obtener_imagenes_instrumentos(query, cantidad=10):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page={cantidad}"
    response = requests.get(url)
    datos = response.json()
    return [foto["urls"]["regular"] for foto in datos["results"]]


# Generar una lista de imágenes
imagenes_guitarras = obtener_imagenes_instrumentos("guitarra", 5)
imagenes_pianos = obtener_imagenes_instrumentos("piano", 5)

# Selección aleatoria de URL para un producto
url_imagen = random.choice(imagenes_guitarras + imagenes_pianos)
print(url_imagen)
