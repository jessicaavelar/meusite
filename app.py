import requests
from bs4 import BeautifulSoup as bs
from flask import Flask


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


app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
        <h1>
            Olá, mundo!
        </h1>
        <a href="/noticias-yanomami">Notícias Yanomami</a> - <a href="/sobre">Sobre este site</a>
        <h2>
            <b>:D</b>
        </h2>
    """

@app.route("/sobre")
def sobre():
    return """
        <h1>
            Sobre
        </h1>
        <a href="/">Página Inicial</a> - <a href="/noticias-yanomami">Notícias Yanomami</a>
        <p>
            Este site foi criado por <b>Jéssica Avelar</b>.
        </p>
    """

@app.route("/noticias-yanomami")
def noticias():
    noticias = noticias_site()
    
    return f"""
    <h1> Notícias Yanomami </h1>
    <a href="/">Página Inicial</a> - <a href="/sobre">Sobre este site</a>
    <p>
        <b>Notícias do Território Yanomami:</b>
    </p>
    <p>
        {noticias["link"]}
    </p>
    """
