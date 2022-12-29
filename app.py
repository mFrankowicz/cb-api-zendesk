from flask import Flask
import requests
app = Flask(__name__)

@app.route('/rastreio/<nf>')
def hello_world(nf):
    url = f"https://api.intelipost.com.br/api/v1/shipment_order/invoice/{nf}"

    payload = ""
    headers = {
        "Content-Type": "application/json",
        "api-key": "312a8fb1734ce968c4e2e3cf2c4a9ef6bd1efdac7d6fcde513acfdb99a4c2727"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    return response.text
