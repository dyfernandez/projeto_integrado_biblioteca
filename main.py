import sys

import psycopg2

from database.conexao import conectar
from ui.menu import menu_principal


def main():
    try:
        conexao = conectar()
    except psycopg2.OperationalError as erro:
        print(f"Não foi possível conectar ao banco: {erro}")
        return 1

    try:
        menu_principal(conexao)
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando.")
    except psycopg2.Error:
        print("\nA conexão com o banco foi perdida.")
        return 1
    finally:
        conexao.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
