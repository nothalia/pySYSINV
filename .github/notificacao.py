# notificacao.py
import requests

TELEGRAM_TOKEN = '7688585252:AAFMvBRNjFheSA9kpH2NIr0L3uscDuGJRMM'
TELEGRAM_CHAT_ID = '8195358198'

def enviar_alerta_telegram(codigo, valor_medio, preco_atual):
    mensagem = (
        f'📢 Atualização de Investimento\n'
        f'📌 Ação: {codigo}\n'
        f'💰 Valor de compra: R$ {valor_medio:.2f}\n'
        f'📉 Cotação atual: R$ {preco_atual:.2f}\n'
    )
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem}
    
    resposta = requests.post(url, data=data)
    if not resposta.ok:
        print('Erro ao enviar mensagem:', resposta.text)
