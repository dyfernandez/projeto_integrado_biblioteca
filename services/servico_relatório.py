class ServicoRelatorio:
    def __init__(self, conexao):
        self.conexao = conexao

    def relatorio_livros_disponiveis(self):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT l.id_livro, l.nome_livro, l.ano_publicacao, l.copias, "
                "COALESCE(string_agg(a.nome_autor, ', '), '') "
                "FROM livro l "
                "LEFT JOIN livro_autor la ON la.id_livro = l.id_livro "
                "LEFT JOIN autor a ON a.id_autor = la.id_autor "
                "WHERE l.copias > 0 "
                "GROUP BY l.id_livro "
                "ORDER BY l.nome_livro"
            )
            return cur.fetchall()
        finally:
            cur.close()

    def relatorio_livros_emprestados(self): ...

    def relatorio_usuarios(self): ...
