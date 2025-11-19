# GestaoFinanceira/Transacoes.py
from openpyxl import load_workbook
import os
from datetime import datetime

FNAME = "Gestao_Financeira.xlsx"
MESES = ["Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
CATEGORIAS = {"1":"Alimentação","2":"Moradia","3":"Vestuário","4":"Outros"}


#=============================== ID ====================================
def ID(wb):
    max_id = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row:
                continue
            try:
                cell = row[0]
                if cell is None:
                    continue
                iid = int(cell)
                if iid > max_id:
                    max_id = iid
            except Exception:
                continue
    return max_id + 1

#================================= Transasções =================================
def transacoes(n, ws, wb):
    #-------------------------- ADICIONAR -----------------------------
    if n == 1:
        print("-----------------------------------------------------------------------")
        data_str = input("Informe a data da transação (ex: 12/10 ou 12/10/2025): ").strip()
        if data_str == "":
            print("Data não pode ser vazia. Operação abortada.")
            return None

        # TIPO
        try:
            tipo_in = int(input("Me informe qual foi o tipo de transação:\n1. Entrada \n2. Saída\n"))
        except ValueError:
            print("Entrada inválida. Operação abortada.")
            return None
        if tipo_in == 1:
            tipo = "Entrada"
        elif tipo_in == 2:
            tipo = "Saída"
        else:
            print("Você deve digitar 1 ou 2. Operação abortada.")
            return None

        # CATEGORIA
        categoria = input("Qual seria a categoria da transação:\n1- Alimentação\n2- Moradia\n3- Vestuário\n4- Outros\nEscolha (número ou nome): ").strip()
        if categoria == "":
            print("Categoria vazia. Operação abortada.")
            return None
        if categoria in CATEGORIAS:
            categoria = CATEGORIAS[categoria]
        else:
            cap = categoria.capitalize()
            if cap in CATEGORIAS.values():
                categoria = cap
            else:
                print("Categoria inválida. Operação abortada.")
                return None

        # VALOR
        val_in = input("Informe o valor (use . como separador decimal): ").strip()
        try:
            valor = float(val_in)
            if valor <= 0:
                print("Valor deve ser positivo. Operação abortada.")
                return None
        except ValueError:
            print("Valor inválido. Operação abortada.")
            return None

        descricao = input("Descrição (opcional): ").strip()

        # ESCOLHA DE PLANILHA
        escolha = input("Deseja usar a planilha ativa (a) ou escolher outro mês (c)? Digite 'a' ou 'c': ").strip().lower()
        if escolha == 'c':
            meses_full = ["Janeiro"] + MESES
            print("Escolha o mês (1-12):")
            for idx, m in enumerate(meses_full, start=1):
                print(f"{idx:2d} - {m}")
            sel_in = input("Mês (1-12): ").strip()
            try:
                sel = int(sel_in)
            except ValueError:
                print("Entrada inválida. Operação abortada.")
                return None
            if 1 <= sel <= 12:
                sheet_name = meses_full[sel-1]
                if sheet_name not in wb.sheetnames:
                    wb.create_sheet(sheet_name)
                ws_target = wb[sheet_name]
            else:
                print("Número fora do intervalo. Operação abortada.")
                return None
        else:
            ws_target = ws

        tid = ID(wb)
        ws_target.append([tid, tipo, categoria, valor, data_str, descricao])
        wb.save(FNAME)
        print(f"Transação adicionada com ID {tid} na planilha {ws_target.title}.")
        return None

#======================= Remover transação =========================
    elif n == 2:
        id_in = input("Informe o ID da transação a remover (ou 'c' para cancelar): ").strip()
        if id_in.lower() == 'c' or id_in == "":
            print("Operação cancelada.")
            return None
        try:
            id_rem = int(id_in)
        except ValueError:
            print("ID inválido.")
            return None

        for wsx in wb.worksheets:
            for row_idx, cells in enumerate(wsx.iter_rows(min_row=2), start=2):
                cell_id = cells[0].value
                if cell_id == id_rem:
                    tipo = cells[1].value; categoria = cells[2].value; valor = cells[3].value; data = cells[4].value; desc = cells[5].value
                    print(f"Encontrado na planilha {wsx.title}: ID {cell_id} | {tipo} | {categoria} | {valor} | {data} | {desc}")
                    confirma = input("Confirmar remoção? (s/n): ").strip().lower()
                    if confirma == 's':
                        wsx.delete_rows(row_idx, 1)
                        wb.save(FNAME)
                        print("Transação removida.")
                        return None
                    else:
                        print("Remoção cancelada.")
                        return None
        print("ID não encontrado.")
        return None

#======================== Encerrar ===========================
    elif n == 0:
        print("Encerrando...")
        return "quebra"

    # outras opções: retorno imediato (evita loops)
    else:
        return None
