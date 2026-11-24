import sys

import psycopg2

from database.conexao import conectar
from ui.menu import menu_principal


def main():
    """Conecta no banco, abre o menu e fecha a conexão no final. Devolve 0 se deu certo e 1 se deu erro."""
    # Se o banco estiver fora do ar, avisa e encerra sem mostrar o menu
    try:
        conexao = conectar()
    except psycopg2.OperationalError as erro:
        print(f"Não foi possível conectar ao banco: {erro}")
        return 1

    try:
        menu_principal(conexao)
    # Ctrl+C ou Ctrl+D encerram o programa sem mostrar erro feio
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando.")
    except psycopg2.Error:
        print("\nA conexão com o banco foi perdida.")
        return 1
    finally:
        # Fecha a conexão aconteça o que acontecer
        conexao.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
