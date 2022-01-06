import csv
import datetime
import io
import requests


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
