class Livro:
    """Um livro do acervo. 'copias' é quantos exemplares estão disponíveis agora."""
    def __init__(self, id_livro, nome_livro, ano_publicacao, copias):
        self.id_livro = id_livro
        self.nome_livro = nome_livro
        self.ano_publicacao = ano_publicacao
        self.copias = copias