from models.livro import Livro


class ServicoLivro:
    def __init__(self, conexao):
        self.conexao = conexao

    def criar_livro(self, nome_livro, ano_publicacao, copias, ids_autores):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "INSERT INTO livro (nome_livro, ano_publicacao, copias) VALUES (%s, %s, %s) RETURNING id_livro",
                (nome_livro, ano_publicacao, copias),
            )
            id_livro = cur.fetchone()[0]

            for id_autor in ids_autores:
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
        cur = self.conexao.cursor()
        try:
            if isinstance(id_ou_nome, int):
                filtro = "WHERE l.id_livro = %s"
                valor = id_ou_nome
            else:
                filtro = "WHERE l.nome_livro ILIKE %s"
                valor = f"%{id_ou_nome}%"

            cur.execute(
                "SELECT l.id_livro, l.nome_livro, l.ano_publicacao, l.copias, "
                "COALESCE(string_agg(a.nome_autor, ', '), '') "
                "FROM livro l "
                "LEFT JOIN livro_autor la ON la.id_livro = l.id_livro "
                "LEFT JOIN autor a ON a.id_autor = la.id_autor "
                f"{filtro} "
                "GROUP BY l.id_livro "
                "ORDER BY l.nome_livro",
                (valor,),
            )
            linhas = cur.fetchall()
            return [(Livro(*linha[:4]), linha[4]) for linha in linhas]
        finally:
            cur.close()

    def listar_livros(self):
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
