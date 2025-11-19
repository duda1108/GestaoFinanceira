from openpyxl import Workbook
from GestaoFinanceira.Transacoes import transacoes
from GestaoFinanceira.ListarTransacoes import vizualizar

usuarios = {}  # dicionário em memória: {nome: senha}


def cadastrar_usuario():
    print("--------- CADASTRO ---------")
    nome = input("Digite um nome de usuário: ").strip()
    if nome == "":
        print("Nome de usuário não pode ser vazio.")
        return
    if nome in usuarios:
        print("Usuário já existe. Tente outro nome.")
        return

    senha = input("Digite uma senha: ").strip()
    if senha == "":
        print("Senha não pode ser vazia.")
        return

    usuarios[nome] = senha
    print(f"Usuário '{nome}' cadastrado com sucesso!")


def fazer_login():
    print("\n--------- LOGIN ---------")
    nome = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    if nome in usuarios and usuarios[nome] == senha:
        print(f"Login bem-sucedido! Bem-vindo, {nome}.")
        return nome
    else:
        print("Usuário ou senha inválidos.")
        return None

import os
from openpyxl import Workbook, load_workbook

FILENAME = "Gestao_Financeira.xlsx"

def criar_planilha(filename=FILENAME):

    if os.path.exists(filename):
        wb = load_workbook(filename)
        ws = wb.active
        return wb, ws

    wb = Workbook()
    ws = wb.active
    ws.title = "Janeiro"
    meses = ["Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro",
             "Novembro", "Dezembro"]
    for m in meses:
        wb.create_sheet(m)

    # Cabeçalho: incluiu "ID" para manter compatibilidade com (tid, tipo, cat, valor, data, desc)
    for sheet in wb.worksheets:
        sheet.append(["ID", "Tipo", "Categoria", "Valor", "Data", "Descrição"])

    wb.save(filename)
    return wb, ws


def menu_inicial():
    while True:
        print("\n================= MENU INICIAL =================")
        print("1 - Cadastrar novo usuário")
        print("2 - Login")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            cadastrar_usuario()

        elif escolha == "2":
            usuario_logado = fazer_login()
            if usuario_logado is not None:
                wb, ws = criar_planilha(FILENAME)

                # Loop do menu financeiro (após login)
                while True:
                    print("\n================= MENU PRINCIPAL =================")
                    print("Bem vindo à sua gestão financeira! Selecione o que deseja:")
                    print(" 1- Adicionar transação")
                    print(" 2- Remover transação")
                    print(" 3- Listar Transação por categoria")
                    print(" 4- Listar Transação por período")
                    print(" 5- Vizualizar o saldo")
                    print(" 0- Encerrar")

                    escolha_n = input("Escolha a opção que deseja: ").strip()
                    try:
                        n = int(escolha_n)
                    except ValueError:
                        print("Opção inválida. Digite um número.")
                        continue

                    # chama transacoes (que lida com adicionar/remover etc)
                    resultado = transacoes(n, ws, wb)

                    # chama vizualizar apenas para opções que exibem (3,4,5)
                    resultado1 = None
                    if n in (3, 4, 5):
                        resultado1 = vizualizar(n, ws, wb)

                    # salvar a cada alteração/iteração (opcional mas seguro)
                    try:
                        wb.save(FILENAME)
                    except Exception as e:
                        print("Aviso: não foi possível salvar o arquivo:", e)

                    # condições de quebra/retorno esperadas pela sua lógica
                    if resultado == "quebra" or resultado1 == "quebra":
                        # pode querer fazer um logout (voltar ao menu inicial)
                        print("Encerrando sessão do usuário.")
                        break

                    if n == 0:
                        print("Encerrando sessão do usuário.")
                        break

                # após logout do usuário, volta ao menu inicial (não encerra o programa)
        elif escolha == "0":
            print("Encerrando programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu_inicial()