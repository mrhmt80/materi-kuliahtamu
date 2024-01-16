#ambil library apa saja ?
import cv2
import mediapipe as mp

#proses capture Video
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
drawingUtils = mp.solutions.drawing_utils

#proses deteksi tangan
while (cap.isOpened()):
    s, img = cap.read()
    if not s:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    #jika sesuai maka memunculkan titik koordinat
    if result.multi_hand_landmarks:
        for h in result.multi_hand_landmarks:
            hh, w, c = img.shape
            X1, Y1 = int(h.landmark[4].x*w), int(h.landmark[4].y*hh)
            X2, Y2 = int(h.landmark[8].x*w), int(h.landmark[8].y*hh)

            cv2.circle(imgRGB, (X1,Y1), 14, (255,0,255), cv2.FILLED)
            cv2.circle(imgRGB, (X2,Y2), 14, (255,0,255), cv2.FILLED)
            cv2.line(imgRGB, (X1,Y1),(X2,Y2), (255,0,0), 4)

            drawingUtils.draw_landmarks(imgRGB, h, mpHands.HAND_CONNECTIONS)
    cv2.namedWindow("Hands", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hands", 640, 480)
    cv2.imshow("Hands",imgRGB)
    if cv2.waitKey(20) & 0xFF == 'q':
        break

#proses memunculkan pada jendela python
cap.release()
cv2.destroyAllWindows()
