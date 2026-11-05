class Emprestimo:
    def __init__(self, id_emprestimo, usuario, livro, data_retirada, data_prev_devol, data_devol=None):
        self.id_emprestimo = id_emprestimo
        self.usuario = usuario
        self.livro = livro
        self.data_retirada = data_retirada
        self.data_prev_devol = data_prev_devol
        self.data_devol = data_devol