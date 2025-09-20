# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///doacao.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

# Modelo de Móvel
class Movel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    localizacao = db.Column(db.String(100), nullable=False)
    id_doador = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

# Rota inicial
@app.route("/")
def home():
    return "API de Doação de Móveis funcionando 🪑"

# Rota para criar usuários
@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    dados = request.get_json()

    if not all(k in dados for k in ("nome", "email", "telefone")):
        return jsonify({"erro": "Campos obrigatórios: nome, email, telefone"}), 400

    if Usuario.query.filter_by(email=dados["email"]).first():
        return jsonify({"erro": "Email já cadastrado."}), 400

    novo_usuario = Usuario(
        nome=dados["nome"],
        email=dados["email"],
        telefone=dados["telefone"]
    )

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuário criado com sucesso!", "usuario_id": novo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao criar usuário.", "detalhes": str(e)}), 500

# Rota para listar usuários
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "telefone": u.telefone
        })
    return jsonify(resultado)

# Inicializa o app e o banco de dados
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
