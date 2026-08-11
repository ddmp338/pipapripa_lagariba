# pipapripa_lagariba
Criando um CRUD aí com um ORM aí

<h1>Como executar</h1>

Dependências --> Abra seu terminal e execute: pip install Flask Flask-SQLAlchemy

Execute --> No diretório onde está o app.py, execute: python app.py

Acesse --> Abra http://127.0.0.1:5000/

<h2>Especificações</h2>

models.py --> define a conexão com o banco de dados e as tabelas Autor e Livro

app.py --> configura o Flask, o banco de dados, e implementa todas as rotas para o CRUD

base.html --> layout base para todos os templates

index.html --> página inicial

autor_listar.html --> lista de autores

autor_form.html --> formulário para criar/editar autor

livro_listar.html --> lista de livros

livro_form.html --> formulário para criar/editar livro

<h2>Prompt único</h2>
Crie um CRUD para registrar livros e seus autores com Flask e ORM

Para criar o CRUD, se limite a essa fonte: https://flask.palletsprojects.com/en/stable/

Para usar o ORM, se limite ao SQLite