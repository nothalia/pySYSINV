from db.connection import conecta_banco
from decimal import Decimal

def inserir_hist_compra(idacao, data, valor, quantidade, corretora):
    conexao = conecta_banco()

    cursor = conexao.execute("SELECT QTDACOES, VRMEDIO FROM TB_ACOES WHERE IDACOES = ?", (idacao,))

    atual = cursor.fetchone()
    qtd_atual, vrmedio_atual = atual
    quantidade = Decimal(quantidade)
    valor = Decimal(valor)

    # Novo valor médio
    nova_qtd = qtd_atual + (quantidade)
    novo_vrmedio = ((qtd_atual * vrmedio_atual) + ((quantidade) * (valor))) / nova_qtd  

    cursor = conexao.execute("""
        UPDATE TB_ACOES SET QTDACOES = ?, VRMEDIO = ? WHERE IDACOES = ?
    """, (nova_qtd, novo_vrmedio, idacao))  
    cursor = conexao.execute("""
        INSERT INTO TB_CMP_ACOES (IDACOES, DTCMP, VRCMP, QTDACOES, NMCORRETORA)
        VALUES (?, ?, ?, ?, ?)
    """, (idacao, data, valor, quantidade, corretora))
    conexao.commit()
    conexao.close()

def listar_hist_acoes(idacao):
    conexao = conecta_banco()
    cursor = conexao.execute("SELECT * FROM TB_CMP_ACOES WHERE IDACOES = ?", idacao)
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def atualizar_hist_acao(id, idacao, data, valor, quantidade, corretora):
    conexao = conecta_banco()
    cursor = conexao.execute("""
        UPDATE TB_CMP_ACOES
        SET IDACOES = ?, DTCMP= ?, VRCMP= ?,QTDACOES = ?, NMCORRETORA= ?
        WHERE IDCMPACOES = ?
    """, (idacao, data, valor, quantidade, corretora, id))
    conexao.commit()
    conexao.close()

def excluir_hist_acao(id_hist):
    conn = conecta_banco()
    cursor = conn.cursor()

    # Buscar o ID da ação associada à compra
    cursor.execute("SELECT IDACOES FROM TB_CMP_ACOES WHERE IDCMPACOES = ?", (id_hist,))
    idacao = cursor.fetchone()[0]

    # Excluir a compra
    cursor.execute("DELETE FROM TB_CMP_ACOES WHERE IDCMPACOES = ?", (id_hist,))

    # Buscar todas as compras restantes dessa ação
    cursor.execute("SELECT VRCMP, QTDACOES FROM TB_CMP_ACOES WHERE IDACOES = ?", (idacao,))
    compras = cursor.fetchall()

    if compras:
        total_qtd = sum([Decimal(c[1]) for c in compras])
        total_valor = sum([Decimal(c[0]) * Decimal(c[1]) for c in compras])
        novo_vrmedio = total_valor / total_qtd
    else:
        total_qtd = 0
        novo_vrmedio = 0

    # Atualizar a ação na TB_ACOES
    cursor.execute("""
        UPDATE TB_ACOES SET QTDACOES = ?, VRMEDIO = ? WHERE IDACOES = ?
    """, (total_qtd, novo_vrmedio, idacao))

    conn.commit()
    conn.close()

def atualizar_valor_acao(id, nome, quantidade, vrmedio, vratual):
    conexao = conecta_banco()
    cursor = conexao.execute("""
        UPDATE TB_ACOES
        SET NMACOES = ?, QTDACOES = ?, VRMEDIO = ?, VRATUAL = ?
        WHERE IDACOES = ?
    """, (nome, quantidade, vrmedio, vratual, id))
    conexao.commit()
    conexao.close()   

def buscar_hist_por_id(id):
    conexao = conecta_banco()
    cursor = conexao.execute("""SELECT A.IDCMPACOES
                            FROM TB_CMP_ACOES A, TB_ACOES B
                             WHERE A.IDACOES = B.IDACOES
                             AND IDCMPACOES = ?""", (id,))
    acao = cursor.fetchone()
    conexao.close()
    return acao

def buscar_id_acao_por_hist(id_hist):
    conexao = conecta_banco()
    cursor = conexao.execute("SELECT IDACOES FROM TB_CMP_ACOES WHERE IDCMPACOES = ?", (id_hist,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado[0] if resultado else None


