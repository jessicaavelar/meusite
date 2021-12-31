import csv
import datetime
import io
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template


def dados_covid_pr():
    hoje = datetime.datetime.now().date()
    ontem = hoje - datetime.timedelta(days=1)
    for data in (hoje, ontem):
        url = f"https://www.saude.pr.gov.br/sites/default/arquivos_restritos/files/documento/{data.year}-{data.month:02d}/INFORME_EPIDEMIOLOGICO_{data.day:02d}_{data.month:02d}_{data.year}_OBITOS_CASOS_Municipio.csv"
        resposta = requests.get(url)
        if resposta.ok:
            conteudo = resposta.content.decode(resposta.apparent_encoding)
            break
  
    casos = 0
    obitos = 0
    leitor = csv.DictReader(io.StringIO(conteudo), delimiter=";")
    for registro in leitor:
        casos += int(registro["Casos"])
        obitos += int(registro["Obitos"])

    return data, casos, obitos
    
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
    arquivo = open("templates/home.html")
    return arquivo.read()

@app.route("/sobre")
def sobre():
    arquivo = open("templates/sobre.html")
    return arquivo.read()

@app.route("/covid-pr")
def covid_pr():
    data_boletim, casos_pr, obitos_pr = dados_covid_pr()
    return render_template(
        "covid-pr.html",
        data = data_boletim,
        casos = casos_pr,
        obitos = obitos_pr
    )


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
        {noticias}
    </p>
    """
