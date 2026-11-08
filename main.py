import sys

import psycopg2
from psycopg2 import errors

from database.conexao import conectar
from services.servico_autor import ServicoAutor
from services.servico_emprestimo import ServicoEmprestimo
from services.servico_livro import ServicoLivro
from services.servico_relatorio import ServicoRelatorio
from services.servico_usuario import ServicoUsuario


# Leitura do teclado


def ler_texto(rotulo):
    while True:
        valor = input(rotulo).strip()
        if valor:
            return valor
        print("Campo obrigatório.")


def ler_opcional(rotulo):
    return input(rotulo).strip() or None


def ler_inteiro(rotulo, minimo=None, opcional=False):
    while True:
        valor = input(rotulo).strip()
        if not valor and opcional:
            return None
        try:
            numero = int(valor)
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if minimo is not None and numero < minimo:
            print(f"O valor mínimo é {minimo}.")
            continue
        return numero


def ler_ids(rotulo, opcional=False):
    while True:
        valor = input(rotulo).strip()
        if not valor and opcional:
            return None
        try:
            ids = [int(parte) for parte in valor.split(",")]
        except ValueError:
            print("Digite os ids separados por vírgula. Exemplo: 1, 2")
            continue
        return ids


def confirmar(rotulo):
    return input(f"{rotulo} (s/N): ").strip().lower() in ("s", "sim")


# Exibição


def mostrar_lista(itens, formatar):
    if not itens:
        print("Nenhum registro encontrado.")
        return
    for item in itens:
        print(formatar(item))


def formatar_data(data):
    return data.strftime("%d/%m/%Y")


def formatar_autor(autor):
    return f"[{autor.id_autor}] {autor.nome_autor} ({autor.pais})"


def formatar_livro(par):
    livro, autores = par
    return (
        f"[{livro.id_livro}] {livro.nome_livro} ({livro.ano_publicacao}) | "
        f"Autores: {autores or '-'} | Cópias: {livro.copias}"
    )


def formatar_usuario(usuario):
    return (
        f"[{usuario.id_usuario}] {usuario.nome_usuario} | {usuario.telefone} | "
        f"{usuario.email} | {usuario.rua}, {usuario.numero} - {usuario.bairro}"
    )


def formatar_emprestimo(linha):
    id_emprestimo, usuario, livro, retirada, previsao = linha
    return (
        f"[{id_emprestimo}] {livro} | Usuário: {usuario} | "
        f"Retirada: {formatar_data(retirada)} | Devolver até: {formatar_data(previsao)}"
    )


def formatar_livro_disponivel(linha):
    id_livro, nome, ano, copias, autores = linha
    return f"[{id_livro}] {nome} ({ano}) | Autores: {autores or '-'} | Cópias: {copias}"


def formatar_relatorio_usuario(linha):
    id_usuario, nome, total, abertos = linha
    return f"[{id_usuario}] {nome} | Empréstimos: {total} | Em aberto: {abertos}"


# Autores


def cadastrar_autor(autores):
    nome = ler_texto("Nome: ")
    pais = ler_texto("País: ")
    print(f"Autor cadastrado com id {autores.criar_autor(nome, pais)}.")


def buscar_autor(autores):
    mostrar_lista(autores.buscar_autor(ler_texto("Id ou nome exato: ")), formatar_autor)


def listar_autores(autores):
    mostrar_lista(autores.listar_autor(), formatar_autor)


def atualizar_autor(autores):
    id_autor = ler_inteiro("Id do autor: ")
    print("Deixe em branco para manter o valor atual.")
    dados = {
        "nome_autor": ler_opcional("Novo nome: "),
        "pais": ler_opcional("Novo país: "),
    }
    if all(valor is None for valor in dados.values()):
        print("Nada para alterar.")
        return
    autores.atualizar_autor(id_autor, **dados)
    print("Autor atualizado.")


# Livros


