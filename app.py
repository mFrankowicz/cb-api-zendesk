from flask import Flask
from flask import jsonify
import requests
import datetime
app = Flask(__name__)

@app.route('/rastrear/<nf>')
def rastreio(nf):
    url = f"https://api.intelipost.com.br/api/v1/shipment_order/invoice/{nf}"

    payload = ""
    headers = {
        "Content-Type": "application/json",
        "api-key": "312a8fb1734ce968c4e2e3cf2c4a9ef6bd1efdac7d6fcde513acfdb99a4c2727"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    if response.status_code == '400':
        return "Não foi possível rastrear o pedido", 400, {'ContentType':'application/json'} 
    else:
        if len(response.json()['content']) == 0:
            return "Número da NF não encontrado"
        else:
            return(transformar(response.json()))

def transformar(data):
    content = data['content'][0]
    end_customer = content['end_customer']
    nome_cliente = end_customer['first_name'] + ' ' + end_customer['last_name']
    endereco_rua = end_customer['shipping_address']
    endereco_numero = end_customer['shipping_number']
    endereco_bairro = end_customer['shipping_quarter']
    endereco_cep = end_customer['shipping_zip_code']
    endereco_cidade = end_customer['shipping_city']
    endereco_estado = end_customer['shipping_state']

    data_prevista = content['estimated_delivery_date_iso']

    transportadora = content['logistic_provider_name']
    volumes_array = content['shipment_order_volume_array']

    volumes = volumes_array[0]['name']
    historico_array = volumes_array[0]['shipment_order_volume_state_history_array']
    historico = ""
    for e in historico_array:
        data_evento = e['created_iso']
        m = e['shipment_volume_micro_state']['shipment_volume_state_localized']
        parsed = datetime.datetime.fromisoformat(data_evento)
        historico += f"{parsed.strftime('%d/%m/%y %H:%M')} : {m}\n"

    m_data_prevista = f"Data Estimada de Entrega: {datetime.datetime.fromisoformat(data_prevista).strftime('%d/%m/%y')}"
    m_transportadora = f"Transportadora: {transportadora}"

    mensagem = {
        "cliente": nome_cliente,
        "endereco_entrega": endereco_estado + ', ' + endereco_cidade + '. CEP:' + endereco_cep,
        "data_prevista": m_data_prevista,
        "transportadora": m_transportadora,
        "historico": historico
    }
    return jsonify(mensagem)