# GestaoFinanceira/ListarTransacoes.py

from datetime import datetime

def vizualizar(n, ws, wb):

#========================== Listar por categoria ============================
    if n == 3:
        categoria = input("Informe a categoria (ex: Alimentação, Moradia, Vestuário, Outros): ").strip().capitalize()  #deixar string e maisculo inicial

        print("\n========== transações por categoria ========")
        achou = False

        for wsx in wb.worksheets:
            for row in wsx.iter_rows(min_row=2, values_only=True):
                if not row:
                    continue
                (tid, tipo, cat, valor, data, desc) = row
                if cat and cat.capitalize() == categoria:
                    achou = True
                    print(f"[{wsx.title}] ID:{tid} | {tipo} | {cat} | R${valor} | {data} | {desc}")

        if not achou:
            print("Nenhuma transação encontrada para essa categoria.")

        return None


#=========================== Listar por periodo ================================
    if n == 4:
        print("Informe o intervalo de datas:")
        d1 = input("Data inicial (ex: 01/01/2025): ").strip()
        d2 = input("Data final   (ex: 31/01/2025): ").strip()

        try:
            d1p = datetime.strptime(d1, "%d/%m/%Y")
            d2p = datetime.strptime(d2, "%d/%m/%Y")
        except:
            print("Datas inválidas! Use o formato DD/MM/AAAA.")
            return None

        print("\n========== TRANSAÇÕES POR PERÍODO ==========")
        achou = False

        for wsx in wb.worksheets:
            for row in wsx.iter_rows(min_row=2, values_only=True):
                if not row or not row[4]:
                    continue
                (tid, tipo, cat, valor, data, desc) = row

                try:
                    data_convertida = datetime.strptime(data, "%d/%m/%Y")
                except:
                    continue

                if d1p <= data_convertida <= d2p:
                    achou = True
                    print(f"[{wsx.title}] ID:{tid} | {tipo} | {cat} | R${valor} | {data} | {desc}")

        if not achou:
            print("Nenhuma transação encontrada neste periodo.")

        return None


#=============================== Saldo por periodo ========================================
    if n == 5:
        print("Informe o intervalo de datas:")
        d1 = input("Data inicial (ex: 01/01/2025): ").strip()
        d2 = input("Data final (ex: 31/01/2025): ").strip()

    #separação
        try:
            d1p = datetime.strptime(d1, "%d/%m/%Y")
            d2p = datetime.strptime(d2, "%d/%m/%Y")
        except:
            print("Datas inválidas! Use o formato DD/MM/AAAA.")
            return None

        total_entradas = 0
        total_saidas = 0

    #olhar as colunas e buscar os valores do periodo q o clinete pediu
        for wsx in wb.worksheets:
            for row in wsx.iter_rows(min_row=2, values_only=True):
                if not row or not row[4]:
                    continue
                (tid, tipo, cat, valor, data, desc) = row

            #tentar achar data
                try:
                    data_convertida = datetime.strptime(data, "%d/%m/%Y")
                except:
                    continue

                #calculo entrada saida e saldo
                if d1p <= data_convertida <= d2p:
                    if tipo == "Entrada":
                        total_entradas += valor
                    elif tipo == "Saída":
                        total_saidas += valor

        saldo = total_entradas - total_saidas

        print("\n========== SALDO DO PERÍODO ==========")
        print(f"Entradas: R${total_entradas}")
        print(f"Saídas: R${total_saidas}")
        print(f"Saldo: R${saldo}")

        return None

    return None
