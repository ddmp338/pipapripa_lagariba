# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Autor, Livro
from datetime import datetime
import os

# --- Configuração da Aplicação ---
app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-muito-segura'  # Necessário para mensagens flash

# Configuração do SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'livraria.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com a aplicação
db.init_app(app)

# Cria as tabelas se elas não existirem (dentro do contexto da aplicação)
with app.app_context():
    db.create_all()

# --- Rotas da Página Inicial ---
@app.route('/')
def index():
    """Página inicial com links para as listagens."""
    return render_template('index.html')

# --- CRUD para AUTORES ---

@app.route('/autores')
def listar_autores():
    """Lista todos os autores."""
    autores = Autor.query.order_by(Autor.nome).all()
    return render_template('autor_listar.html', autores=autores)

@app.route('/autores/novo', methods=['GET', 'POST'])
def criar_autor():
    """Cria um novo autor."""
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento_str = request.form.get('data_nascimento')

        # Validação simples
        if not nome:
            flash('O nome do autor é obrigatório.', 'danger')
            return render_template('autor_form.html')

        # Converte a data, se fornecida
        data_nascimento = None
        if data_nascimento_str:
            try:
                data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido. Use AAAA-MM-DD.', 'danger')
                return render_template('autor_form.html')

        # Cria e salva o autor
        novo_autor = Autor(nome=nome, data_nascimento=data_nascimento)
        try:
            db.session.add(novo_autor)
            db.session.commit()
            flash(f'Autor "{nome}" criado com sucesso!', 'success')
            return redirect(url_for('listar_autores'))
        except Exception as e:  # Em caso de erro (ex: nome duplicado)
            db.session.rollback()
            flash(f'Erro ao criar autor: {e}', 'danger')

    return render_template('autor_form.html', autor=None)

@app.route('/autores/<int:id>/editar', methods=['GET', 'POST'])
def editar_autor(id):
    """Edita um autor existente."""
    autor = Autor.query.get_or_404(id)

    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento_str = request.form.get('data_nascimento')

        if not nome:
            flash('O nome do autor é obrigatório.', 'danger')
            return render_template('autor_form.html', autor=autor)

        data_nascimento = None
        if data_nascimento_str:
            try:
                data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido. Use AAAA-MM-DD.', 'danger')
                return render_template('autor_form.html', autor=autor)

        # Atualiza os dados
        autor.nome = nome
        autor.data_nascimento = data_nascimento
        try:
            db.session.commit()
            flash(f'Autor "{nome}" atualizado com sucesso!', 'success')
            return redirect(url_for('listar_autores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar autor: {e}', 'danger')

    # Pré-preenche o formulário
    return render_template('autor_form.html', autor=autor)

@app.route('/autores/<int:id>/deletar', methods=['POST'])
def deletar_autor(id):
    """Deleta um autor e todos os seus livros (cascade)."""
    autor = Autor.query.get_or_404(id)
    try:
        db.session.delete(autor)
        db.session.commit()
        flash(f'Autor "{autor.nome}" e seus livros foram deletados.', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar autor: {e}', 'danger')
    return redirect(url_for('listar_autores'))

# --- CRUD para LIVROS ---

@app.route('/livros')
def listar_livros():
    """Lista todos os livros com seus autores."""
    livros = Livro.query.order_by(Livro.titulo).all()
    return render_template('livro_listar.html', livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
def criar_livro():
    """Cria um novo livro."""
    autores = Autor.query.order_by(Autor.nome).all()
    if not autores:
        flash('Cadastre um autor antes de criar um livro.', 'info')
        return redirect(url_for('criar_autor'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        ano = request.form.get('ano_publicacao')
        isbn = request.form.get('isbn')

        if not titulo or not autor_id:
            flash('Título e autor são obrigatórios.', 'danger')
            return render_template('livro_form.html', autores=autores, livro=None)

        ano_int = None
        if ano:
            try:
                ano_int = int(ano)
            except ValueError:
                flash('Ano de publicação deve ser um número.', 'danger')
                return render_template('livro_form.html', autores=autores, livro=None)

        novo_livro = Livro(titulo=titulo, autor_id=int(autor_id), ano_publicacao=ano_int, isbn=isbn or None)
        try:
            db.session.add(novo_livro)
            db.session.commit()
            flash(f'Livro "{titulo}" criado com sucesso!', 'success')
            return redirect(url_for('listar_livros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar livro: {e}', 'danger')

    return render_template('livro_form.html', autores=autores, livro=None)

@app.route('/livros/<int:id>/editar', methods=['GET', 'POST'])
def editar_livro(id):
    """Edita um livro existente."""
    livro = Livro.query.get_or_404(id)
    autores = Autor.query.order_by(Autor.nome).all()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        ano = request.form.get('ano_publicacao')
        isbn = request.form.get('isbn')

        if not titulo or not autor_id:
            flash('Título e autor são obrigatórios.', 'danger')
            return render_template('livro_form.html', autores=autores, livro=livro)

        ano_int = None
        if ano:
            try:
                ano_int = int(ano)
            except ValueError:
                flash('Ano de publicação deve ser um número.', 'danger')
                return render_template('livro_form.html', autores=autores, livro=livro)

        # Atualiza os dados
        livro.titulo = titulo
        livro.autor_id = int(autor_id)
        livro.ano_publicacao = ano_int
        livro.isbn = isbn or None
        try:
            db.session.commit()
            flash(f'Livro "{titulo}" atualizado com sucesso!', 'success')
            return redirect(url_for('listar_livros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar livro: {e}', 'danger')

    return render_template('livro_form.html', autores=autores, livro=livro)

@app.route('/livros/<int:id>/deletar', methods=['POST'])
def deletar_livro(id):
    """Deleta um livro específico."""
    livro = Livro.query.get_or_404(id)
    try:
        db.session.delete(livro)
        db.session.commit()
        flash(f'Livro "{livro.titulo}" deletado.', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar livro: {e}', 'danger')
    return redirect(url_for('listar_livros'))

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)