from time import sleep
from turtle import width
from passlib.hash import pbkdf2_sha256 as cryp
from csv import writer, reader
import os
from datetime import datetime, timedelta
from tkinter import *


class Cadastro:

    def __init__(self, nome: str, email: str, senha: str):
        self.__nome: str = nome
        self.__email: str = email
        self.__senha: str = cryp.hash(senha, rounds=200000, salt_size=16)

    def __str__(self) -> str:
        return 'Essa é uma classe do tipo Cadastro'

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def email(self) -> str:
        return self.__email

    @property
    def senha(self) -> str:
        return self.__senha

    def user(self) -> str:
        return self.__email.split('@')[0]


class User(Cadastro):
    count = 0

    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email, senha)
        self.__num: int = User.count + 1
        User.count = self.__num

    def __str__(self) -> str:
        return 'Essa é uma classe do tipo User'

    @classmethod
    def contador(cls) -> str:
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
        janela_cadastro.title('Cadastro')

        texto_cadastro = Label(
            janela_cadastro,
            text='CADASTRO'
        ).grid(column=0, row=0, padx=10, pady=10, sticky='nswe', columnspan=4)
        nome_texto = Label(
            janela_cadastro,
            text='Digite o seu nome de usuário'
        ).grid(column=0, row=1, padx=10, pady=10, sticky='nswe', columnspan=4)
        entry_nome = Entry(janela_cadastro)
        entry_nome.grid(column=0, row=2, padx=10, pady=10,
                        sticky='nswe', columnspan=4)

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
                    text='Digite o seu email'
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

        botao_nome = Button(janela_cadastro, text='Continuar',
                            command=func_nome)
        botao_nome.grid(column=0, row=3, padx=60, pady=10, sticky='nswe',
                        columnspan=4)

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
                    text='Crie uma senha'
                ).grid(column=0, row=1, padx=10, pady=10,
                       sticky='nswe', columnspan=4)

                global entry_senha_cadastro
                entry_senha_cadastro = Entry(janela_cadastro)
                entry_senha_cadastro.grid(column=0, row=2, padx=10, pady=10,
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
            if len(entry_senha_cadastro.get()) >= 8:
                texto_cadastro_fim = Label(
                    janela_cadastro,
                    text='Cadastro efetuado! Feche a janela.'
                ).grid(column=0, row=4, padx=10, pady=10,
                       sticky='nswe', columnspan=4)
                user = User(entry_nome.get(), entry_email.get(),
                            entry_senha_cadastro.get())
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

        janela_cadastro.mainloop()
        janela_principal()


def logar():
    try:
        janela.destroy()
    except TclError:
        pass
    janela_logar = Tk()
    janela_logar.title('Login')

    texto_logar = Label(
            janela_logar,
            text='LOGAR',
        ).grid(column=0, row=0, padx=10, pady=10, sticky='nswe', columnspan=4)

    nome_ou_email_texto = Label(
        janela_logar,
        text='Digite o seu nome de usuário ou o email'
    ).grid(column=0, row=1, padx=10, pady=10, sticky='nswe', columnspan=4)
    entry_nome_email = Entry(janela_logar)
    entry_nome_email.grid(column=0, row=2, padx=10, pady=10,
                          sticky='nswe', columnspan=4)

    senha_texto = Label(
        janela_logar,
        text='Digite a sua senha'
    ).grid(column=0, row=3, padx=10, pady=10, sticky='nswe', columnspan=4)
    entry_senha_logar = Entry(janela_logar)
    entry_senha_logar.grid(column=0, row=4, padx=10, pady=10, sticky='nswe',
                           columnspan=4)

    def limite():
        for n in range(10, -1, -1):
            segundostexto = Label(
                                janela_logar,
                                text=f'Aguarde {n} segundo(s).',
                                foreground='red'
                            ).grid(column=0, row=5, padx=0, pady=0,
                                   sticky='nswe', columnspan=4)
            janela_logar.after(1000)
            janela_logar.update()
        global chances_login
        chances_login += 5
        janela_logar.destroy()
        logar()

    def func_nome_email():
        global chances_login
        if chances_login > 0:
            nome_email = entry_nome_email.get()

            if len(nome_email) > 0 and len(entry_senha_logar.get()) >= 8:
                if nome_email[0] != '@' and nome_email[-4:] == '.com' and \
                 nome_email[-11:-4] == 'hotmail' or nome_email[-9:-4] \
                 == 'gmail' and '@' in nome_email and \
                 len(entry_senha_logar.get()) >= 8:
                    with open('usuarios.csv') as arq:
                        lei_csv = reader(arq)
                        verify = 0

                        for n in lei_csv:
                            if entry_nome_email.get() == n[1] \
                             and cryp.verify(entry_senha_logar.get(), n[2]):
                                verify += 1
                                bem_vindo_texto = Label(
                                    janela_logar,
                                    text=f'Seja bem-vindo {n[0]}'
                                ).grid(column=0, row=6, padx=10, pady=10,
                                       sticky='nswe', columnspan=4)
                            else:
                                pass
                        if verify == 0:
                            print('ok')
                            attempts -= 1
                            incorreto_texto = Label(
                                janela_logar,
                                text=f'Email ou senha incorretos! \
                                {attempts} restantes.',
                                foreground='red'
                            ).grid(column=0, row=6, padx=10, pady=10,
                                   sticky='nswe', columnspan=4)
                else:
                    with open('usuarios.csv') as arq:
                        lei_csv = reader(arq)
                        verify = 0

                        for n in lei_csv:
                            if entry_nome_email.get().title() == n[0].title() \
                             and cryp.verify(entry_senha_logar.get(), n[2]):
                                verify += 1
                                bem_vindo_texto = Label(
                                    janela_logar,
                                    text=f'Seja bem-vindo {n[0]}'
                                ).grid(column=0, row=6, padx=10, pady=10,
                                       sticky='nswe', columnspan=4)
                            else:
                                pass
                        if verify == 0:
                            chances_login -= 1
                            incorreto_texto = Label(
                                janela_logar,
                                text=f'Usuário ou senha incorretos!\n{chances_login} tentativas restantes.',
                                foreground='red'
                            ).grid(column=0, row=6, padx=10, pady=10,
                                   sticky='nswe', columnspan=4)
                            if chances_login == 0:
                                erro_logar_texto = Label(
                                    janela_logar,
                                    text='Limite de tentativas excedido!',
                                    foreground='red'
                                ).grid(column=0, row=6, padx=10, pady=10,
                                       sticky='nswe', columnspan=4)
                                limite()
            else:
                user_ou_senha_texto = Label(
                                janela_logar,
                                text=f'Digite um usuário ou senha válido.',
                                foreground='red'
                            ).grid(column=0, row=6, padx=10, pady=10,
                                   sticky='nswe', columnspan=4)
        else:
            erro_logar_texto = Label(
                                janela_logar,
                                text='Limite de tentativas excedido!',
                                foreground='red'
                            ).grid(column=0, row=6, padx=10, pady=10,
                                   sticky='nswe', columnspan=4)
            limite()

    global chances_login
    chances_login = 5
    botao_nome_email = Button(janela_logar, text='Continuar',
                              command=func_nome_email)
    botao_nome_email.grid(column=0, row=5, padx=60, pady=10,
                          sticky='nswe', columnspan=4)
    janela_logar.mainloop()


def janela_principal():
    global janela
    janela = Tk()
    janela.title('Faça o login ou se cadastre')

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
