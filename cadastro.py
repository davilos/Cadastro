from time import sleep
from passlib.hash import pbkdf2_sha256 as cryp
from csv import writer, reader
import os
from tkinter import *


class Cadastro:

    def __init__(self, nome, email, senha):
        self.__nome = nome
        self.__email = email
        self.__senha = cryp.hash(senha, rounds=200000, salt_size=16)

    def __str__(self):
        return 'Essa é uma classe do tipo Cadastro'

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email

    @property
    def senha(self):
        return self.__senha

    def user(self):
        return self.__email.split('@')[0]


class User(Cadastro):
    count = 0

    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha)
        self.__num = User.count + 1
        User.count = self.__num

    def __str__(self):
        return 'Essa é uma classe do tipo User'

    @classmethod
    def contador(cls):
        return f'Temos {cls.count} usuário(s) no sistema.'


def cadastrar():
    with open('usuarios.csv', 'a+', encoding='utf8', newline='') as arq:
        esc_csv = writer(arq)
        if os.path.exists('usuarios.csv'):
            pass
        else:
            esc_csv.writerow(["Nome", "Email", "Senha"])

        janela.destroy()
        janela_cadastro = Tk()

        texto_cadastro = Label(
            janela_cadastro,
            text='CADASTRO',
        ).grid(column=0, row=0, padx=10, pady=10, sticky='nswe', columnspan=4)
        nome_texto = Label(
            janela_cadastro,
            text='Digite o seu nome de usuário',
        ).grid(column=0, row=1, padx=10, pady=10, sticky='nswe', columnspan=4)

        def func_nome():
            if entry_nome.get() != '':
                with open('usuarios.csv', 'r+') as arq2:
                    lei_csv = reader(arq2)
                    for n in lei_csv:
                        verificador = 0
                        if str(entry_nome.get()).title() == n[0]:
                            verificador += 1
                            texto_user_exit = Label(
                                janela_cadastro,
                                text='Usuário já cadastrado!',
                                foreground='red'
                            ).grid(column=0, row=4, padx=10, pady=10,
                                   sticky='nswe', columnspan=4)
                email_texto = Label(
                    janela_cadastro,
                    text='Digite o seu email',
                ).grid(column=0, row=1, padx=10, pady=10,
                       sticky='nswe', columnspan=4)

                global entry_email
                entry_email = Entry(janela_cadastro)
                entry_email.grid(column=0, row=2, padx=10, pady=10,
                                 sticky='nswe', columnspan=4)
                botao_email = Button(janela_cadastro, text='Continuar',
                                     command=func_email).grid(column=0, row=3,
                                                              padx=60, pady=10,
                                                              sticky='nswe',
                                                              columnspan=4)
            else:
                texto_erro_nome = Label(
                    janela_cadastro,
                    text='Nome inválido',
                    foreground='red'
                ).grid(column=0, row=1, padx=10, pady=10,
                       sticky='nswe', columnspan=4)

        def func_email():
            global email_cadastro
            email_cadastro = entry_email.get()

            if email_cadastro[0] != '@' and email_cadastro[-4:] == '.com' and \
               email_cadastro[-11:-4] == 'hotmail' or \
               email_cadastro[-9:-4] == 'gmail' and '@' in email_cadastro:
                with open('usuarios.csv', 'r+') as arq2:
                    lei_csv = reader(arq2)
                    for n in lei_csv:
                        verificador = 0
                        if str(entry_email.get()).title() == n[1]:
                            verificador += 1
                            texto_user_exit = Label(
                                janela_cadastro,
                                text='Email já cadastrado!',
                                foreground='red'
                            ).grid(column=0, row=4, padx=10, pady=10,
                                   sticky='nswe', columnspan=4)
                senha_texto = Label(
                    janela_cadastro,
                    text='Crie uma senha',
                ).grid(column=0, row=1, padx=10, pady=10,
                       sticky='nswe', columnspan=4)

                global entry_senha
                entry_senha = Entry(janela_cadastro)
                entry_senha.grid(column=0, row=2, padx=10, pady=10,
                                 sticky='nswe', columnspan=4)
                botao_senha = Button(janela_cadastro, text='Continuar',
                                     command=func_senha).grid(column=0, row=3,
                                                              padx=60, pady=10,
                                                              sticky='nswe',
                                                              columnspan=4)
            else:
                texto_erro_email = Label(
                    janela_cadastro,
                    text='Email inválido!',
                    foreground='red'
                ).grid(column=0, row=1, padx=10, pady=10,
                       sticky='nswe', columnspan=4)

        def func_senha():
            if len(entry_senha.get()) >= 8:
                texto_cadastro_fim = Label(
                    janela_cadastro,
                    text='Cadastro efetuado! Feche a janela.'
                ).grid(column=0, row=4, padx=10, pady=10,
                       sticky='nswe', columnspan=4)
                user = User(entry_nome.get(), entry_email.get(),
                            entry_senha.get())
                esc_csv.writerow([
                    user.nome, user.email,
                    user.senha])
            else:
                texto_erro_senha = Label(
                    janela_cadastro,
                    text='Digite uma senha mais forte',
                    foreground='red'
                ).grid(column=0, row=1, padx=10, pady=10,
                       sticky='nswe', columnspan=4)

        entry_nome = Entry(janela_cadastro)
        entry_nome.grid(column=0, row=2, padx=10, pady=10,
                        sticky='nswe', columnspan=4)
        botao_nome = Button(janela_cadastro, text='Continuar',
                            command=func_nome).grid(column=0, row=3, padx=60,
                                                    pady=10, sticky='nswe',
                                                    columnspan=4)
        janela_cadastro.mainloop()
        janela_principal()


def logar():
    attempts = 5

    while attempts > 0:
        option = input('Digite o nome de usuário ou o email: ')
        password = input('Digite a senha: ')
        if '@' and '.com' in option:
            with open('usuarios.csv') as arq:
                lei_csv = reader(arq)
                verificador = 0
                for n in lei_csv:
                    if option == n[1] and cryp.verify(password, n[2]):
                        verificador += 1
                        print(f'Seja bem-vindo {n[0]}')
                    else:
                        pass
                if verificador == 0:
                    attempts -= 1
                    print('\033[31mE-mail ou senha incorretos\033[m')

        else:
            with open('usuarios.csv') as arq:
                lei_csv = reader(arq)
                verificador = 0
                for n in lei_csv:
                    if option.title() == n[0].title() \
                     and cryp.verify(password, n[2]):
                        verificador += 1
                        print(f'Seja bem-vindo {n[0]}')
                    else:
                        pass
                if verificador == 0:
                    attempts -= 1
                    print('\033[31mUsuário ou senha incorretos\033[m')
        print(f'\033[1;97m{attempts} tentativas restantes.\033[1;97m')
    print('\033[31mLimite de tentativas excedido!\033[m')
    janela_principal()


def janela_principal():
    global janela
    janela = Tk()
    janela.title('Cadastro')

    texto_orientacao = Label(
        janela,
        text='Você deseja cadastrar ou logar?',
    ).grid(column=0, row=0, padx=10, pady=10, sticky='nswe', columnspan=4)

    botao_c = Button(
        janela,
        text='Cadastrar',
        command=cadastrar
    ).grid(column=0, row=1, padx=60, pady=10, sticky='nswe', columnspan=4)

    botao_l = Button(
        janela,
        text='Logar',
        command=logar
    ).grid(column=0, row=2, padx=60, pady=10, sticky='nswe', columnspan=4)

    janela.mainloop()


if __name__ == '__main__':
    janela_principal()
