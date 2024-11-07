import requests


def get_img_unsplash(api_key, query, cantidad=10):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={api_key}&per_page={cantidad}"
    response = requests.get(url)
    datos = response.json()
    return [foto["urls"]["regular"] for foto in datos["results"]]
