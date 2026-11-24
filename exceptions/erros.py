"""Erros das regras do sistema de biblioteca.

Todos herdam de ErroBiblioteca, que herda de ValueError. Assim o menu pode
capturar só ErroBiblioteca e mostrar a mensagem sem derrubar o programa.
"""


class ErroBiblioteca(ValueError):
    """Base de todos os erros de regra do sistema."""


class LivroSemAutor(ErroBiblioteca):
    """Tentou cadastrar ou atualizar um livro sem nenhum autor."""


class AutorNaoEncontrado(ErroBiblioteca):
    """Não existe autor com o id informado."""


class LivroNaoEncontrado(ErroBiblioteca):
    """Não existe livro com o id informado."""


class UsuarioNaoEncontrado(ErroBiblioteca):
    """Não existe usuário ativo com o id informado."""


class EmprestimoNaoEncontrado(ErroBiblioteca):
    """O empréstimo não existe ou já foi devolvido."""


class LivroIndisponivel(ErroBiblioteca):
    """O livro existe, mas não tem nenhuma cópia disponível."""


class UsuarioComPendencia(ErroBiblioteca):
    """O usuário ainda tem livro para devolver, então não pode ser desativado."""
