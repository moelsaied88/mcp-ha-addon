import json
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HA_URL = os.environ.get("HA_URL", "")
HA_TOKEN = os.environ.get("HA_TOKEN", "")
EXPOSED = os.environ.get("EXPOSED", "").split(",")

def call_ha_service(domain, service, entity_id, data=None):
    url = f"{HA_URL}/api/services/{domain}/{service}"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"entity_id": entity_id}
    if data:
        payload.update(data)

    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.text

@app.route("/mcp/command", methods=["POST"])
def mcp_command():
    body = request.json
    action = body.get("action")
    entity = body.get("entity")
    data = body.get("data", {})

    if entity not in EXPOSED:
        return jsonify({"error": "Entity not exposed"}), 403

    domain, service = action.split(".")
    status, result = call_ha_service(domain, service, entity, data)

    return jsonify({"status": status, "result": result})

@app.route("/mcp/entities", methods=["GET"])
def get_entities():
    return jsonify({"entities": EXPOSED})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
