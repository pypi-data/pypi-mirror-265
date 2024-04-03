import socket, time

for x in range(1000):
    try:
        ip = socket.gethostbyname("esx01.nordfluidinterno.lan")
        print(f"ok: {ip}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.3)

import socket, time

for x in range(1000):
    try:
        ip = socket.gethostbyname("syneto.eu")
        print(f"ok1: {ip}")
    except Exception as e:
        print(f"Error1: {e}")
    try:
        ip = socket.gethostbyname("esx01.nordfluidinterno.lan")
        print(f"ok2: {ip}")
    except Exception as e:
        print(f"Error2: {e}")
    time.sleep(0.3)
