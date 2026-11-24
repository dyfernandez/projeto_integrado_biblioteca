# Sistema de Biblioteca Comunitária / Community Library System

[Português](#português) · [English](#english)

---

## Português

Trabalho da disciplina Projeto Integrado, do curso de Ciência de Dados (UNIC). Sistema de terminal para gerenciar uma biblioteca de bairro: cadastro de livros, autores e usuários, empréstimos, devoluções, buscas e relatórios. Escrito em Python, com os dados guardados em PostgreSQL.

**Autor:** Dylan Fernandez

### Funcionalidades

| Requisito | O que faz |
| :--- | :--- |
| RF01 | Cadastro de livros (título, ano, cópias e um ou mais autores) |
| RF02 | Cadastro de autores (nome e país) |
| RF03 | Cadastro de usuários (nome, telefone, e-mail e endereço) |
| RF04 | Registro de empréstimos, com verificação de cópias e prazo de devolução |
| RF05 | Registro de devoluções, repondo a cópia no acervo |
| RF06 | Consultas por título, autor e/ou ano |
| RF07 | Relatórios: livros disponíveis, livros emprestados e usuários |

### Tecnologias

- Python 3
- PostgreSQL
- `psycopg2-binary` (acesso ao banco)
- `python-dotenv` (leitura do arquivo `.env`)

### Estrutura do projeto

```text
.
├── main.py                  # Abre a conexão e inicia o menu
├── database/
│   ├── conexao.py           # Função conectar() (lê o .env)
│   └── schema.sql           # Criação das tabelas
├── models/                  # Classes simples das entidades
├── services/                # Regras de negócio e SQL de cada domínio
├── exceptions/
│   └── erros.py             # Erros do sistema (ErroBiblioteca e derivados)
└── ui/
    └── menu.py              # Menus e leitura do teclado
```

A separação em camadas é: `ui` (tela) → `services` (regras e SQL) → banco. Os `models` apenas representam os dados.

### Como rodar

1. **Crie o banco e as tabelas** no PostgreSQL:

   ```bash
   createdb biblioteca
   psql -d biblioteca -f database/schema.sql
   ```

2. **Crie o ambiente virtual e instale as dependências:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install psycopg2-binary python-dotenv
   ```

3. **Crie o arquivo `.env`** na raiz do projeto (ele não vai para o git):

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=biblioteca
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   ```

4. **Execute:**

   ```bash
   python main.py
   ```

### Uso

O menu principal tem cinco áreas: **Livros**, **Autores**, **Usuários**, **Empréstimos** e **Relatórios**. Cada uma abre um submenu numerado, e a opção `0` volta (ou sai, no menu principal). Nas telas de atualização, deixar um campo em branco mantém o valor atual.

Para cadastrar um livro é preciso ter ao menos um autor cadastrado.

### Decisões de projeto

**Banco de dados**
- O número de cópias fica na própria tabela `livro`, com `CHECK (copias >= 0)`, então o banco nunca aceita estoque negativo.
- `UNIQUE (id_livro, id_autor)` em `livro_autor` impede o mesmo autor duas vezes no mesmo livro.
- Usuário não é apagado: é desativado (`status_usuario = FALSE`), para não perder o histórico de empréstimos.

**Empréstimos**
- O empréstimo é recusado se o livro não tem cópias disponíveis.
- O prazo é fixo, de 7 dias, e é calculado no próprio SQL (`CURRENT_DATE + 7`).
- `data_devol` nasce vazia (`NULL`). A devolução é um `UPDATE` na mesma linha do empréstimo.
- Não dá para desativar um usuário que ainda tem livro para devolver.

**Transações**
- Operações que mexem em mais de uma tabela (registrar empréstimo, devolver, criar e atualizar livro) fazem um único `commit` no fim. Se algo falhar, o `rollback` desfaz tudo e nada fica pela metade.

**Arquitetura**
- Não há listas em memória: o banco é a fonte da verdade.
- A conexão é aberta uma vez no `main.py` e passada para os serviços.
- Os relatórios têm SQL próprio e devolvem tuplas.
- A relação livro-autor não tem serviço próprio: é gerenciada pelo `ServicoLivro`.
- A tela fica separada em `ui/menu.py`.

**Regras**
- Não existe exclusão de autor.
- Todo livro exige pelo menos um autor. Autores repetidos na lista são ignorados pelo serviço e também barrados pelo banco.
- Erros de regra (id inexistente, livro sem cópias, livro sem autor etc.) levantam exceções de `exceptions/erros.py`. Todas herdam de `ErroBiblioteca`, que herda de `ValueError`, e o menu mostra a mensagem sem derrubar o programa.
- As buscas devolvem sempre uma lista. Em uma busca simples, um texto só com números procura pelo id **ou** pelo título.

---

## English

Assignment for the Projeto Integrado (Integrated Project) course of the Data Science program at UNIC. A terminal application to manage a neighborhood library: books, authors and users, loans, returns, searches and reports. Written in Python, with data stored in PostgreSQL.

**Author:** Dylan Fernandez

### Features

| Requirement | What it does |
| :--- | :--- |
| RF01 | Book registration (title, year, copies and one or more authors) |
| RF02 | Author registration (name and country) |
| RF03 | User registration (name, phone, e-mail and address) |
| RF04 | Loan registration, checking available copies and setting a due date |
| RF05 | Return registration, putting the copy back in the collection |
| RF06 | Search by title, author and/or year |
| RF07 | Reports: available books, borrowed books and users |

### Technologies

- Python 3
- PostgreSQL
- `psycopg2-binary` (database access)
- `python-dotenv` (reads the `.env` file)

### Project structure

```text
.
├── main.py                  # Opens the connection and starts the menu
├── database/
│   ├── conexao.py           # conectar() function (reads the .env)
│   └── schema.sql           # Table creation
├── models/                  # Simple entity classes
├── services/                # Business rules and SQL for each domain
├── exceptions/
│   └── erros.py             # System errors (ErroBiblioteca and subclasses)
└── ui/
    └── menu.py              # Menus and keyboard input
```

The layers are: `ui` (screen) → `services` (rules and SQL) → database. The `models` only represent the data.

### How to run

1. **Create the database and tables** in PostgreSQL:

   ```bash
   createdb biblioteca
   psql -d biblioteca -f database/schema.sql
   ```

2. **Create a virtual environment and install the dependencies:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install psycopg2-binary python-dotenv
   ```

3. **Create the `.env` file** in the project root (it is not tracked by git):

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=biblioteca
   DB_USER=your_user
   DB_PASSWORD=your_password
   ```

4. **Run:**

   ```bash
   python main.py
   ```

### Usage

The main menu has five areas: **Books** (Livros), **Authors** (Autores), **Users** (Usuários), **Loans** (Empréstimos) and **Reports** (Relatórios). Each one opens a numbered submenu, and option `0` goes back (or exits, in the main menu). In the update screens, leaving a field blank keeps the current value.

To register a book, at least one author must already exist.

### Design decisions

**Database**
- The number of copies is stored in the `livro` table itself, with `CHECK (copias >= 0)`, so the database never accepts negative stock.
- `UNIQUE (id_livro, id_autor)` in `livro_autor` prevents the same author from being linked twice to the same book.
- Users are never deleted: they are deactivated (`status_usuario = FALSE`) so the loan history is kept.

**Loans**
- A loan is refused if the book has no copies available.
- The loan period is fixed at 7 days and is calculated in the SQL itself (`CURRENT_DATE + 7`).
- `data_devol` starts empty (`NULL`). Returning a book is an `UPDATE` on the same loan row.
- A user who still has a book to return cannot be deactivated.

**Transactions**
- Operations that touch more than one table (registering a loan, returning a book, creating and updating a book) make a single `commit` at the end. If anything fails, `rollback` undoes everything and nothing is left half-done.

**Architecture**
- There are no in-memory lists: the database is the source of truth.
- The connection is opened once in `main.py` and passed to the services.
- Reports have their own SQL and return tuples.
- The book-author link has no service of its own: it is handled by `ServicoLivro`.
- The screen code is separated in `ui/menu.py`.

**Rules**
- There is no author deletion.
- Every book requires at least one author. Duplicate authors in the list are ignored by the service and also blocked by the database.
- Rule errors (unknown id, book without copies, book without author, etc.) raise exceptions from `exceptions/erros.py`. They all inherit from `ErroBiblioteca`, which inherits from `ValueError`, and the menu prints the message without crashing the program.
- Searches always return a list. In the simple search, a text made only of digits looks for the id **or** the title.