def cadastrar_livro(livros, autores):
    lista_autores = autores.listar_autor()
    if not lista_autores:
        print("Cadastre um autor antes de cadastrar um livro.")
        return
    print("Autores disponíveis:")
    mostrar_lista(lista_autores, formatar_autor)

    nome = ler_texto("Título: ")
    ano = ler_inteiro("Ano de publicação: ", minimo=0)
    copias = ler_inteiro("Cópias: ", minimo=0)
    ids_autores = ler_ids("Ids dos autores (exemplo: 1, 2): ")
    print(f"Livro cadastrado com id {livros.criar_livro(nome, ano, copias, ids_autores)}.")


def buscar_livro(livros):
    mostrar_lista(livros.buscar_livro(ler_texto("Id ou parte do título: ")), formatar_livro)


def buscar_livros_com_filtros(livros):
    print("Deixe em branco os filtros que não quiser usar.")
    titulo = ler_opcional("Título: ")
    autor = ler_opcional("Autor: ")
    ano = ler_inteiro("Ano: ", opcional=True)
    mostrar_lista(livros.buscar_livros(titulo=titulo, autor=autor, ano=ano), formatar_livro)


def listar_livros(livros):
    mostrar_lista(livros.listar_livros(), formatar_livro)


def atualizar_livro(livros):
    id_livro = ler_inteiro("Id do livro: ")
    print("Deixe em branco para manter o valor atual.")
    dados = {
        "nome_livro": ler_opcional("Novo título: "),
        "ano_publicacao": ler_inteiro("Novo ano: ", minimo=0, opcional=True),
        "copias": ler_inteiro("Novo total de cópias: ", minimo=0, opcional=True),
        "ids_autores": ler_ids("Novos ids de autores (exemplo: 1, 2): ", opcional=True),
    }
    if all(valor is None for valor in dados.values()):
        print("Nada para alterar.")
        return
    livros.atualizar_livro(id_livro, **dados)
    print("Livro atualizado.")


# Usuários


def cadastrar_usuario(usuarios):
    usuarios.criar_usuario(
        ler_texto("Nome: "),
        ler_texto("Telefone: "),
        ler_texto("E-mail: "),
        ler_texto("Rua: "),
        ler_texto("Número: "),
        ler_texto("Bairro: "),
    )
    print("Usuário cadastrado.")


def buscar_usuario(usuarios):
    mostrar_lista(usuarios.buscar_usuario(ler_texto("Id ou nome exato: ")), formatar_usuario)


def listar_usuarios(usuarios):
    mostrar_lista(usuarios.listar_usuario(), formatar_usuario)


def atualizar_usuario(usuarios):
    id_usuario = ler_inteiro("Id do usuário: ")
    print("Deixe em branco para manter o valor atual.")
    dados = {
        "nome": ler_opcional("Novo nome: "),
        "telefone": ler_opcional("Novo telefone: "),
        "email": ler_opcional("Novo e-mail: "),
        "rua": ler_opcional("Nova rua: "),
        "numero": ler_opcional("Novo número: "),
        "bairro": ler_opcional("Novo bairro: "),
    }
    if all(valor is None for valor in dados.values()):
        print("Nada para alterar.")
        return
    usuarios.atualizar_usuario(id_usuario, **dados)
    print("Usuário atualizado.")


def desativar_usuario(usuarios):
    id_usuario = ler_inteiro("Id do usuário: ")
    if not confirmar("Confirma a desativação?"):
        print("Operação cancelada.")
        return
    usuarios.deletar_usuario(id_usuario)
    print("Usuário desativado.")


# Empréstimos


def registrar_emprestimo(emprestimos):
    id_usuario = ler_inteiro("Id do usuário: ")
    id_livro = ler_inteiro("Id do livro: ")
    emprestimos.registrar_emprestimo(id_usuario, id_livro)
    print("Empréstimo registrado. Devolução prevista em 7 dias.")


def devolver_livro(emprestimos):
    emprestimos.devolver_livro(ler_inteiro("Id do empréstimo: "))
    print("Devolução registrada.")


def listar_emprestimos_abertos(emprestimos):
    mostrar_lista(emprestimos.listar_emprestimos_abertos(), formatar_emprestimo)


def listar_emprestimos_do_usuario(emprestimos):
    id_usuario = ler_inteiro("Id do usuário: ")
    mostrar_lista(emprestimos.listar_emprestimos_abertos_usuario(id_usuario), formatar_emprestimo)


