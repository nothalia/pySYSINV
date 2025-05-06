from flask import Flask, render_template, request, redirect, url_for
from models.acoes import listar_acoes, inserir_acao, buscar_acao_por_id, atualizar_acao, excluir_acao, calcular_total_vrtotal
from models.compras import buscar_hist_por_id, buscar_id_acao_por_hist, inserir_hist_compra, listar_hist_acoes, atualizar_hist_acao, excluir_hist_acao
import yfinance as yf


app = Flask(__name__)

@app.route('/')
def index():
    acoes = listar_acoes()
    total_vrtotal = calcular_total_vrtotal()
    return render_template('index.html', acoes=acoes, total_vrtotal=total_vrtotal)

@app.route('/nova', methods=['GET'])
def nova_acao():
    return render_template('form_acao.html', acao=None)

@app.route('/nova', methods=['POST'])
def criar_acao():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    vrmedio = request.form['vrmedio']
    vratual = request.form['vratual']
    flsa = request.form.get('flsa_acao', 'N') 

    inserir_acao(nome, quantidade, vrmedio, vratual, flsa)
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET'])
def editar_acao(id):
    acao = buscar_acao_por_id(id)
    return render_template('form_acao.html', acao=acao)

@app.route('/editar/<int:id>', methods=['POST'])
def salvar_acao(id):
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    vrmedio = request.form['vrmedio']
    vratual = request.form['vratual']
    flsa = request.form.get('flsa_acao', 'N') 

    atualizar_acao(id, nome, quantidade, vrmedio, vratual, flsa)
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    excluir_acao(id)
    return redirect(url_for('index'))

# -------- SIMULAÇÃO -------- #
@app.route('/nova_simulacao', methods=['GET', 'POST'])
def nova_simulacao():
    if request.method == 'POST':
        total_acoes = int(request.form['total_acoes'])
        resultados = []

        for i in range(total_acoes):
            nome = request.form.get(f'nome_{i}')
            preco = float(request.form.get(f'preco_{i}'))
            quantidade = int(request.form.get(f'quantidade_{i}'))
            total = preco * quantidade
            if quantidade > 0:
                resultados.append({'nome': nome, 'preco': preco, 'quantidade': quantidade, 'total': total})

        # Recupera novamente as ações do banco para exibir no formulário
        acoes = listar_acoes()  # você já deve ter essa função
        return render_template('form_simulacao.html', acoes=acoes, resultados=resultados)

    else:
        acoes = listar_acoes()
        return render_template('form_simulacao.html', acoes=acoes)



# -------- COMPRAS / HISTÓRICO -------- #
@app.route('/nova_hist', methods=['GET'])
def nova_hist_acao():
    acoes = listar_acoes()
    return render_template('form_hist_acao.html', id_acao=None, acoes=acoes)

@app.route('/nova_hist', methods=['POST'])
def criar_hist_acao():
    idacao = request.form['idacao']
    dtcompra = request.form['dtcompra']
    vrcompra = request.form['vrcompra']
    qtdcompra = request.form['qtdcompra']
    nmcorretora = request.form['nmcorretora']

    inserir_hist_compra(idacao, dtcompra, vrcompra, qtdcompra, nmcorretora)
    return redirect(url_for('ver_hist_acao', id_acao=idacao))

@app.route('/historico/<int:id_acao>')
def ver_hist_acao(id_acao):
    historico = listar_hist_acoes(id_acao)
    return render_template('historico.html', historico=historico, id_acao=id_acao)

@app.route('/editar_hist/<int:id>', methods=['GET'])
def editar_hist_acao(id):
    historico = buscar_hist_por_id(id)
    acoes = listar_acoes()  # <--- importante!
    return render_template('form_hist_acao.html', acaohist=historico, acoes=acoes)

@app.route('/editar_hist/<int:id>', methods=['POST'])
def salvar_hist_acao(id):
    idacao = request.form['idacao']
    dtcompra = request.form['dtcompra']
    vrcompra = request.form['vrcompra']
    qtdcompra = request.form['qtdcompra']
    nmcorretora = request.form['nmcorretora']

    atualizar_hist_acao(id, idacao, dtcompra, vrcompra, qtdcompra, nmcorretora)
    return redirect(url_for('ver_hist_acao', id_acao=idacao))

@app.route('/excluir_hist/<int:id>')
def excluir_hist(id):
    idacao = buscar_id_acao_por_hist(id)
    excluir_hist_acao(id)
    return redirect(url_for('ver_hist_acao', id_acao=idacao))


def buscar_cotacao_yahoo(ticker):
    acao = yf.Ticker(ticker)
    dados = acao.history(period="1d")
    if not dados.empty:
        return float(dados["Close"][0])
    return None

@app.route('/nova_compra/<int:id_acao>', methods=['GET', 'POST'])
def nova_compra(id_acao):
    acoes = listar_acoes()
    return render_template("form_hist_acao.html", acoes=acoes)




if __name__ == '__main__':
    app.run(debug=True)
