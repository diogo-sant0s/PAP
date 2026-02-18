# PAP — Demonstração de Login (Flask) com e sem SQL Injection

Projeto da **Prova de Aptidão Profissional (PAP)** que demonstra, em contexto escolar, a diferença entre um **login vulnerável** (SQL Injection) e um **login protegido** (queries parametrizadas).

> **Aviso (uso educativo):** este repositório existe apenas para fins de **aprendizagem**. Não uses o “Site Desprotegido” em produção.

---

## O que existe aqui

Este repositório contém **duas versões** da mesma aplicação Flask:

- **`Site Desprotegido/`** — login **vulnerável** (constrói SQL por concatenação de strings).
- **`Site Protegido/`** — login **protegido** (usa parâmetros/queries parametrizadas com SQLAlchemy).

Ambos incluem:

- `main.py` — inicializa e executa o servidor Flask.
- `views.py` — rotas (`/`, `/login`, `/dashboard`, `/logout`) e lógica de autenticação.
- `database.py` — modelo `Login`, criação da BD SQLite e utilizador padrão.
- `templates/` — páginas HTML (`base.html`, `login.html`, `dashboard.html`).
- `static/style.css` — estilos.
- `requirements.txt` — dependências.

---

## Utilizador padrão (para testes)

Ao arrancar a aplicação, é criado um utilizador por defeito (se ainda não existir):

- **Username:** `admin`
- **Password:** `1234`

---

## Como executar

> Podes executar **um site de cada vez** (cada pasta tem a sua própria aplicação).

### 1) Criar ambiente virtual (recomendado)

No terminal, dentro de **cada pasta** (`Site Protegido` ou `Site Desprotegido`):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 2) Instalar dependências

```bash
pip install -r requirements.txt
```

### 3) Executar o servidor

```bash
python main.py
```

Por omissão, o projeto arranca em:

- `http://localhost:5000`

---

## Diferença principal: vulnerável vs protegido

### Site Desprotegido — **vulnerável a SQL Injection**

No `Site Desprotegido/views.py`, a query é construída juntando diretamente o input do utilizador numa string SQL, por exemplo:

```python
query = f"SELECT * FROM login WHERE username = '{login_input}' AND password = '{password_input}'"
result = db_session.execute(text(query)).fetchone()
```

Isto é perigoso porque permite que o utilizador **altere a lógica do `WHERE`** ao injetar caracteres especiais/SQL.

### Site Protegido — **proteção com parâmetros**

No `Site Protegido/views.py`, a query usa **placeholders** e os valores são passados como **parâmetros**:

```python
query = text("SELECT * FROM Login WHERE username = :username AND password = :password")
result = db_session.execute(query, {"username": login_input, "password": password_input}).fetchone()
```

Aqui, o input do utilizador **não é concatenado** na string SQL: é enviado separadamente como parâmetro, o que ajuda a evitar SQL Injection.

---

## Notas sobre ficheiros incluídos

- `database.db` é uma base de dados **SQLite** local (fica dentro de cada pasta do site).
- `flask_session/` guarda sessões no sistema de ficheiros (pode ser apagado sem problemas — é recriado).
- `__pycache__/` são ficheiros gerados pelo Python (podem ser ignorados no versionamento).

---

## Licença

Este projeto inclui um ficheiro `LICENSE` (ver repositório).

---

## Autor / Contexto

Projeto desenvolvido para a **PAP**, com objetivo de explicar:

- como funciona um login simples com Flask;
- o conceito de SQL Injection;
- e como a parametrização/ORM ajuda a mitigar este tipo de vulnerabilidade.
