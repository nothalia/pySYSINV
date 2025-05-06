from db.connection import conecta_banco

def inserir_acao(nome, qtd, vr_medio, vr_atual, flsa): ###AÇÕES !!! ###
    conexao = conecta_banco()
    cursor = conexao.execute("""
        INSERT INTO TB_ACOES (NMACOES, QTDACOES, VRMEDIO, VRATUAL, FLSA)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, qtd, vr_medio, vr_atual, flsa))
    conexao.commit()
    conexao.close()

def listar_acoes():
    conexao = conecta_banco()
    cursor = conexao.execute("SELECT * FROM TB_ACOES")
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def buscar_acao_por_id(id):
    conexao = conecta_banco()
    cursor = conexao.execute("SELECT * FROM TB_ACOES WHERE IDACOES = ?", id)
    acao = cursor.fetchone()
    conexao.close()
    return acao

def atualizar_acao(id, nome, quantidade, vrmedio, vratual, flsa):
    conexao = conecta_banco()
    cursor = conexao.execute("""
        UPDATE TB_ACOES
        SET NMACOES = ?, QTDACOES = ?, VRMEDIO = ?, VRATUAL = ?, FLSA = ?
        WHERE IDACOES = ?
    """, (nome, quantidade, vrmedio, vratual, flsa, id))
    conexao.commit()
    conexao.close()

def excluir_acao(id):
    conexao = conecta_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM TB_CMP_ACOES WHERE IDACOES = ?", id)
    cursor.execute("DELETE FROM TB_ACOES WHERE IDACOES = ?", id)

    conexao.commit()
    conexao.close()

def calcular_total_vrtotal():
    conexao = conecta_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT SUM(VRTOTAL) FROM TB_ACOES")
    total = cursor.fetchone()[0] or 0  # Garante que não retorne None
    conexao.close()
    return total
