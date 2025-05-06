import pyodbc

def conecta_banco(driver='ODBC Driver 17 for SQL Server', server='LAPTOP-LTHN7L5I\MSSQLSERVER01',
                  database='natFinancas', username='naths', password='123456'):
    
    string_conexao = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    conexao = pyodbc.connect(string_conexao)
    #cursor = conexao.cursor()
    return conexao
    #, cursor

# Teste
conexao = conecta_banco()
print("Conexão realizada com sucesso!")
