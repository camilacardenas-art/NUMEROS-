import socket
import serial

# Configuración del servidor de puente
HOST = '127.0.0.1'
PORT = 4000

print(f"[PUENTE] Iniciando servidor en {HOST}:{PORT}...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("[PUENTE] Esperando conexión desde Wokwi o cliente...")
conn, addr = server_socket.accept()
print(f"[PUENTE] ¡Conectado desde {addr}!")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"[PUENTE REVOLT] Recibido: {data.decode('utf-8', errors='ignore')}")

conn.close()
