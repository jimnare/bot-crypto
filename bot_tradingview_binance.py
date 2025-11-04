from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *
import threading

# ============================================================
# CONFIGURACIÓN BINANCE
# ============================================================
import os
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


client = Client(API_KEY, API_SECRET)

# ============================================================
# CONFIGURACIÓN DEL SERVIDOR
# ============================================================
app = Flask(__name__)

# ============================================================
# FUNCIÓN DE EJECUCIÓN DE ORDEN
# ============================================================
def ejecutar_orden(symbol, side, cantidad):
    try:
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY if side == "BUY" else SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=cantidad
        )
        print(f"✅ Orden ejecutada: {side} {cantidad} {symbol}")
        return order
    except Exception as e:
        print(f"❌ Error al ejecutar la orden: {e}")
        return None

# ============================================================
# RUTA DEL WEBHOOK
# ============================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Señal recibida:", data)

    symbol = data.get("symbol", "PEPEUSDT")
    side = data.get("side", "").upper()
    cantidad = float(data.get("amount", 20))

    if side in ["BUY", "SELL"]:
        threading.Thread(target=ejecutar_orden, args=(symbol, side, cantidad)).start()
        return jsonify({"status": "ok", "message": f"Orden {side} ejecutada"})
    else:
        return jsonify({"status": "error", "message": "Acción inválida"}), 400

# ============================================================
# INICIO DEL SERVIDOR
# ============================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
