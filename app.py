from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
        <h1>Olá, mundo!</h1>
        <h2><b>:D</b></h2>
    """

@app.route("/sobre")
def sobre():
    return """
        <h1>Sobre</h1>
        <p>Este site foi criado por <b>Jéssica Avelar</b>.</p>
    """
