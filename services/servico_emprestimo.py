from models.emprestimo import Emprestimo


class ServicoEmprestimo:
    def __init__(self, conexao):
        self.conexao = conexao

    def registrar_emprestimo(self, id_usuario, id_livro):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT 1 FROM usuario WHERE id_usuario = %s AND status_usuario = TRUE",
                (id_usuario,),
            )
            if cur.fetchone() is None:
                raise ValueError("Usuário não encontrado ou desativado.")
            cur.execute(
                "SELECT 1 FROM livro WHERE id_livro = %s AND copias >= 1",
                (id_livro,),
            )
            if cur.fetchone() is None:
                raise ValueError("Livro não encontrado ou sem cópias disponíveis.")

            cur.execute(
                "INSERT INTO emprestimo (id_usuario, id_livro, data_retirada, data_prev_devol) VALUES (%s, %s, CURRENT_DATE, CURRENT_DATE + 7)",
                (id_usuario, id_livro),
            )
            cur.execute(
                "UPDATE livro SET copias = copias - 1 WHERE id_livro = %s",
                (id_livro,),
            )

            self.conexao.commit()
        except Exception as e:
            self.conexao.rollback()
            raise e
        finally:
            cur.close()

    def devolver_livro(self, id_emprestimo):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "UPDATE emprestimo SET data_devol = CURRENT_DATE "
                "WHERE id_emprestimo = %s AND data_devol IS NULL "
                "RETURNING id_livro",
                (id_emprestimo,),
            )
            linha = cur.fetchone()
            if linha is None:
                raise ValueError("Emprestimo não encontrado ou já devolvido..")
            id_livro = linha[0]

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
