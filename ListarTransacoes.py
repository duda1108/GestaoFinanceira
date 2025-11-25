# GestaoFinanceira/ListarTransacoes.py
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


def vizualizar(n, ws, wb):
    #print(f"DEBUG vizualizar chamado com n={n!r}, type={type(n)}")
#========================== Listar por categoria ============================
    if n == 3:
        print("\n========== Transações por categoria ==========\n")

        categorias = {}  # chave = categoria, valor = lista de textos formatados
        despesas = {}  # chave = categoria, valor = soma das saídas (apenas Saída)

        # Percorre todas as linhas existentes no excel
        for wsx in wb.worksheets:
            for row in wsx.iter_rows(min_row=2, values_only=True):
                if not row:
                    continue

                # Prevenção contra erro de linha incompleta
                row = tuple(row) + (None,) * max(0, 6 - len(row))
                tid, tipo, cat, valor, data, desc = row

                if not cat:
                    continue

                # Cria categoria se ainda não existir (para listar)
                if cat not in categorias:
                    categorias[cat] = []

                # Adiciona transação em seu respectivo grupo (string formatada)
                categorias[cat].append(
                    f"[{wsx.title}] ID:{tid} | {tipo} | {cat} | R${valor} | {data} | {desc}"
                )

                # Acumula apenas as SAÍDAS para o gráfico
                if tipo is not None:
                    # normaliza o texto do tipo para comparar (aceita "Saída", "Saida", "saída", "saida")
                    tnorm = str(tipo).strip().lower()
                    if tnorm.startswith("s"):  # assume 's' de Saída/saida
                        try:
                            v = float(valor) if valor is not None else 0.0
                        except Exception:
                            # se não conseguir converter, considera 0 e segue
                            v = 0.0
                        despesas[cat] = despesas.get(cat, 0.0) + v

        # Agora imprime tudo de forma separada por categoria
        if not categorias:
            logger.info("Listagem por categoria: nenhuma transação encontrada")
            print("Nenhuma transação encontrada.")
            return None
        for cat in categorias:
            logger.info("Listagem por categoria concluída: categorias=%s", list(categorias.keys()))
            print(f"\n--- categoria: {cat} ---")
            for linha in categorias[cat]:
                print(linha)

        # --- Cria gráfico de pizza com as SAÍDAS por categoria ---
        # Filtra apenas categorias com valor positivo
        gasto_labels = []
        gasto_sizes = []
        for cat, total in despesas.items():
            try:
                total_f = float(total)
            except Exception:
                total_f = 0.0
            if total_f > 0:
                gasto_labels.append(cat)
                gasto_sizes.append(total_f)

        if not gasto_sizes:
            print("\nNenhuma saída encontrada para gerar gráfico de pizza.")
            return None

        # Import local para não forçar alteração no topo do arquivo
        try:
            import matplotlib.pyplot as plt
        except Exception as e:
            print(f"\nNão foi possível importar matplotlib para gerar o gráfico: {e}")
            return None

        try:
            plt.pie(gasto_sizes, labels=gasto_labels, autopct="%1.1f%%")
            plt.title("Distribuição das saídas por categoria")
            plt.show()
        except ValueError as e:
            # Captura erros como valores negativos ou soma <= 0
            print(f"\nNão foi possível gerar o gráfico de pizza: {e}")

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
                if not row:
                    continue

                # Prevenção contra error
                row = tuple(row) + (None,) * max(0, 6 - len(row))
                tid, tipo, cat, valor, data, desc = row

                try:
                    data_convertida = datetime.strptime(data, "%d/%m/%Y")
                except:
                    continue

                if d1p <= data_convertida <= d2p:
                    achou = True
                    print(f"[{wsx.title}] ID:{tid} | {tipo} | {cat} | R${valor} | {data} | {desc}")

        if not achou:
            logger.info("Listagem por período: nenhuma transação encontrada entre %s e %s", d1, d2)
            print("Nenhuma transação encontrada neste periodo.")


        return None
