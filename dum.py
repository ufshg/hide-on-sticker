# cv.namedWindow("image", flags=cv.WINDOW_NORMAL)


#cv.imshow("image", img)


#resize_img = cv.resize(img, dsize=(500, 500), interpolation=cv.INTER_LINEAR)
#cv.imshow("imager", resize_img)

#key = cv.waitKey(0)
#cv.destroyAllWindows()

"""
영상에 적용
import cv2 as cv

face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_alt.xml"
)
eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_eye.xml")
cap = cv.VideoCapture("sample.mp4")
v = 20
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 10)
    for x, y, w, h in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)

        for ex, ey, ew, eh in eyes:
            cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    cv.imshow("frame", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv.destroyAllWindows()
"""
