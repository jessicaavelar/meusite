import requests
from bs4 import BeautifulSoup as bs 


def noticias_site():
    site = "https://terrasindigenas.org.br/noticias/4016/TI/500/1"
    r = requests.get(site)
    html = bs(r.text, "html.parser")

    lista = html.find("ul", {"id": "list-noticias"})
    tag_a = lista.find_all("a")
    
    noticias_ti = []
    for tag in tag_a:
        texto = tag.text
        titulo = texto.split("-")
        url = "https://terrasindigenas.org.br" + tag.attrs["href"]
        noticias_ti.append({
            "data": titulo[0],
            "titulo": titulo[1],
            "link": url,
        })
    return noticias_ti
