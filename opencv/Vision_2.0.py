import cv2
import numpy as np
import psycopg2
import time
from tkinter import Button, Tk, Label

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="Vision",
    user="vision",
    password="root",
    host="localhost"
)

# Función para almacenar la ruta de la captura en la base de datos
def almacenar_captura(ruta):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO capturas (ruta) VALUES (%s)", (ruta,))
    conn.commit()
    cursor.close()

# Función para realizar el reconocimiento facial
def reconocer_persona(imagen):
    # Realizar el reconocimiento facial aquí (puedes implementar tu lógica de reconocimiento)
    # En este ejemplo, simplemente devuelve un nombre ficticio
    return "Persona Desconocida"

# Función para tomar una captura
def tomar_captura():
    global captura_realizada
    captura_realizada = False

# Función para encender la cámara
def encender_camara():
    cap = cv2.VideoCapture(0)
    captura_realizada = False

    def captura_continua():
        nonlocal captura_realizada
        ret, frame = cap.read()  # Lee un fotograma de la cámara
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Realiza la detección de caras
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                if not captura_realizada:
                    # Realiza la captura solo si no se ha hecho una antes
                    nombre_archivo = r"C:\Users\Richard-P\Desktop\opencv\opencv\capturaia\rostro_{}.jpg".format(int(time.time()))
                    cv2.imwrite(nombre_archivo, frame)  # Almacenar el fotograma completo
                    almacenar_captura(nombre_archivo)
                    captura_realizada = True  # Establece el estado de captura realizada

                    # Realizar el reconocimiento facial en la nueva captura
                    nombre_persona = reconocer_persona(frame)
                    mensaje_captura.config(text="¡Captura realizada de {}!".format(nombre_persona))

            cv2.imshow('img', frame)

            # Presiona 'Esc' para salir
            k = cv2.waitKey(30)
            if k == 27:
                cap.release()
                cv2.destroyAllWindows()
            else:
                root.after(10, captura_continua)  # Llama a la función después de 10 milisegundos

    captura_continua()

# Configurar la interfaz gráfica
root = Tk()
root.title("Captura Facial")

# Botón para encender la cámara
boton_camara = Button(root, text="Camara", command=encender_camara)
boton_camara.pack(pady=20)

# Botón para tomar una captura
boton_captura = Button(root, text="Tomar Captura", command=tomar_captura)
boton_captura.pack()

# Etiqueta para mostrar el mensaje de captura
mensaje_captura = Label(root, text="")
mensaje_captura.pack()

# Cargar un clasificador preentrenado para la detección facial
face_cascade = cv2.CascadeClassifier('opencv/raw.githubusercontent.com_opencv_opencv_master_data_haarcascades_haarcascade_frontalface_default.xml')

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()
