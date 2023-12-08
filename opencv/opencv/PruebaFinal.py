import cv2
import mediapipe as mp
import math
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import threading
import psycopg2
from psycopg2 import sql

# Configuración de la base de datos
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'Vision'
DB_USER = 'vision'
DB_PASSWORD = 'root'

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

mpDibujo = mp.solutions.drawing_utils
ConfDibu = mpDibujo.DrawingSpec(thickness=1, circle_radius=1)

mpMallaFacial = mp.solutions.face_mesh
MallaFacial = mpMallaFacial.FaceMesh(max_num_faces=1)

texto = ""
captura_realizada = False  # Variable para controlar si ya se realizó una captura
nombre_persona = ""  # Variable para almacenar el nombre de la persona

# Conexión a la base de datos
conexion = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def crear_tabla_si_no_existe():
    with conexion.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS capturas (
                id SERIAL PRIMARY KEY,
                ruta VARCHAR(255) NOT NULL,
                emocion VARCHAR(50) NOT NULL,
                nombre_persona VARCHAR(255) NOT NULL
            )
        """)
    conexion.commit()

def guardar_captura_en_db(ruta, emocion, nombre_persona):
    with conexion.cursor() as cursor:
        cursor.execute(
            sql.SQL("INSERT INTO capturas (ruta, emocion, nombre_persona) VALUES (%s, %s, %s)"),
            (ruta, emocion, nombre_persona)
        )
    conexion.commit()

def guardar_resultado(frame):
    cv2.imwrite("reconocimiento_emociones.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    print("Resultado guardado como 'reconocimiento_emociones.png'")

def capturar_fotogramas():
    global texto
    global captura_realizada
    global nombre_persona

    nombre_persona = simpledialog.askstring("Nombre", "Ingrese el nombre de la persona:")

    while True:
        ret, frame = cap.read()
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = MallaFacial.process(frameRGB)

        px = []
        py = []
        lista = []

        if resultados.multi_face_landmarks:
            for rostros in resultados.multi_face_landmarks:
                for id, puntos in enumerate(rostros.landmark):
                    al, an, c = frame.shape
                    x, y = int(puntos.x * an), int(puntos.y * al)
                    px.append(x)
                    py.append(y)
                    lista.append([id, x, y])
                    if len(lista) == 468:
                        x1, y1 = lista[65][1:]
                        x2, y2 = lista[158][1:]
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        longitud1 = math.hypot(x2 - x1, y2 - y1)

                        x3, y3 = lista[295][1:]
                        x4, y4 = lista[385][1:]
                        cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                        longitud2 = math.hypot(x4 - x3, y4 - y3)

                        x5, y5 = lista[78][1:]
                        x6, y6 = lista[308][1:]
                        cx3, cy3 = (x5 + x6) // 2, (y5 + y6) // 2
                        longitud3 = math.hypot(x6 - x5, y6 - y5)

                        x7, y7 = lista[13][1:]
                        x8, y8 = lista[14][1:]
                        cx4, cy4 = (x7 + x8) // 2, (y7 + y8) // 2
                        longitud4 = math.hypot(x8 - x7, y8 - y7)

                        if longitud1 < 19 and longitud2 < 19 and longitud3 > 80 and longitud3 < 95 and longitud4 < 5:
                            texto = 'Persona Enojada'
                        elif 20 < longitud1 < 30 and 20 < longitud2 < 30 and 95 < longitud3 < 110 and 10 < longitud4 < 20:
                            texto = 'Persona Feliz'
                        elif 35 < longitud1 and 35 < longitud2 and 80 < longitud3 < 90 and longitud4 > 20:
                            texto = 'Persona Asombrada'
                        elif 25 < longitud1 < 35 and 25 < longitud2 < 35 and 90 < longitud3 < 95 and longitud4 < 5:
                            texto = 'Persona Triste'

                        cv2.rectangle(frame, (min(px), min(py)), (max(px), max(py)), (255, 0, 0), 2)
                        (text_width, text_height), baseline = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)
                        text_x = int((an - text_width) // 2)
                        text_y = int(al - 40)
                        cv2.putText(frame, texto, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        
                        cv2.putText(frame, f'Reconocimiento De Emociones', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        # Mostrar el nombre de la persona en la ventana
                        cv2.putText(frame, f'Nombre: {nombre_persona}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        # Guardar la captura si no se ha realizado antes
                        if texto and not captura_realizada:
                            nombre_captura = f"captura_{nombre_persona}.png"
                            cv2.imwrite(nombre_captura, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                            print(f"Captura de {nombre_persona} guardada como '{nombre_captura}'")
                            guardar_captura_en_db(nombre_captura, texto, nombre_persona)
                            captura_realizada = True

        cv2.imshow("Reconocimiento de Emociones", frame)
        t = cv2.waitKey(1)

        if t == 27:
            guardar_resultado(frame)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Reconocimiento de Emociones")

# Función para cerrar la aplicación
def cerrar_aplicacion():
    cap.release()
    cv2.destroyAllWindows()
    conexion.close()
    root.destroy()

# Crear el botón "Camara"
boton_camara = tk.Button(root, text="Camara", command=capturar_fotogramas)
boton_camara.pack(pady=10)

# Crear el botón "Cerrar"
boton_cerrar = tk.Button(root, text="Cerrar", command=cerrar_aplicacion)
boton_cerrar.pack(pady=10)

# Cre


# Crear la tabla en la base de datos si no existe
crear_tabla_si_no_existe()

root.mainloop()
