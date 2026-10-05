import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Variable global para guardar la última tecla recibida
ultima_tecla = None
clientes_socket = []

# Servidor Socket para PyBullet
def iniciar_servidor_pybullet():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 4000))
    server.listen(5)
    print("[PUENTE] Servidor Socket listo para PyBullet en puerto 4000.")
    
    while True:
        client, addr = server.accept()
        print(f"[PUENTE] PyBullet conectado desde {addr}")
        clientes_socket.append(client)

# Servidor HTTP para recibir peticiones de Wokwi / Web
class WokwiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global ultima_tecla
        # Extraer la tecla enviada por la URL (ej: http://localhost:8080/?key=1)
        if '?key=' in self.path:
            tecla = self.path.split('?key=')[1].split('&')[0]
            print(f"\n[PUENTE DETECTÓ DESDE WOKWI]: Tecla {tecla}")
            
            # Reenviar a PyBullet
            for cliente in clientes_socket:
                try:
                    cliente.send((tecla + '\n').encode('utf-8'))
                except:
                    pass
                    
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return  # Ocultar logs molestos de HTTP

# Iniciar hilo de socket para PyBullet
t = threading.Thread(target=iniciar_servidor_pybullet, daemon=True)
t.start()

# Iniciar servidor HTTP en puerto 8080
httpd = HTTPServer(('127.0.0.1', 8080), WokwiHandler)
print("[PUENTE] Escuchando eventos web en http://127.0.0.1:8080...")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[PUENTE] Servidor cerrado.")
