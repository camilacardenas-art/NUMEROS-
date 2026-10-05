# NUMEROS-
#ENLACE PARCIAL LATEX 

https://es.overleaf.com/read/cfhfrkhhgvtt#653b11

# 🤖 Sistema de Simulación Robótica y Control de Trazo en 3D

Este proyecto implementa un entorno de simulación robótica e interacción hardware-software integrando un **brazo robótico manipulador en PyBullet**, un **controlador empotrado ESP32** simulado en Wokwi, un **sistema de Visión por Computador (OpenCV)** y un **puente de comunicación asíncrono**. 

El objetivo principal es permitir que el brazo robótico dibuje patrones numéricos (`1`, `2` y `3`) y realice limpiezas de lienzo mediante algoritmos de **Cinemática Inversa (IK)** activados por hardware o procesamiento de imágenes.

---

## 📐 Arquitectura del Sistema

El proyecto se divide en 4 capas de funcionalidad:

1. **Hardware / Emulación (Wokwi & ESP32):** 
   - Un microcontrolador **ESP32 DevKit v4** escanea las pulsaciones en un **teclado matricial 4x4** (Filas: GPIO 13, 12, 14, 27 | Columnas: GPIO 26, 25, 33, 32).
   - Transmite los comandos del usuario vía socket/puerto serie a la estación de trabajo local.

2. **Puente de Comunicación (`puente_wokwi.py`):**
   - Servidor local en Python que gestiona el tráfico de datos en tiempo real entre la emulación web/física y el motor de físicas sin bloquear los hilos principales.

3. **Módulo opcional de Visión por Computador (`vision_control.py`):**
   - Procesamiento de imágenes mediante **OpenCV** usando la cámara web para reconocimiento de gestos / marcas, permitiendo la activación remota por visión artificial.

4. **Entorno de Simulación 3D (`brazo_pybullet.py`):**
   - Carga del modelo URDF (`brazo.urdf`).
   - Cálculo de trayectoria continua mediante `p.calculateInverseKinematics`.
   - Renderizado de trazos vectoriales en el espacio 3D (`p.addUserDebugLine`).

---

## 🚀 Guía de Instalación y Requisitos

### Requisitos Previos
* **Python 3.10+** (Probado en Python 3.14)
* Visual Studio Code o entorno similar
* Navegador Web (para Wokwi) o cámara web funcional

### Dependencias de Python
Instala los paquetes necesarios ejecutando en tu entorno virtual:

```bash
pip install pybullet numpy opencv-python pyserial
```
## 🛠️ Paso a Paso: Guía de Ejecución

### 1. Configuración y Carga en Wokwi
1. Accede a tu proyecto en Wokwi.
2. Copia el siguiente esquema en la pestaña `diagram.json` para asegurar el conexionado correcto de pines:
   ```json
   {
     "version": 1,
     "author": "ESP32 Keypad Integration",
     "editor": "wokwi",
     "parts": [
       { "type": "board-esp32-devkit-c-v4", "id": "esp", "top": -40, "left": 0, "attrs": {} },
       { "type": "wokwi-membrane-keypad", "id": "keypad", "top": -120, "left": 220, "attrs": {} }
     ],
     "connections": [
       [ "keypad:R1", "esp:13", "green", [ "v0" ] ],
       [ "keypad:R2", "esp:12", "green", [ "v0" ] ],
       [ "keypad:R3", "esp:14", "green", [ "v0" ] ],
       [ "keypad:R4", "esp:27", "green", [ "v0" ] ],
       [ "keypad:C1", "esp:26", "blue", [ "v0" ] ],
       [ "keypad:C2", "esp:25", "blue", [ "v0" ] ],
       [ "keypad:C3", "esp:33", "blue", [ "v0" ] ],
       [ "keypad:C4", "esp:32", "blue", [ "v0" ] ]
     ]
   }
   ```
   
