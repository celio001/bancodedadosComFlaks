from flask import Flask, render_template, request
import urllib.request, json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
frutas = []
registros = []
@app.route('/', methods=['GET', 'POST'])
def principal():
    #frutas = ["Morango", "Uva", "laranja","Mamão","Maça"]
    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))
    return render_template("index.html", frutas=frutas)

@app.route('/sobre', methods=['GET', 'POST'])
def sobre():
    if request.method == 'POST':
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({'aluno': request.form.get('aluno'), 'nota': request.form.get('nota')})
    return render_template("sobre.html", registros=registros)

@app.route('/filmes/<propriedades>')
def filmes(propriedades):

    if propriedades == 'populares':
        popularApi = os.environ['POPULARES_API']
        resposta = urllib.request.urlopen(popularApi)

    elif propriedades == 'kids':
        kidsApi = os.environ['KIDS_API']
        resposta = urllib.request.urlopen(kidsApi)

    elif propriedades == '2010':
        Api_2010 = os.environ['2010_API']
        resposta = urllib.request.urlopen(Api_2010)

    elif propriedades == 'drama':
        dramaApi = os.environ['DRAMA_API']
        resposta = urllib.request.urlopen(dramaApi)

    dados = resposta.read()

    jsondata = json.loads(dados)

    return render_template("filmes.html", filmes=jsondata['results'])

app.run(debug=True)