import socket
import time
import pybullet as p
import pybullet_data

# ==========================================
# 1. CONFIGURACIÓN DEL SOCKET (PUENTE LOCAL)
# ==========================================
HOST = '127.0.0.1'
PORT = 4000

client_socket = None
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.setblocking(False)  # Modo no bloqueante para no congelar la simulación
    print("[SOCKET] Conectado exitosamente al puente local en el puerto 4000.")
except Exception as e:
    print(f"[SOCKET] No se pudo conectar al puente local: {e}")
    print("[SOCKET] Se mantendrá activo el control directo desde el teclado del PC.")

# ==========================================
# 2. INICIALIZACIÓN DE PYBULLET
# ==========================================
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Cargar plano de fondo
planeId = p.loadURDF("plane.urdf")

# Cargar tu brazo robótico personalizado
armStartPos = [0, 0, 0]
armStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
robotId = p.loadURDF("brazo.urdf", armStartPos, armStartOrientation, useFixedBase=True)

num_joints = p.getNumJoints(robotId)
print(f"[PYBULLET] Robot 'brazo.urdf' cargado con {num_joints} articulaciones.")

# ==========================================
# 3. FUNCIONES DE DIBUJO Y RESET
# ==========================================
lineas_dibujadas = []

def dibujar_linea(p1, p2, color=[1, 0, 0], ancho=3):
    """ Dibuja un trazo persistente en el espacio 3D de PyBullet """
    linea_id = p.addUserDebugLine(p1, p2, lineColorRGB=color, lineWidth=ancho)
    lineas_dibujadas.append(linea_id)

def limpiar_tablero():
    """ Borra todos los trazos realizados en pantalla """
    global lineas_dibujadas
    for linea in lineas_dibujadas:
        p.removeUserDebugItem(linea)
    lineas_dibujadas.clear()
    print("\n[RESET] Tablero de dibujo limpiado.")

def ejecutar_patron_dibujo(tecla):
    """ Ejecuta el patrón gráfico según la tecla ingresada """
    tecla = str(tecla).upper().strip()
    print(f"\n[DIBUJANDO] Ejecutando patrón para la tecla: {tecla}")
    
    z = 0.5  # Altura de referencia en el espacio 3D

    if tecla == '1':
        print("Trazando número 1...")
        dibujar_linea([0.2, 0.0, z], [0.2, 0.0, z + 0.3], color=[1, 0, 0])
        dibujar_linea([0.15, 0.0, z + 0.25], [0.2, 0.0, z + 0.3], color=[1, 0, 0])

    elif tecla == '2':
        print("Trazando número 2...")
        dibujar_linea([0.1, 0.0, z + 0.3], [0.2, 0.0, z + 0.3], color=[0, 0, 1])
        dibujar_linea([0.2, 0.0, z + 0.3], [0.2, 0.0, z + 0.15], color=[0, 0, 1])
        dibujar_linea([0.2, 0.0, z + 0.15], [0.1, 0.0, z + 0.15], color=[0, 0, 1])
        dibujar_linea([0.1, 0.0, z + 0.15], [0.1, 0.0, z], color=[0, 0, 1])
        dibujar_linea([0.1, 0.0, z], [0.2, 0.0, z], color=[0, 0, 1])

    elif tecla == '3':
        print("Trazando número 3...")
        dibujar_linea([0.1, 0.0, z + 0.3], [0.2, 0.0, z + 0.3], color=[0, 1, 0])
        dibujar_linea([0.2, 0.0, z + 0.3], [0.2, 0.0, z + 0.15], color=[0, 1, 0])
        dibujar_linea([0.1, 0.0, z + 0.15], [0.2, 0.0, z + 0.15], color=[0, 1, 0])
        dibujar_linea([0.2, 0.0, z + 0.15], [0.2, 0.0, z], color=[0, 1, 0])
        dibujar_linea([0.1, 0.0, z], [0.2, 0.0, z], color=[0, 1, 0])

    elif tecla in ['C', 'A']:
        limpiar_tablero()

    else:
        print(f"Tecla '{tecla}' sin patrón asignado.")

# ==========================================
# 4. BUCLE PRINCIPAL
# ==========================================
print("\n" + "="*50)
print(" SISTEMA LISTO PARA DIBUJAR ")
print(" -> Teclas en PyBullet: 1, 2, 3 o C/A (Limpiar)")
print(" -> Escuchando comandos desde el puente de Wokwi...")
print("="*50 + "\n")

try:
    while True:
        p.stepSimulation()
        time.sleep(1. / 240.)

        # A) CAPTURA DE TECLAS DIRECTAS EN PYBULLET (TECLADO PC)
        keys = p.getKeyboardEvents()
        for k, v in keys.items():
            if v & p.KEY_WAS_TRIGGERED:
                char_key = chr(k).upper() if 0 <= k < 256 else None
                if char_key:
                    print(f"[Teclado PC] Presionado: {char_key}")
                    ejecutar_patron_dibujo(char_key)

        # B) LECTURA DE TECLAS DESDE EL SOCKET (WOKWI)
        if client_socket:
            try:
                data = client_socket.recv(1024)
                if data:
                    tecla_recibida = data.decode('utf-8').strip()
                    if tecla_recibida:
                        print(f"[Socket -> Wokwi] Tecla recibida: {tecla_recibida}")
                        ejecutar_patron_dibujo(tecla_recibida)
            except BlockingIOError:
                pass  # No hay nuevos datos en este ciclo

except KeyboardInterrupt:
    print("\n[SALIR] Simulación finalizada.")
    if client_socket:
        client_socket.close()
    p.disconnect()