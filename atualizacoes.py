from db.connection import conecta_banco
import yfinance as yf
from datetime import datetime
from notificacao import enviar_alerta_telegram
from decimal import Decimal
import socket

def is_sql_server_up(host='localhost', port=1433):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except:
        return False

# Função para atualizar cotações
def atualizar_cotacoes():

    if not is_sql_server_up():
        return

    conexao = conecta_banco()
    cursor = conexao.cursor()

    # Buscar todas as ações cadastradas
    cursor.execute("SELECT IDACOES, NMACOES, FLSA, VRMEDIO FROM TB_ACOES")
    acoes = cursor.fetchall()

    for id_acao, nome_acao, flsa_acao, vr_medio in acoes:       

        try:
            # Adiciona sufixo para ações brasileiras
            ticker = nome_acao + '.SA' if flsa_acao.upper() == 'S' else nome_acao
            #print("entrou")
            # Caso especial: BTC
            if id_acao == 12:
                #print("passou1")
                       
                ticker_btc = yf.Ticker("BTC-USD")
                usdbrl = yf.Ticker("USDBRL=X")
                btc_hist = ticker_btc.history(period="1d")
                brl_hist = usdbrl.history(period="1d")
                #print("passou2")

                if not btc_hist.empty and not brl_hist.empty:
                    btc_usd = btc_hist['Close'].iloc[-1]
                    dolar_brl = brl_hist['Close'].iloc[-1]
                    btc_brl = btc_usd * dolar_brl

                    #print("antes update")
                    # Atualiza valor atual
                    cursor.execute("""
                        UPDATE TB_ACOES SET VRATUAL = ?, DTATUALIZACAO = ?, VRTOTAL = QTDACOES*VRATUAL
                        WHERE IDACOES = ?
                    """, (btc_brl, datetime.now(), id_acao))

                    conexao.commit()

                    # Verifica último valor registrado para essa ação
                    cursor.execute("""
                        SELECT TOP 1 VRPRECO
                        FROM TB_HIST_PRECO
                        WHERE IDACOES = ?
                        ORDER BY DTHORA DESC
                    """, (id_acao,))
                    ultimo = cursor.fetchone()

                    # Só insere se for diferente ou se não houver histórico
                    if not ultimo or float(ultimo[0]) != round(btc_brl, 2):
                        cursor.execute("""
                            INSERT INTO TB_HIST_PRECO (IDACOES, DTHORA, VRPRECO)
                            VALUES (?, ?, ?)
                        """, (id_acao, datetime.now(), btc_brl))

                    conexao.commit()

                    percentual_alerta = Decimal("0.10")
                    limite_compra = vr_medio * (Decimal("1.00") + percentual_alerta)
                
                    #print(f"BTC atual: {btc_brl}, VR_MEDIO: {vr_medio}, LIMITE_COMPRA: {limite_compra}")
                    if btc_brl < vr_medio or btc_brl < limite_compra:               
                        enviar_alerta_telegram(nome_acao, vr_medio, btc_brl)

                    #print(f"{nome_acao}: atualizado para R$ {btc_brl:.2f}")
                    conexao.commit()
                    continue

            # Caso especial: IVV (ação americana)
            if id_acao == 13:
                #print("passou")
                
                dados = yf.Ticker(ticker)
                cotacao = dados.history(period="1d")['Close'].iloc[-1]

                cursor.execute("""
                    UPDATE TB_ACOES SET VRATUAL = ?, DTATUALIZACAO = ?, VRTOTAL = QTDACOES*VRATUAL
                    WHERE IDACOES = ?
                """, (cotacao, datetime.now(), id_acao))

                # Verifica último valor registrado para essa ação
                cursor.execute("""
                    SELECT TOP 1 VRPRECO
                    FROM TB_HIST_PRECO
                    WHERE IDACOES = ?
                    ORDER BY DTHORA DESC
                """, (id_acao,))
                ultimo = cursor.fetchone()

                # Só insere se for diferente ou se não houver histórico
                if not ultimo or float(ultimo[0]) != round(cotacao, 2):
                    cursor.execute("""
                        INSERT INTO TB_HIST_PRECO (IDACOES, DTHORA, VRPRECO)
                        VALUES (?, ?, ?)
                    """, (id_acao, datetime.now(), cotacao))

                    enviar_alerta_telegram('nome_acao', 10000, 50)
                    percentual_alerta = 0.05
                    limite_compra = 535.00 #vr_medio * (1 + percentual_alerta)
                    if cotacao < vr_medio or cotacao < limite_compra:
                        enviar_alerta_telegram(nome_acao, vr_medio, cotacao)


                #print(f"{nome_acao}: atualizado para R$ {cotacao:.2f}")
                conexao.commit()
                continue

            # Demais ações
            dados = yf.Ticker(ticker)
            cotacao = dados.history(period="1d")['Close'].iloc[-1]
            
            #print("passou")
            cursor.execute("""
                UPDATE TB_ACOES SET VRATUAL = ?, DTATUALIZACAO = ?, VRTOTAL = QTDACOES*VRATUAL
                WHERE IDACOES = ?
            """, (cotacao, datetime.now(), id_acao))

            # Verifica último valor registrado para essa ação
            cursor.execute("""
                SELECT TOP 1 VRPRECO
                FROM TB_HIST_PRECO
                WHERE IDACOES = ?
                ORDER BY DTHORA DESC
            """, (id_acao,))
            ultimo = cursor.fetchone()
            
            # Só insere se for diferente ou se não houver histórico
            if not ultimo or float(ultimo[0]) != round(cotacao, 2):
                cursor.execute("""
                    INSERT INTO TB_HIST_PRECO (IDACOES, DTHORA, VRPRECO)
                    VALUES (?, ?, ?)
                """, (id_acao, datetime.now(), cotacao))

                #percentual_alerta = 0.02
                #limite_compra = 570.00 #vr_medio * (1 + percentual_alerta)

                if cotacao < vr_medio: #or cotacao < limite_compra                 
                    enviar_alerta_telegram(nome_acao, vr_medio, cotacao)

            #print(f"{nome_acao}: atualizado para R$ {cotacao:.2f}")
            conexao.commit()

        except Exception as e:
            print(f"Erro ao processar {nome_acao}: {e}")
            continue
            #print(f"Erro ao enviar alerta: {e}")           
            #conexao.close()
            #conexao.rollback()

    conexao.close()

# Executa a função
if __name__ == "__main__":
    atualizar_cotacoes()
