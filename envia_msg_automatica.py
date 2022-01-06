import requests
import os
from covid_pr import dados_covid_pr


data, casos, obitos = dados_covid_pr

token = os.environ["TELEGRAM_TOKEN"]
url = f"https://api.telegram.org/bot{token}/sendMessage"
chat_id = 5023867801
texto = f"Olá!\nAcabei de capturar dados de COVID-19 do Paraná para a data {data}.\nCasos: {casos}\nÓbitos: {obitos}"
mensagem = {"chat_id": chat_id, "text": texto }
requests.post(url, data = mensagem)