#============================== Transações ao longo do tempo =================================
    if n == 5:
        # Lista todas as transações com data, tipo e valor
        transacoes = []

        for wsx in wb.worksheets:
            for row in wsx.iter_rows(min_row=2, values_only=True):
                if not row:
                    continue
                row = tuple(row) + (None,) * max(0, 6 - len(row))
                tid, tipo, cat, valor, data, desc = row

                if data is None:
                    continue

                try:
                    dt = datetime.strptime(data, "%d/%m/%Y")
                except:
                    continue

                # Converte valor
                try:
                    if isinstance(valor, str):
                        v = float(valor.replace(",", "."))
                    else:
                        v = float(valor) if valor is not None else 0.0
                except:
                    v = 0.0

                tnorm = str(tipo).strip().lower() if tipo else ""
                transacoes.append((dt, tnorm, v))

        if not transacoes:
            print("Nenhuma transação encontrada para gerar o gráfico.")
            return None

        # Ordena por data
        transacoes.sort(key=lambda x: x[0])

        # Calcula saldo acumulado
        saldo = 0.0
        datas = []
        saldos = []

        for dt, tnorm, v in transacoes:
            if tnorm.startswith("e"):
                saldo += v
            elif tnorm.startswith("s"):
                saldo -= v
            saldos.append(saldo)
            datas.append(dt)

        # Gráfico — saldo ao longo do tempo
        try:
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except Exception as e:
            print("Erro ao importar matplotlib:", e)
            return None

        plt.figure(figsize=(10, 4))
        plt.plot(datas, saldos, color="blue", linewidth=2, marker="o")

        plt.title("Saldo Acumulado ao Longo do Tempo")
        plt.xlabel("Data")
        plt.ylabel("Saldo (R$)")
        plt.grid(alpha=0.3)

        # melhora visual das datas
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))
        plt.gcf().autofmt_xdate()

        plt.tight_layout()

        try:
            plt.show()
        except Exception as e:
            print("Erro ao mostrar o gráfico:", e)

        return None
    #=============================== Saldo por periodo ========================================
    if n == 6:
        print("Informe o intervalo de datas:")
        d1 = input("Data inicial (ex: 01/01/2025): ").strip()
        d2 = input("Data final (ex: 31/01/2025): ").strip()

        try:
            d1p = datetime.strptime(d1, "%d/%m/%Y")
            d2p = datetime.strptime(d2, "%d/%m/%Y")
        except ValueError:
            print("Datas inválidas! Use o formato DD/MM/AAAA.")
            return None

        total_entradas = 0
        total_saidas = 0

        for wsx in wb.worksheets:
            for row in wsx.iter_rows(min_row=2, values_only=True):
                if not row:
                    continue

                # Prevenção contra linhas vazias
                row = tuple(row) + (None,) * max(0, 6 - len(row))
                tid, tipo, cat, valor, data, desc = row

                # valida data antes de tentar converter
                if not data:
                    continue
                try:
                    data_convertida = datetime.strptime(str(data), "%d/%m/%Y")
                except (ValueError, TypeError):
                    continue

                # dentro do intervalo
                if d1p <= data_convertida <= d2p:

                    # normaliza tipo
                    tipo_norm = (tipo or "").strip().lower()

                    # valida valor antes de somar
                    try:
                        if isinstance(valor, str):
                            valor_num = float(valor.replace(",", ".").strip())
                        else:
                            valor_num = float(valor)
                    except:
                        continue

                    if tipo_norm == "entrada":
                        total_entradas += valor_num
                    elif tipo_norm in ("saída", "saida"):
                        total_saidas += valor_num

        saldo = total_entradas - total_saidas
        logger.info("Saldo por período calculado: d1=%s d2=%s entradas=%s saidas=%s saldo=%s",
                    d1, d2, total_entradas, total_saidas, saldo)
        print("\n========== SALDO DO PERÍODO ==========")
        print(f"Entradas: R${total_entradas}")
        print(f"Saídas: R${total_saidas}")
        print(f"Saldo: R${saldo}")

        return None

    return None
