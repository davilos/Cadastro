from cadastro import Cadastro, User
import unittest


class CadastroTestes(unittest.TestCase):

    def setUp(self) -> None:
        self.cadastro_test = Cadastro('Dávilos', 'davilosfulano@hotmail.com',
                                      1234)


class UserTestes(unittest.TestCase):

    def setUp(self) -> None:
        self.user_test = User('Gabriel', 'gabrielfulano@gmail.com', 4321)

    def tearDown(self) -> None:
        print('tearDown executando...')
