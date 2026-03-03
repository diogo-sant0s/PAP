## Projeto de Login (Ambiente Escolar)

Este projeto é um exemplo simples de aplicação Flask com autenticação, pensado apenas para **aprendizagem em ambiente escolar**.

O objetivo principal é:

- Mostrar **como funciona um login básico** com base de dados.
- Explicar, em teoria, **o que seria um login vulnerável a SQL Injection**.
- Mostrar **como o código atual evita esse tipo de vulnerabilidade**, usando SQLAlchemy (ORM) e consultas parametrizadas.

---

## Tecnologias usadas

- **Python 3**
- **Flask**
- **Flask-Session**
- **SQLAlchemy** (ORM para aceder à base de dados)
- **SQLite** (`database.db`)

---

## Estrutura principal

- `main.py` – cria a aplicação Flask e arranca o servidor.
- `database.py` – configuração da base de dados e modelo `Login`, além de criar o utilizador padrão.
- `views.py` – rotas `/`, `/login`, `/dashboard` e `/logout`.
- `templates/` – páginas HTML (`login.html`, `dashboard.html`, `base.html`).
- `static/style.css` – estilos da interface.

---

## Utilizador padrão para testes

Ao iniciar a aplicação, o ficheiro `database.py` garante a criação de um utilizador por defeito:

- **Utilizador (campo `email`)**: `admin`
- **Password**: `1234`

Este utilizador é criado apenas se ainda não existir na base de dados.

---

## Como funciona o login seguro (no projeto)

No ficheiro `views.py`, a rota de login lê os dados do formulário e usa o SQLAlchemy para procurar o utilizador:

```python
email = request.form.get('email', '').lower().strip()
password = request.form.get('password', '')

user = db_session.query(Login).filter_by(email=email).first()

if user and password and user.password == password:
    flask_session['user_id'] = user.id
    return redirect(url_for('dashboard'))
```

Em termos de SQL, o ORM converte isto num comando do género:

- `SELECT * FROM Login WHERE email = :email`

O ponto importante é que:

- O valor que o utilizador escreveu **não é colado diretamente na string SQL**.
- Em vez disso, é passado como **parâmetro** (`:email`), o que impede que o utilizador consiga “partir” a query com código SQL malicioso.

Isto é a base de uma **consulta parametrizada**, que é a forma correta de evitar SQL Injection.

---

## SQL Injection (conceito teórico)

**SQL Injection** acontece quando:

- O programa **constrói a query SQL juntando diretamente o texto escrito pelo utilizador** dentro da string SQL.
- Por exemplo, em vez de usar parâmetros, a aplicação faria algo “do tipo”:  
  “pegar no username que o utilizador escreveu” + “colar dentro do `WHERE` da query”.

Assim, se o utilizador escreve texto especial (por exemplo com aspas e operadores lógicos), pode:

- alterar a condição do `WHERE`,
- ou até terminar o comando e injetar outro.

Para evitar isso, usa-se sempre:

- **ORMs** (como o SQLAlchemy, que já parametriza por nós), ou
- **queries parametrizadas** (em que o SQL é fixo e os valores vêm em parâmetros separados).

O código deste projeto **segue essa abordagem segura**, usando o SQLAlchemy com `filter_by(...)`.

---

## XSS (Cross-Side Scripting) – conceito

Também apenas em teoria:

- XSS acontece quando um site **mostra diretamente conteúdo HTML/JavaScript vindo do utilizador** sem escapar.
- Em Flask, o motor de templates Jinja2 faz, por defeito, o “escape” de variáveis (`{{ variavel }}`), o que ajuda a evitar XSS.
- Só quando se usa o filtro `|safe` é que se diz ao template para confiar totalmente no conteúdo (e isso pode ser perigoso se o texto vier de utilizadores).

No projeto atual:

- As páginas são simples e **não imprimem conteúdo vindo de outros utilizadores**, por isso não se demonstra XSS aqui.

---
# PAP
Projeto para a Prova de Aptidão Profissional
