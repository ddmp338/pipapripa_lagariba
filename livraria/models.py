# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Cria a instância do ORM
db = SQLAlchemy()

class Autor(db.Model):
    """Modelo para a tabela Autor."""
    __tablename__ = 'autores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    data_nascimento = db.Column(db.Date, nullable=True)

    # Relacionamento com Livros (um autor para muitos livros)
    livros = db.relationship('Livro', backref='autor', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Autor {self.nome}>'

class Livro(db.Model):
    """Modelo para a tabela Livro."""
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=True)
    isbn = db.Column(db.String(13), nullable=True, unique=True)

    # Chave estrangeira para Autor
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'