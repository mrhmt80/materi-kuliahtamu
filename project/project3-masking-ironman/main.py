#library yang dibutuhkan
import cv2
import mediapipe as mp

#definisi variabel landmark wajah dan ditambah filter mask
mpose = mp.solutions.pose
pose = mpose.Pose()

#proses ambil video
cap = cv2.VideoCapture(0)

#fungsi untuk menambahkan mask pada landmark wajah
def mask(frame, image, l_shoulder_x, l_shoulder_y):
    rol = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    rol = cv2.resize(rol, (600, 600), cv2.INTER_AREA)
    frame_h, frame_w, frame_c = frame.shape
    rol_h, rol_w, rol_c = rol.shape
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    for i in range(rol_h):
        for j in range(rol_w):
            if rol[i, j][3] != 0:
                if 0<=(l_shoulder_y - int(rol_h / 2)) + i < frame_h:
                        if 0<=(l_shoulder_x - int(rol_w / 2)) + j< frame_w:
                                frame[(l_shoulder_y - int(rol_h / 2)) + i, (l_shoulder_x - int(rol_w / 2)) + j] = rol[
                                    i, j]
    return frame

#proses stream

def stream():
    l_shoulder_x = 0
    l_shoulder_y = 0
    while True:
        suc, frame = cap.read()
        if suc:
        
            imcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            result = pose.process(imcolor)
            h, w = frame.shape[:2]
            lm = result.pose_landmarks
            if lm:
                #menyesuaikan landmark wajah dengan mask
                lm_pose = mpose.PoseLandmark
                l_shoulder_x = int(lm.landmark[lm_pose.NOSE].x * w)
                l_shoulder_y = int(lm.landmark[lm_pose.NOSE].y * h)
                #pilih gambar yang mau dijadikan topeng
                frame = mask(frame, 'ironman.png', l_shoulder_x, l_shoulder_y)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




if __name__=="__main__":
    stream()