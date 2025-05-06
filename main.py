from db.connection import conecta_banco
from models.acoes import inserir_acao, listar_acoes

try:
    conexao, cursor = conecta_banco()
    print("✅ Conexão com banco de dados bem-sucedida! 🎉")

    # Aqui você pode executar comandos SQL, por exemplo:
    # cursor.execute("SELECT * FROM TB_ACOES")
    # for row in cursor.fetchall():
    #     print(row)

finally:
    # Fecha a conexão
    conexao.close()
    print("🔒 Conexão fechada.")

# Teste de inserção

# Teste de listagem
for acao in listar_acoes():
    print(acao)    