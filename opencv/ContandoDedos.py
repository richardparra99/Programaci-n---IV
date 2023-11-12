# import cv2
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands

# cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

# with mp_hands.Hands(
#   static_image_mode = False,
#   max_num_hands = 2,
#   min_detection_confidence = 0.5) as hands:
#   while True:
#     ret, frame  = cap.read()
#     if ret  == False:
#       break
#     height,width, _ = frame.shape
#     frame = cv2.flip(frame,1)
#     frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#     results = hands.process(frame_rgb)
    
#     if results.multi_hand_landmarks is not None:
#       for hand_landmarks in results.multi_hand_landmarks:
#         mp_drawing.draw_landmarks(
#           frame,hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
#     cv2.imshow("Frame",frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#       break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
    
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        dedos_levantados = 0
        
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                dedos = []
                
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    dedos.append(cy)
                
                if dedos[8] < dedos[6]:
                    dedos_levantados += 1
                if dedos[12] < dedos[10]:
                    dedos_levantados += 1
                if dedos[16] < dedos[14]:
                    dedos_levantados += 1
                if dedos[20] < dedos[18]:
                    dedos_levantados += 1
        
        cv2.putText(frame, f"Dedos Levantados: {dedos_levantados}", (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()


