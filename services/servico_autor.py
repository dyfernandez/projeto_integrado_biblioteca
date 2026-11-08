from models.autor import Autor


class ServicoAutor:

    def __init__(self, conexao):
        self.conexao = conexao

    def criar_autor(self, nome_autor, pais):
        cur = self.conexao.cursor()
        try:
            cur.execute(
                "INSERT INTO autor (nome_autor, pais) VALUES (%s, %s) RETURNING id_autor",
                (nome_autor, pais),
            )
            id_autor = cur.fetchone()[0]
            self.conexao.commit()
            return id_autor
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

    def buscar_autor(self, id_ou_nome):
        cur = self.conexao.cursor()
        try:
            if str(id_ou_nome).isdigit():
                cur.execute(
                    "SELECT id_autor, nome_autor, pais FROM autor WHERE id_autor = %s",
                    (int(id_ou_nome),),
                )
            else:
                cur.execute(
                    "SELECT id_autor, nome_autor, pais FROM autor WHERE nome_autor = %s "
                    "ORDER BY id_autor",
                    (id_ou_nome,),
                )
            linhas = cur.fetchall()
            return [Autor(*linha) for linha in linhas]
        finally:
            cur.close()

    def atualizar_autor(self, id_autor, nome_autor=None, pais=None):
        campos = []
        valores = []

        if nome_autor is not None:
            campos.append("nome_autor = %s")
            valores.append(nome_autor)
        if pais is not None:
            campos.append("pais = %s")
            valores.append(pais)

        if not campos:
            return

        valores.append(id_autor)
        sql = f"UPDATE autor SET {', '.join(campos)} WHERE id_autor = %s"
        cur = self.conexao.cursor()
        try:
            cur.execute(sql, tuple(valores))
            if cur.rowcount == 0:
                raise ValueError("Autor não encontrado.")
            self.conexao.commit()
        except Exception:
            self.conexao.rollback()
            raise
        finally:
            cur.close()

    def listar_autor(self):
        cur = self.conexao.cursor()
        try:
            cur.execute("SELECT id_autor, nome_autor, pais FROM autor")
            linhas = cur.fetchall()
            return [Autor(*linha) for linha in linhas]
        finally:
            cur.close()
