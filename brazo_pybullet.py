import pybullet as p
import pybullet_data
import time
import socket

# ==========================================
# 1. CONFIGURACIÓN E INICIALIZACIÓN PYBULLET
# ==========================================
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("brazo.urdf", [0, 0, 0], useFixedBase=True)

num_joints = p.getNumJoints(robotId)
end_effector_index = num_joints - 1  # Último eslabón (punta del efector final)

# ==========================================
# 2. CONEXIÓN SOCKET CON EL PUENTE (OPCIONAL)
# ==========================================
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(0.1) # Modo no bloqueante
puente_conectado = False

try:
    client_socket.connect(('127.0.0.1', 4000))
    puente_conectado = True
    print("[SOCKET] Conectado exitosamente al puente local en puerto 4000.")
except:
    print("[SOCKET] No se detectó puente activo. Se usará control manual por teclado PC.")

# ==========================================
# 3. FUNCIONES DE MOVIMIENTO Y DIBUJO
# ==========================================
lineas_dibujadas = []

def mover_efector_a(target_pos, pasos=25):
    """Calcula la cinemática inversa y mueve las articulaciones del brazo."""
    joint_poses = p.calculateInverseKinematics(
        robotId, 
        end_effector_index, 
        target_pos
    )
    
    # Aplicar posiciones a cada articulación
    for i in range(min(num_joints, len(joint_poses))):
        p.setJointMotorControl2(
            bodyUniqueId=robotId,
            jointIndex=i,
            controlMode=p.POSITION_CONTROL,
            targetPosition=joint_poses[i],
            force=500
        )
    
    # Avanzar la simulación para suavizar el movimiento
    for _ in range(pasos):
        p.stepSimulation()
        time.sleep(1. / 240.)

def trazar_segmento(pos_inicio, pos_fin):
    """Mueve el brazo entre dos puntos y dibuja la línea roja en el aire."""
    mover_efector_a(pos_inicio)
    mover_efector_a(pos_fin)
    
    linea_id = p.addUserDebugLine(pos_inicio, pos_fin, lineColorRGB=[1, 0, 0], lineWidth=4)
    lineas_dibujadas.append(linea_id)

def limpiar_pantalla():
    """Borra todas las líneas del lienzo."""
    global lineas_dibujadas
    for l in lineas_dibujadas:
        p.removeUserDebugItem(l)
    lineas_dibujadas.clear()
    print("[RESET] Lienzo limpio.")

# ==========================================
# 4. RUTINAS DE DIBUJO (NÚMEROS 1, 2 Y 3)
# ==========================================
def dibujar_numero(numero):
    z = 0.35  # Altura base de dibujo
    
    if str(numero) == '1':
        print("\n[DIBUJANDO] Número 1...")
        # Gancho inicial (diagonal de subida)
        trazar_segmento([0.14, 0.0, z + 0.18], [0.18, 0.0, z + 0.25])
        # Trazo vertical descendente
        trazar_segmento([0.18, 0.0, z + 0.25], [0.18, 0.0, z])
        # Base horizontal
        trazar_segmento([0.12, 0.0, z], [0.24, 0.0, z])
        
    elif str(numero) == '2':
        print("\n[DIBUJANDO] Número 2...")
        trazar_segmento([0.10, 0.0, z + 0.25], [0.20, 0.0, z + 0.25])
        trazar_segmento([0.20, 0.0, z + 0.25], [0.20, 0.0, z + 0.12])
        trazar_segmento([0.20, 0.0, z + 0.12], [0.10, 0.0, z + 0.12])
        trazar_segmento([0.10, 0.0, z + 0.12], [0.10, 0.0, z])
        trazar_segmento([0.10, 0.0, z], [0.20, 0.0, z])

    elif str(numero) == '3':
        print("\n[DIBUJANDO] Número 3...")
        trazar_segmento([0.10, 0.0, z + 0.25], [0.20, 0.0, z + 0.25])
        trazar_segmento([0.20, 0.0, z + 0.25], [0.15, 0.0, z + 0.12])
        trazar_segmento([0.15, 0.0, z + 0.12], [0.20, 0.0, z + 0.12])
        trazar_segmento([0.20, 0.0, z + 0.12], [0.10, 0.0, z])

    elif str(numero).upper() in ['C', 'A']:
        limpiar_pantalla()

# ==========================================
# 5. BUCLE PRINCIPAL DE INTERACCIÓN
# ==========================================
print("\n" + "="*50)
print(" SISTEMA DE DIBUJO POR CINEMÁTICA INVERSA LISTO ")
print(" Controles activos en ventana PyBullet (Teclado PC):")
print("  - Tecla 1: Dibuja el '1'")
print("  - Tecla 2: Dibuja el '2'")
print("  - Tecla 3: Dibuja el '3'")
print("  - Tecla C: Limpiar borrador")
print("="*50 + "\n")

try:
    while True:
        p.stepSimulation()
        time.sleep(1. / 240.)

        # 1. Leer pulsaciones desde la ventana gráfica de PyBullet
        keys = p.getKeyboardEvents()
        for k, v in keys.items():
            if v & p.KEY_WAS_TRIGGERED:
                char_key = chr(k).upper() if 0 <= k < 256 else None
                if char_key:
                    dibujar_numero(char_key)

        # 2. Leer comandos del Socket (Si está conectado)
        if puente_conectado:
            try:
                data = client_socket.recv(1024)
                if data:
                    comando = data.decode('utf-8').strip()
                    print(f"[SOCKET DETECTADO]: {comando}")
                    dibujar_numero(comando)
            except socket.timeout:
                pass
            except:
                puente_conectado = False

except KeyboardInterrupt:
    if puente_conectado:
        client_socket.close()
    p.disconnect()