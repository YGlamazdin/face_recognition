import cv2
import datetime

cap = cv2.VideoCapture(0)

CAMERA_WIDTH = 640*2
CAMERA_HEIGHT = 480*2


cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
# self.out = cv2.VideoWriter('output.mp4', -1, 20.0, (640, 480))

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

count_face=0
buff = []
while True:
    try:
        ret, frame = cap.read()

        # cv2.imwrite('/home/pi/robot/1.jpg', frame)
        # img2 = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)

        # cv2.imwrite('1.jpg', img2)

        if count_face < 0:
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_image, 1.45, 5)
            for (x, y, w, h) in faces:
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if w < 70:
                    continue
                for b in buff:
                    out.write(b)
                buff = []
                count_face = 20
                print("face", w, datetime.datetime.now())

        # cv2.imwrite('1.jpg', frame)

        count_face -= 1
        buff.append(frame)

        if count_face > 0:
            out.write(frame)

        if len(buff) > 10:
            buff.pop(0)

    except:
        print("frame error")
