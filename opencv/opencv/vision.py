import cv2
import psycopg2
import time

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

# Carga el clasificador Haarcascade para detección de caras
face_cascade = cv2.CascadeClassifier('opencv/raw.githubusercontent.com_opencv_opencv_master_data_haarcascades_haarcascade_frontalface_default.xml')

# Abre la cámara (cámara principal)
cap = cv2.VideoCapture(0)

captura_realizada = False  # Variable para rastrear si ya se hizo una captura

while True:
    ret, frame = cap.read()  # Lee un fotograma de la cámara
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Realiza la detección de caras
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        if not captura_realizada:  # Realiza la captura solo si no se ha hecho una antes
            nombre_archivo = "capturas/rostro_{}.jpg".format(int(time.time()))
            cv2.imwrite(nombre_archivo, frame)
            almacenar_captura(nombre_archivo)
            captura_realizada = True  # Establece el estado de captura realizada
    
    cv2.imshow('img', frame)
    
    # Presiona 'Esc' para salir
    k = cv2.waitKey(30)
    if k == 27:
        break

# Libera la cámara y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
conn.close()
