from models.usuario import Usuario


class ServicoUsuario:
    def __init__(self, conexao):
        self.conexao = conexao

    def criar_usuario(self, nome, telefone, email, rua, numero, bairro):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "INSERT INTO usuario (nome_usuario, telefone, email, rua, numero, bairro) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (nome, telefone, email, rua, numero, bairro),
            )
            self.conexao.commit()
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

    def buscar_usuario(self, id_ou_nome):
        cur = self.conexao.cursor()
        try:
            if str(id_ou_nome).isdigit():
                cur.execute(
                    "SELECT id_usuario, nome_usuario, telefone, email, rua, numero, bairro "
                    "FROM usuario WHERE id_usuario = %s AND status_usuario = TRUE",
                    (int(id_ou_nome),),
                )
            else:
                cur.execute(
                    "SELECT id_usuario, nome_usuario, telefone, email, rua, numero, bairro "
                    "FROM usuario WHERE nome_usuario = %s AND status_usuario = TRUE",
                    (id_ou_nome,),
                )
            linha = cur.fetchone()
            if linha is None:
                return None
            return Usuario(*linha)
        finally:
            cur.close()

    def atualizar_usuario(
        self,
        id_usuario,
        nome=None,
        telefone=None,
        email=None,
        rua=None,
        numero=None,
        bairro=None,
    ):
        cur = self.conexao.cursor()
        campos = []
        valores = []

        if nome is not None:
            campos.append("nome_usuario = %s")
            valores.append(nome)

        if telefone is not None:
            campos.append("telefone = %s")
            valores.append(telefone)

        if email is not None:
            campos.append("email = %s")
            valores.append(email)

        if rua is not None:
            campos.append("rua = %s")
            valores.append(rua)

        if numero is not None:
            campos.append("numero = %s")
            valores.append(numero)

        if bairro is not None:
            campos.append("bairro = %s")
            valores.append(bairro)

        if not campos:
            cur.close()
            return

        valores.append(id_usuario)

        try:
            cur.execute(
                f"UPDATE usuario SET {', '.join(campos)} "
                "WHERE id_usuario = %s AND status_usuario = TRUE",
                valores,
            )
            self.conexao.commit()
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

    def deletar_usuario(self, id_usuario):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "SELECT 1 FROM emprestimo "
                "WHERE id_usuario = %s AND data_devol IS NULL",
                (id_usuario,),
            )
            if cur.fetchone() is not None:
                raise ValueError("O usuário tem um livro pendente de devolução.")

            cur.execute(
                "UPDATE usuario SET status_usuario = FALSE "
                "WHERE id_usuario = %s AND status_usuario = TRUE",
                (id_usuario,),
            )
            self.conexao.commit()
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

        def listar_usuario(self):
            cur = self.conexao.cursor()
            try:
                cur.execute(
                    "SELECT id_usuario, nome_usuario, telefone, email, rua, numero, bairro "
                    "FROM usuario WHERE status_usuario = TRUE"
                )
                linhas = cur.fetchall()
                return [Usuario(*linha) for linha in linhas]
            finally:
                cur.close()
