from models.livro import Livro


class ServicoLivro:
    """Regras e acesso ao banco para livros.
    
    Nas consultas, string_agg junta os nomes dos autores numa linha só
    (um livro pode ter vários autores). As buscas devolvem pares (Livro, autores).
    """
    def __init__(self, conexao):
        """Guarda a conexão que vem do main.py."""
        self.conexao = conexao

    def criar_livro(self, nome_livro, ano_publicacao, copias, ids_autores):
        """Cadastra o livro e liga ele aos autores. Devolve o id do livro.
        Tudo no mesmo commit: se algo falhar, nem o livro fica salvo.
        """
        cur = self.conexao.cursor()
        try:
            # Regra: livro sem autor não pode ser cadastrado
            if not ids_autores:
                raise ValueError("O livro precisa ter pelo menos um autor.")

            cur.execute(
                "INSERT INTO livro (nome_livro, ano_publicacao, copias) VALUES (%s, %s, %s) RETURNING id_livro",
                (nome_livro, ano_publicacao, copias),
            )
            id_livro = cur.fetchone()[0]

            # set() tira ids repetidos, senão ligaria o mesmo autor duas vezes
            for id_autor in set(ids_autores):
                cur.execute(
                    "INSERT INTO livro_autor (id_livro, id_autor) VALUES (%s, %s)",
                    (id_livro, id_autor),
                )

            self.conexao.commit()
            return id_livro
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

    def buscar_livro(self, id_ou_nome):
        """Busca simples: por id ou por parte do título."""
        cur = self.conexao.cursor()
        try:
            texto = str(id_ou_nome)
            # Se digitou só números, procura pelo id e também por títulos com esse número
            if texto.isdigit():
                filtro = "WHERE l.id_livro = %s OR l.nome_livro ILIKE %s"
                valores = (int(texto), f"%{texto}%")
            else:
                filtro = "WHERE l.nome_livro ILIKE %s"
                valores = (f"%{texto}%",)

            cur.execute(
                "SELECT l.id_livro, l.nome_livro, l.ano_publicacao, l.copias, "
                "COALESCE(string_agg(a.nome_autor, ', '), '') "
                "FROM livro l "
                "LEFT JOIN livro_autor la ON la.id_livro = l.id_livro "
                "LEFT JOIN autor a ON a.id_autor = la.id_autor "
                f"{filtro} "
                "GROUP BY l.id_livro "
                "ORDER BY l.nome_livro",
                valores,
            )
            linhas = cur.fetchall()
            return [(Livro(*linha[:4]), linha[4]) for linha in linhas]
        finally:
            cur.close()

    def buscar_livros(self, titulo=None, autor=None, ano=None):
        """Busca com filtros opcionais (título, autor e ano). Só filtra pelo que for informado.
        """
        # Vai montando o WHERE só com os filtros preenchidos
        condicoes = []
        valores = []

        if titulo:
            condicoes.append("l.nome_livro ILIKE %s")
            valores.append(f"%{titulo}%")

        if autor:
            # EXISTS em vez de WHERE em a.nome_autor: o filtro não pode cortar
            # as linhas do JOIN, senão string_agg perde os outros autores.
            condicoes.append(
                "EXISTS (SELECT 1 FROM livro_autor la2 "
                "JOIN autor a2 ON a2.id_autor = la2.id_autor "
                "WHERE la2.id_livro = l.id_livro AND a2.nome_autor ILIKE %s)"
            )
            valores.append(f"%{autor}%")

        if ano is not None and ano != "":
            condicoes.append("l.ano_publicacao = %s")
            valores.append(ano)

        filtro = f"WHERE {' AND '.join(condicoes)} " if condicoes else ""

        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT l.id_livro, l.nome_livro, l.ano_publicacao, l.copias, "
                "COALESCE(string_agg(a.nome_autor, ', '), '') "
                "FROM livro l "
                "LEFT JOIN livro_autor la ON la.id_livro = l.id_livro "
                "LEFT JOIN autor a ON a.id_autor = la.id_autor "
                f"{filtro}"
                "GROUP BY l.id_livro "
                "ORDER BY l.nome_livro",
                tuple(valores),
            )
            linhas = cur.fetchall()
            return [(Livro(*linha[:4]), linha[4]) for linha in linhas]
        finally:
            cur.close()

    def listar_livros(self):
        """Devolve todos os livros com seus autores."""
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT l.id_livro, l.nome_livro, l.ano_publicacao, l.copias, "
                "COALESCE(string_agg(a.nome_autor, ', '), '') "
                "FROM livro l "
                "LEFT JOIN livro_autor la ON la.id_livro = l.id_livro "
                "LEFT JOIN autor a ON a.id_autor = la.id_autor "
                "GROUP BY l.id_livro "
                "ORDER BY l.nome_livro"
            )
            linhas = cur.fetchall()
            return [(Livro(*linha[:4]), linha[4]) for linha in linhas]
        finally:
            cur.close()

    def atualizar_livro(
        self,
        id_livro,
        nome_livro=None,
        ano_publicacao=None,
        copias=None,
        ids_autores=None,
    ):
        """Altera só o que foi informado (None = manter). Se vier ids_autores, a lista de autores é trocada."""
        # Monta o UPDATE só com os campos preenchidos
        campos = []
        valores = []

        if nome_livro is not None:
            campos.append("nome_livro = %s")
            valores.append(nome_livro)

        if ano_publicacao is not None:
            campos.append("ano_publicacao = %s")
            valores.append(ano_publicacao)

        if copias is not None:
            campos.append("copias = %s")
            valores.append(copias)

        cur = self.conexao.cursor()
        try:
            if ids_autores is not None and not ids_autores:
                raise ValueError("O livro precisa ter pelo menos um autor.")

            cur.execute("SELECT 1 FROM livro WHERE id_livro = %s", (id_livro,))
            if cur.fetchone() is None:
                raise ValueError("Livro não encontrado.")

            if campos:
                query = f"UPDATE livro SET {', '.join(campos)} WHERE id_livro = %s"
                valores.append(id_livro)
                cur.execute(query, tuple(valores))

            # Troca de autores: apaga os vínculos antigos e cria os novos
            if ids_autores is not None:
                cur.execute("DELETE FROM livro_autor WHERE id_livro = %s", (id_livro,))
                for id_autor in set(ids_autores):
                    cur.execute(
                        "INSERT INTO livro_autor (id_livro, id_autor) VALUES (%s, %s)",
                        (id_livro, id_autor),
                    )

            self.conexao.commit()
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()
