class Usuarios:
    def __init__(self, id, nome, email) -> None:
        self.id = id
        self.nome = nome
        self.email = email

        self.base_de_dados = [

            Usuarios(id=1, nome='Alexandre', email='aleleonel@gmail.com'),
            Usuarios(id=2, nome='Alexandre', email='aleleonel@gmail.com'),
            Usuarios(id=3, nome='AlexLeonel',
                     email='aleleonelcomercial2@gmail.com')
        ]

    def deleta_registro(self, user_id):
        self.user_id = user_id
        for x in range(len(self.base_de_dados)):
            if self.user_id == self.base_de_dados[x].id:
                del(self.base_de_dados[x])
                print("\nRegistro excluido!\n")
            else:
                print("\nRegistro não encontrado\n")


deleta = Usuarios(2, 'Alexandre', 'aleleonel@gmail.com')
