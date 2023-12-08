import cv2
import numpy as np
import psycopg2
import time
from tkinter import Button, Tk, Label
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="Vision",
    user="vision",
    password="root",
    host="localhost"
)

# Cargar un clasificador preentrenado para la detección facial
face_cascade = cv2.CascadeClassifier('opencv/raw.githubusercontent.com_opencv_opencv_master_data_haarcascades_haarcascade_frontalface_default.xml')

# Cargar el modelo preentrenado para el reconocimiento de emociones faciales
emotion_model = load_model('C:/Users/Richard-P/Desktop/opencv/opencv/model_v6_23.hdf5')
emotion_labels = ['Enojado', 'Disgusto', 'Miedo', 'Feliz', 'Triste', 'Sorpresa', 'Neutral']

# Variable global para indicar si se ha realizado una captura
captura_realizada = False

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

# Función para realizar el reconocimiento de emociones faciales
def reconocer_emocion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        roi_gray = roi_gray.astype('float') / 255.0
        roi_gray = img_to_array(roi_gray)
        roi_gray = np.expand_dims(roi_gray, axis=0)

        predictions = emotion_model.predict(roi_gray)[0]
        emotion_label = emotion_labels[np.argmax(predictions)]

        # Imprimir las predicciones y etiquetas en la consola
        print("Predicciones:", predictions)
        print("Emoción detectada:", emotion_label)

        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame


# Función para tomar una captura
def tomar_captura():
    global captura_realizada
    captura_realizada = False

# Función para encender la cámara
def encender_camara():
    cap = cv2.VideoCapture(0)
    global captura_realizada  # Agrega esta línea

    captura_realizada = False

    def captura_continua():
        global captura_realizada
        ret, frame = cap.read()
        if ret:
            # Realiza la detección de caras y emociones
            frame_con_emocion = reconocer_emocion(frame)

            # Muestra el resultado en la ventana
            cv2.imshow('img', frame_con_emocion)

            # Realiza la captura solo si no se ha hecho una antes
            if not captura_realizada:
                nombre_archivo = r"C:\Users\Richard-P\Desktop\opencv\opencv\capturaia\rostro_{}.jpg".format(int(time.time()))
                cv2.imwrite(nombre_archivo, frame)  # Almacenar el fotograma completo
                almacenar_captura(nombre_archivo)
                captura_realizada = True  # Establece el estado de captura realizada
                nombre_persona = reconocer_persona(frame)
                mensaje_captura.config(text="¡Captura realizada de {}!".format(nombre_persona))

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

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()
