import csv
import datetime
import io
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template


def dados_covid_pr():
    hoje = datetime.datetime.now().date()
    ontem = hoje - datetime.timedelta(days=1)
    conteudo = None
    for data in (hoje, ontem):
        url1 = f"https://www.saude.pr.gov.br/sites/default/arquivos_restritos/files/documento/{data.year}-{data.month:02d}/INFORME_EPIDEMIOLOGICO_{data.day:02d}_{data.month:02d}_{data.year}_OBITOS_CASOS_Municipio.csv"
        url2 = url1.lower()
        for url in (url1, url2):
            resposta = requests.get(url)
            if resposta.ok:
                conteudo = resposta.content.decode(resposta.apparent_encoding)
                break
        if conteudo:
            break
    if not conteudo:
        return None, None, None
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
    return render_template("home.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


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
    not_ti = noticias_site()
    return render_template(
        "yanomami.html",
        noticias = not_ti
    )


from flask import request
import requests

@app.route("/telegram", methods = ["POST"])
def telegram():

    dados = request.json
    chat_id = dados["message"]["chat"]["id"]
    texto = dados["message"]["text"].lower()
    if texto in ["oi", "ola", "olá", "olar", "hello"]:
        resposta = "Olá, tudo bem?"
    elif texto in ["buenas", "buenos", "bom dia", "boa tarde", "boa noite"]:
        resposta = texto
    elif "covid" in texto:
        data, casos, obitos = dados_covid_pr()
        resposta = f"As informações que tenho sobre COVID-19 são do estado do Paraná, em {data}: {casos} casos e {obitos} óbitos."
    else:
        resposta = "Oi, como vai? Não entendi."
        
    token = "5004646901:AAGf8yJpBnWDIY-XvGKtCWh2Ib4vVxtFkLk"
    mensagem = {"chat_id": chat_id, "text": resposta}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data = mensagem)
    
    return "ok"


