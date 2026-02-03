import websocket
import threading
import time

API_KEY = "0123456789"
WS_URL = "ws://localhost:8000/ws"

def on_message(ws, message):
    print("📩 Message reçu :", message)

def on_error(ws, error):
    print("❌ Erreur :", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket fermé")

def on_open(ws):
    print("✅ WebSocket connecté")

    # Thread keep-alive (optionnel mais recommandé)
    def keep_alive():
        while True:
            try:
                ws.send("ping")
                time.sleep(20)
            except:
                break

    threading.Thread(target=keep_alive, daemon=True).start()

ws = websocket.WebSocketApp(
    WS_URL,
    header=[f"X-API-Key: {API_KEY}"],
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open
)

# 🔁 Boucle infinie (reconnexion auto)
while True:
    ws.run_forever(ping_interval=30, ping_timeout=10)
    time.sleep(5)