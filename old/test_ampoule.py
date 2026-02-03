"""from yeelight import Bulb

bulb = Bulb("192.168.1.12")

props = bulb.get_properties()

print(props)"""

import socket
import json

msg = {
    "id": 1,
    "method": "get_prop",
    "params": ["power"]
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(("192.168.1.42", 55443))
s.send(json.dumps(msg).encode() + b"\r\n")

print(s.recv(1024).decode())
s.close()