from flask import Flask, request, jsonify

app = Flask(__name__)

# Tokens fixos (você pode mudar)
TOKEN_ADM = "ADM_123abc"
TOKEN_USER = "USER_456xyz"

# Trade inicial
trade = {
    "adm": {"dado": None, "confirm": False},
    "user": {"dado": None, "confirm": False},
    "status": "pendente"
}

# Função para gerar fake
def gerar_fake(dado):
    return "FAKE_" + dado[::-1]  # inverte o texto + prefixo FAKE

# Endpoint para validar token
@app.route("/validar-token", methods=["POST"])
def validar_token():
    token = request.json.get("token")
    if token == TOKEN_ADM:
        return jsonify({"status": "ok", "tipo": "ADM"})
    elif token == TOKEN_USER:
        return jsonify({"status": "ok", "tipo": "USER"})
    else:
        return jsonify({"status": "erro", "mensagem": "Token inválido"}), 403

# Endpoint para enviar dados
@app.route("/enviar-dados", methods=["POST"])
def enviar_dados():
    token = request.json.get("token")
    dado = request.json.get("dado")
    
    if token == TOKEN_ADM:
        trade["adm"]["dado"] = gerar_fake(dado)
    elif token == TOKEN_USER:
        trade["user"]["dado"] = dado
    else:
        return jsonify({"status": "erro", "mensagem": "Token inválido"}), 403

    return jsonify({"status": "ok", "trade": trade})

# Endpoint para confirmar trade
@app.route("/confirmar-trade", methods=["POST"])
def confirmar_trade():
    token = request.json.get("token")
    
    if token == TOKEN_ADM:
        trade["adm"]["confirm"] = True
    elif token == TOKEN_USER:
        trade["user"]["confirm"] = True
    else:
        return jsonify({"status": "erro", "mensagem": "Token inválido"}), 403
    
    if trade["adm"]["confirm"] and trade["user"]["confirm"]:
        trade["status"] = "finalizado"

    return jsonify({"status": trade["status"]})

# Endpoint para ver status da trade
@app.route("/status-trade", methods=["POST"])
def status_trade():
    token = request.json.get("token")

    if trade["status"] != "finalizado":
        return jsonify({"status": trade["status"]})

    if token == TOKEN_ADM:
        return jsonify({"seu": trade["adm"]["dado"], "outro": trade["user"]["dado"]})
    elif token == TOKEN_USER:
        return jsonify({"seu": trade["user"]["dado"], "outro": trade["adm"]["dado"]})
    else:
        return jsonify({"status": "erro", "mensagem": "Token inválido"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
