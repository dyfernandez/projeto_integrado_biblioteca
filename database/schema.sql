-- database/schema.sql
-- Cria as tabelas do sistema de biblioteca no PostgreSQL.
-- Ordem: primeiro as tabelas que ninguém referencia, depois as que apontam pra elas.

CREATE TABLE autor (
    id_autor   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_autor VARCHAR(150) NOT NULL,
    pais       VARCHAR(60)  NOT NULL
);

CREATE TABLE livro (
    id_livro       INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_livro     VARCHAR(200) NOT NULL,
    ano_publicacao INT          NOT NULL,
    copias         INT          NOT NULL CHECK (copias >= 0)
);

CREATE TABLE usuario (
    id_usuario   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_usuario VARCHAR(150) NOT NULL,
    telefone     VARCHAR(20)  NOT NULL,
    email        VARCHAR(255) NOT NULL,
    rua          VARCHAR(150) NOT NULL,
    numero       VARCHAR(10)  NOT NULL,
    bairro       VARCHAR(100) NOT NULL,
    status_usuario BOOLEAN    NOT NULL DEFAULT TRUE 
);

CREATE TABLE emprestimo (
    id_emprestimo   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_usuario      INT  NOT NULL REFERENCES usuario(id_usuario),
    id_livro        INT  NOT NULL REFERENCES livro(id_livro),
    data_retirada   DATE NOT NULL,
    data_prev_devol DATE NOT NULL,
    data_devol      DATE NULL
);

CREATE TABLE livro_autor (
    id_livro_autor INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_livro       INT NOT NULL REFERENCES livro(id_livro),
    id_autor       INT NOT NULL REFERENCES autor(id_autor),
    UNIQUE (id_livro, id_autor)
);