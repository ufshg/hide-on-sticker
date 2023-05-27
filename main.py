import cv2 as cv
import numpy as np
import math

# 마우스 이벤트에 사용할 변수
click = False
x1, y1 = -1, -1

# 사각형의 적용 여부를 관리할 dict
check = dict()

# 원본 이미지를 복사하여 가공한 후 결과를 반환
def show_rectangle1(img, faces):
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

# 1 단계에서 사각형을 클릭했을 때 처리하는 함수
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

# 얼굴 검출기 초기화
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt.xml")

# 이미지 불러오기
img = cv.imread("sample.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.03, 5)

# 검출된 얼굴들을 활성 상태로 check에 추가
for x, y, w, h in faces:
    check[(x, y, w, h)] = True


######################################################
# 1 단계 - 검출된 얼굴 중 지울 것들을 선택
cv.namedWindow('image',flags=cv.WINDOW_NORMAL)
cv.setMouseCallback('image', click_rectangle)

while True:
    cv.imshow('image', show_rectangle1(img, faces))

    key = cv.waitKey(1) & 0xFF

    if key == 13:
        break
    elif key == 27:
        exit(0)
cv.destroyAllWindows()

# 선택하지 않은 얼굴 제거
task = []

# 처음부터 순차로 탐색
for i in range(len(faces)):
    x, y, w, h = faces[i]

    if not check[(x, y, w, h)]:
        task.append(i)
        del check[(x, y, w, h)]

# 역순으로 끝에 있는 것부터 삭제
# 앞에서부터 지우면 인덱스 오류 예상
while task:
    i = task.pop()
    faces = np.delete(faces, i, axis=0)

######################################################

# 1단계 이후 직사각형을 보여줌
def show_rectangle2(img, faces, stack):
    temp = img.copy()
    for x, y, w, h in faces:
        cv.rectangle(temp, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    for x, y, w, h in stack:
        cv.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return temp

def Box(x, y, x1, y1):
    return min(x, x1), min(y, y1), abs(x - x1), abs(y - y1)

def draw_rectangle(event, x, y, flags, param):
    global x1, y1, click, faces, stack

    if event == cv.EVENT_LBUTTONDOWN:
        click = True
        x1, y1 = x, y
        box = Box(x, y, x1, y1)
        stack.append(box)
    elif event == cv.EVENT_MOUSEMOVE:
        if click:
            stack.pop()
            box = Box(x, y, x1, y1)
            stack.append(box)
    elif event == cv.EVENT_LBUTTONUP:
        click = False
        stack.pop()
        box = Box(x, y, x1, y1)
        stack.append(box)
        
    elif event == cv.EVENT_RBUTTONDOWN:
        print('hi')
        if stack:
            print(stack)
            stack.pop()

stack = []

# 2 단계 - 사용자 정의 사각형 그리기
cv.namedWindow('image',flags=cv.WINDOW_NORMAL)
cv.setMouseCallback('image', draw_rectangle)

# 원본 이미지는 변함 없음을 보여줌
while True:
    cv.imshow('image', show_rectangle2(img, faces, stack))

    key = cv.waitKey(1) & 0xFF

    if key == 13:
        break
    elif key == 27:
        exit(0)

cv.destroyAllWindows()

face_result = [(x, y, w, h) for (x, y, w, h) in faces] + stack

######################################################

# 삭제할 사각형 정보
# 각 원소는 순서대로 x, y, w, h 

print(len(face_result))
print(face_result)

# 3단계 - 선택한 영역에 블러처리 또는 스티커 붙이기
cv.namedWindow('image',flags=cv.WINDOW_NORMAL)

# 원본 이미지 해상도
image_height, image_width = img.shape[:2]

# 모자이크 크기 계산
mosaic_ratio = 0.05  # 모자이크 비율 (0.01 ~ 0.05 사이의 값을 사용)
mosaic_size = int(min(image_height, image_width) * mosaic_ratio)

def make_mosaic(img):
    temp = img.copy()
    for (x, y, w, h) in face_result:
         # 모자이크 크기 계산
        face_mosaic_size = int(min(w, h) * mosaic_ratio)

        # 선택된 영역 추출
        face_roi = temp[y:y+h, x:x+w]

        # 선택 영역 모자이크 처리
        mosaic = cv.resize(face_roi, (face_mosaic_size, face_mosaic_size), interpolation=cv.INTER_NEAREST)
        mosaic = cv.resize(mosaic, (w, h), interpolation=cv.INTER_NEAREST)
        
        # 원본 이미지에 모자이크 적용
        temp[y:y+h, x:x+w] = mosaic
    return temp

def show_result(img, key):
    if key == 48:
        return img
    elif key == 49:
        return make_mosaic(img)
    
key = 48
    
while True:
    cv.imshow('image',show_result(img, key))

    key = cv.waitKey(0) & 0xFF

    if key == 13: # s키, S키 : 편집한 이미지 저장
        cv.imwrite('edited'  + '.png',img)
        break
    elif key == 49:
        pass
    elif key == 50:
        pass
    elif key == 51:
        pass
    elif key == 52:
        pass
    elif key == 53:
        pass
    elif key == 54:
        pass
    elif key in (115, 83): # s키, S키 : 편집한 이미지 저장
        cv.imwrite('edited'  + '.png',img)
        break
    elif key == 27:
        exit(0)

cv.destroyAllWindows()