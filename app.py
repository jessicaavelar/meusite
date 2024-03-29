import requests
import os
from flask import Flask, render_template, request

from covid_pr import dados_covid_pr
from noticias_yanomami import noticias_site


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
    
    token = os.environ["TELEGRAM_TOKEN"]
    mensagem = {"chat_id": chat_id, "text": resposta}
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data = mensagem)
    
    return "ok"
