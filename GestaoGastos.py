from openpyxl import Workbook
from GestaoFinanceira.Transacoes import transacoes
from GestaoFinanceira.ListarTransacoes import vizualizar
wb = Workbook()
ws = wb.active
ws.title = "Janeiro"
meses = ["Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
for m in meses:
    wb.create_sheet(m)

    # Cabeçalho em todas as planilhas
for sheet in wb.worksheets:
    sheet.append(["Tipo","Categoria","Valor","Data","Descrição"])
wb.save("Gestao_Financeira.xlsx")

while True:
    print("\n================= MENU PRINCIPAL =================")
    print(f"Bem vindo á sua gestão financeira! Selecione o que deseja: \n 1- Adicionar transação\n 2- Remover transação\n "
          f"3- Listar Tansação por categoria\n 4- Listar Tansação por período\n 5- Vizualizar o saldo\n 0- Encerrar")
    n = int(input(f"Escolha a opção que deseja:"))
    resultado = transacoes(n, ws, wb)
    resultado1 = vizualizar(n, ws, wb)
    if resultado == "quebra":
        break
    elif resultado1 == "quebra":
        break