from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "super secret key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.sqlite3"

db = SQLAlchemy(app)

frutas = []
registros = []

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch

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

@app.route('/cursos')
def lista_cursos():
    page = request.args.get('page', 1, type=int)
    todos_cursos = cursos.query.paginate(page=page, per_page=4)
    return render_template("cursos.html", cursos=todos_cursos)

@app.route('/cria_curso', methods=['GET', 'POST'])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == 'POST':
        if not nome or not descricao or not ch:
            flash("Preench todos os campos do formulário", "erro")
        else:
            curso = cursos(nome, descricao, ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))

    return render_template('novo_curso.html')

@app.route('/<int:id>/atualiza_curso', methods=['GET', 'POST'])
def atualiza_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        ch = request.form['ch']

        cursos.query.filter_by(id=id).update({'nome':nome, 'descricao': descricao, 'ch': ch})
        db.session.commit()
        return redirect(url_for('lista_cursos'))

    return render_template("atualizar_curso.html", curso=curso)

@app.route('/<int:id>/remove_curso')
def remove_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('lista_cursos'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)