# Menus


def executar(conexao, acao):
    try:
        acao()
    except ValueError as erro:
        print(f"Erro: {erro}")
    except psycopg2.Error as erro:
        if conexao.closed:
            raise
        # Leituras não fazem rollback, e sem ele a conexão ficaria inutilizável.
        conexao.rollback()
        if isinstance(erro, errors.ForeignKeyViolation):
            print("Erro: algum id informado não existe.")
        else:
            print(f"Erro no banco: {erro.diag.message_primary}")


def rodar_menu(conexao, titulo, opcoes, rotulo_saida="Voltar"):
    while True:
        print(f"\n=== {titulo} ===")
        for numero, (rotulo, _) in enumerate(opcoes, start=1):
            print(f"{numero}. {rotulo}")
        print(f"0. {rotulo_saida}")

        escolha = input("Opção: ").strip()
        if escolha == "0":
            return
        if not escolha.isdecimal() or not 1 <= int(escolha) <= len(opcoes):
            print("Opção inválida.")
            continue
        _, acao = opcoes[int(escolha) - 1]
        executar(conexao, acao)


def menu_principal(conexao):
    autores = ServicoAutor(conexao)
    livros = ServicoLivro(conexao)
    usuarios = ServicoUsuario(conexao)
    emprestimos = ServicoEmprestimo(conexao)
    relatorios = ServicoRelatorio(conexao)

    menu_livros = [
        ("Cadastrar", lambda: cadastrar_livro(livros, autores)),
        ("Buscar por id ou título", lambda: buscar_livro(livros)),
        ("Buscar com filtros", lambda: buscar_livros_com_filtros(livros)),
        ("Listar", lambda: listar_livros(livros)),
        ("Atualizar", lambda: atualizar_livro(livros)),
    ]
    menu_autores = [
        ("Cadastrar", lambda: cadastrar_autor(autores)),
        ("Buscar", lambda: buscar_autor(autores)),
        ("Listar", lambda: listar_autores(autores)),
        ("Atualizar", lambda: atualizar_autor(autores)),
    ]
    menu_usuarios = [
        ("Cadastrar", lambda: cadastrar_usuario(usuarios)),
        ("Buscar", lambda: buscar_usuario(usuarios)),
        ("Listar", lambda: listar_usuarios(usuarios)),
        ("Atualizar", lambda: atualizar_usuario(usuarios)),
        ("Desativar", lambda: desativar_usuario(usuarios)),
    ]
    menu_emprestimos = [
        ("Registrar empréstimo", lambda: registrar_emprestimo(emprestimos)),
        ("Registrar devolução", lambda: devolver_livro(emprestimos)),
        ("Listar em aberto", lambda: listar_emprestimos_abertos(emprestimos)),
        ("Listar em aberto de um usuário", lambda: listar_emprestimos_do_usuario(emprestimos)),
    ]
    menu_relatorios = [
        (
            "Livros disponíveis",
            lambda: mostrar_lista(
                relatorios.relatorio_livros_disponiveis(), formatar_livro_disponivel
            ),
        ),
        (
            "Livros emprestados",
            lambda: mostrar_lista(
                relatorios.relatorio_livros_emprestados(), formatar_emprestimo
            ),
        ),
        (
            "Usuários",
            lambda: mostrar_lista(relatorios.relatorio_usuarios(), formatar_relatorio_usuario),
        ),
    ]

    rodar_menu(
        conexao,
        "Biblioteca",
        [
            ("Livros", lambda: rodar_menu(conexao, "Livros", menu_livros)),
            ("Autores", lambda: rodar_menu(conexao, "Autores", menu_autores)),
            ("Usuários", lambda: rodar_menu(conexao, "Usuários", menu_usuarios)),
            ("Empréstimos", lambda: rodar_menu(conexao, "Empréstimos", menu_emprestimos)),
            ("Relatórios", lambda: rodar_menu(conexao, "Relatórios", menu_relatorios)),
        ],
        rotulo_saida="Sair",
    )


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
