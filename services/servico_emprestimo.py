from exceptions.erros import (
    EmprestimoNaoEncontrado,
    LivroIndisponivel,
    LivroNaoEncontrado,
    UsuarioNaoEncontrado,
)


class ServicoEmprestimo:
    """Empréstimos e devoluções.
    
    O estoque (livro.copias) é ajustado na mesma transação do empréstimo,
    então os dois andam juntos: ou salva tudo, ou desfaz tudo.
    """
    def __init__(self, conexao):
        """Guarda a conexão que vem do main.py."""
        self.conexao = conexao

    def registrar_emprestimo(self, id_usuario, id_livro):
        """Empresta um livro para um usuário, com devolução prevista em 7 dias.
        """
        cur = self.conexao.cursor()
        try:
            # 1) O usuário precisa existir e estar ativo
            cur.execute(
                "SELECT 1 FROM usuario WHERE id_usuario = %s AND status_usuario = TRUE",
                (id_usuario,),
            )
            if cur.fetchone() is None:
                raise UsuarioNaoEncontrado("Usuário não encontrado ou desativado.")
            # 2) O livro precisa existir e ter pelo menos 1 cópia disponível
            cur.execute("SELECT copias FROM livro WHERE id_livro = %s", (id_livro,))
            livro = cur.fetchone()
            if livro is None:
                raise LivroNaoEncontrado("Livro não encontrado.")
            if livro[0] < 1:
                raise LivroIndisponivel("Livro sem cópias disponíveis.")

            # 3) Registra o empréstimo: retirada hoje, devolução prevista daqui a 7 dias
            cur.execute(
                "INSERT INTO emprestimo (id_usuario, id_livro, data_retirada, data_prev_devol) VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + 7)",
                (id_usuario, id_livro),
            )
            # 4) Tira uma cópia do estoque
            cur.execute(
                "UPDATE livro SET copias = copias - 1 WHERE id_livro = %s",
                (id_livro,),
            )

            # Só salva se os 4 passos deram certo
            self.conexao.commit()
        except Exception as e:
            # Qualquer erro desfaz tudo (nada fica pela metade)
            self.conexao.rollback()
            raise e
        finally:
            cur.close()

    def devolver_livro(self, id_emprestimo):
        """Registra a devolução (data de hoje) e devolve a cópia para o estoque."""
        cur = self.conexao.cursor()
        try:
            # Só atualiza se ainda não foi devolvido; RETURNING traz o livro para repor o estoque
            cur.execute(
                "UPDATE emprestimo SET data_devol = CURRENT_DATE "
                "WHERE id_emprestimo = %s AND data_devol IS NULL "
                "RETURNING id_livro",
                (id_emprestimo,),
            )
            linha = cur.fetchone()
            if linha is None:
                raise EmprestimoNaoEncontrado("Empréstimo não encontrado ou já devolvido.")
            id_livro = linha[0]

            # Devolve a cópia ao estoque
            cur.execute(
                "UPDATE livro SET copias = copias + 1 WHERE id_livro = %s",
                (id_livro,),
            )

            self.conexao.commit()
        except Exception as e:
            self.conexao.rollback()
            raise e
        finally:
            cur.close()

    def listar_emprestimos_abertos(self):
        """Lista os empréstimos que ainda não foram devolvidos (o que vence primeiro aparece antes)."""
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

    def listar_emprestimos_abertos_usuario(self, id_usuario):
        """Igual ao anterior, mas só de um usuário."""
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT e.id_emprestimo, u.nome_usuario, l.nome_livro, "
                "e.data_retirada, e.data_prev_devol "
                "FROM emprestimo e "
                "JOIN usuario u ON u.id_usuario = e.id_usuario "
                "JOIN livro l ON l.id_livro = e.id_livro "
                "WHERE e.id_usuario = %s AND e.data_devol IS NULL "
                "ORDER BY e.data_prev_devol",
                (id_usuario,),
            )
            return cur.fetchall()
        finally:
            cur.close()
