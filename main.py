import cv2 as cv
import numpy as np

# 마우스 이벤트에 사용할 변수
click = False
x1, y1 = -1, -1

# 사각형의 적용 여부를 관리할 dict
check = dict()

def show_rectangle(img, faces):
    temp = img.copy()
    for x, y, w, h in faces:
        if check[(x, y, w, h)]:
        #                                           B  G  R
            cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Draw X
            cv.line(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.line(temp, (x, y + h), (x + w, y), (0, 0, 255), 2)
        else:
            cv.rectangle(temp, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return temp

def click_rectangle(event, x, y, flags, param):
    global x1, y1, click

    if event == cv.EVENT_LBUTTONDOWN:
        click = True
        x1, y1 = x, y
    elif event == cv.EVENT_LBUTTONUP:
        click = False
        x1, y1 = x, y

        # x, y, w, h 인데 변수명이 겹침
        for a, b, w, h in check:
            if a <= x1 <= a + w and b <= y1 <= b + h:
                check[(a, b, w, h)] ^= True


def draw_rectangle(event, x, y, flags, param):
    global x1, y1, click

    if event == cv.EVENT_LBUTTONDOWN:
        click = True
        x1, y1 = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if click:
            pass

# 얼굴 검출기 초기화
face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + "haarcascade_frontalface_alt.xml"
)
eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_eye.xml")

# 이미지 불러오기
img = cv.imread("sample1.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.03, 5)

# 검출된 얼굴들을 활성 상태로 check에 추가
for x, y, w, h in faces:
    check[(x, y, w, h)] = False

cv.namedWindow('image')
cv.setMouseCallback('image', click_rectangle)

while True:
    cv.imshow('image', show_rectangle(img, faces))

    key = cv.waitKey(1) & 0xFF

    if key == 27:
        break

cv.destroyAllWindows()

while True:
    cv.imshow('image2', img)

    key = cv.waitKey(1) & 0xFF

    if key == 27:
        break
cv.destroyAllWindows()

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
