from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
        <h1>Olá, <b>mundo</b>!</h1>
        <p><b>:D</b></p>
    """

@app.route("/sobre")
def sobre():
    return """
        <h1>Sobre</h1>
        <p>Este site foi criado por <b>Jéssica Avelar</b>.</p>
    """
