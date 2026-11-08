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

    def relatorio_livros_emprestados(self):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT e.id_emprestimo, u.nome_usuario, l.nome_livro, "
                "e.data_retirada, e.data_prev_devol "
                "FROM emprestimo e "
                "JOIN usuario u ON u.id_usuario = e.id_usuario "
                "JOIN livro l ON l.id_livro = e.id_livro "
                "WHERE e.data_devol IS NULL "
                "ORDER BY e.data_prev_devol"
            )
            return cur.fetchall()
        finally:
            cur.close()

    def relatorio_usuarios(self):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT c.id_usuario, c.nome_usuario, "
                "COUNT(p.id_emprestimo) AS total_emprestimos, "
                "COUNT(p.id_emprestimo) FILTER (WHERE p.data_devol IS NULL) "
                "AS emprestimos_abertos "
                "FROM usuario c "
                "LEFT JOIN emprestimo p ON c.id_usuario = p.id_usuario "
                "GROUP BY c.id_usuario "
                "ORDER BY c.nome_usuario"
            )
            return cur.fetchall()
        finally:
            cur.close()
