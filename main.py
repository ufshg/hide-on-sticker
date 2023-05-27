import cv2 as cv
import numpy as np
import os
import random as r

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
    elif event == cv.EVENT_LBUTTONUP:
        if click:
            click = False

            # x, y, w, h 인데 변수명이 겹침
            for a, b, w, h in check:
                if a <= x <= a + w and b <= y <= b + h:
                    check[(a, b, w, h)] ^= True

# 얼굴 검출기 초기화
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt.xml")

# 이미지 불러오기
img = cv.imread("resource/resource.png")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.03, 5)

# 검출된 얼굴들을 활성 상태로 check에 추가
for x, y, w, h in faces:
    check[(x, y, w, h)] = True


######################################################
# 1 단계 - 검출된 얼굴 중 지울 것들을 선택
cv.namedWindow('hide on sticker',flags=cv.WINDOW_NORMAL)
cv.setMouseCallback('hide on sticker', click_rectangle)

while True:
    cv.imshow('hide on sticker', show_rectangle1(img, faces))

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
            stack[-1] = Box(x, y, x1, y1)
    elif event == cv.EVENT_LBUTTONUP:
        click = False
        stack.pop()
        box = Box(x, y, x1, y1)
        stack.append(box)
        
    elif event == cv.EVENT_RBUTTONDOWN:
        if stack:
            stack.pop()

stack = []

# 2 단계 - 사용자 정의 사각형 그리기
cv.namedWindow('hide on sticker',flags=cv.WINDOW_NORMAL)
cv.setMouseCallback('hide on sticker', draw_rectangle)

# 원본 이미지는 변함 없음을 보여줌
while True:
    cv.imshow('hide on sticker', show_rectangle2(img, faces, stack))

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

#print(len(face_result))
#print(face_result)

# 3단계 - 선택한 영역에 블러처리 또는 스티커 붙이기
cv.namedWindow('hide on sticker',flags=cv.WINDOW_NORMAL)

# 원본 이미지 해상도
image_height, image_width = img.shape[:2]

# 이미지 해상도에 따라 가변 비율 적용
threshold = (min(image_height, image_width) // 100) * 0.01

# 모자이크 크기 계산
mosaic_ratio = max(0.025, 0.15 - threshold)  # 모자이크 비율 (0.01 ~ 0.05 사이의 값을 사용)
mosaic_size = int(min(image_height, image_width) * mosaic_ratio)

# 모자이크 처리 함수
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

def put_sticker(img, sticker = None, rand = False):
    temp = img.copy()

    if not rand:
        for (x, y, w, h) in face_result:
            x -= 8
            y -= 8
            w += 16
            h += 16
            
            # 영역 범위 밖 예외처리
            try:
                # 얼굴 인식된 영역 크기에 맞게 스티커 크기 조절
                resized_sticker = cv.resize(sticker, (w, h))

                # 스티커 합성
                overlay_alpha = resized_sticker[:, :, 3:4] / 255.0
                background_alpha = 1.0 - overlay_alpha

                # 스티커를 기존 이미지에 덧씌우기
                temp[y:y+h, x:x+w] = overlay_alpha * resized_sticker[:, :, :3] + background_alpha * temp[y:y+h, x:x+w]
            except:
                pass
            
        return temp
    else:
        for (x, y, w, h) in face_result:
            sticker = cv.imread(path_s + f'/{r.randint(1, sticker_len)}.png', cv.IMREAD_UNCHANGED)

            x -= 8
            y -= 8
            w += 16
            h += 16
            
            # 영역 범위 밖 예외처리
            try:
                # 얼굴 인식된 영역 크기에 맞게 스티커 크기 조절
                resized_sticker = cv.resize(sticker, (w, h))

                # 스티커 합성
                overlay_alpha = resized_sticker[:, :, 3:4] / 255.0
                background_alpha = 1.0 - overlay_alpha

                # 스티커를 기존 이미지에 덧씌우기
                temp[y:y+h, x:x+w] = overlay_alpha * resized_sticker[:, :, :3] + background_alpha * temp[y:y+h, x:x+w]
            except:
                pass
            
        return temp


def show_result(img, key):
    if key == 48: # 숫자키 0 -> 원본 복구
        return img
    elif key == 49: # 숫자키 1 -> 모자이크
        return make_mosaic(img)
    elif 50 <= key <= 56:
        sticker = cv.imread(f'./sticker/{key - 49}.png', cv.IMREAD_UNCHANGED)
        return put_sticker(img=img, sticker=sticker)
    elif key == 57:
        return put_sticker(img=img, rand=True)

    #elif key == 57: 
        # 숫자키 9 -> 모든 스티커 랜덤 적용
     #   pass

key_index = 49
key = 49

# 스티커 파일의 경로
path_s = "./sticker"
# 스티커 파일 개수
sticker_len = len(os.listdir(path_s))

# 결과 파일 저장 경로
path_r = './result/'
files = os.listdir(path_r)
result_list = [file for file in files if file.endswith('.png')]

if result_list:
    result_index = len(result_list) + 1
else:
    result_index = 1

temp_saved = None
    
while True:
    if not temp_saved is None:
        cv.imshow('hide on sticker', temp_saved)
        temp_saved = None
    else:
        temp = show_result(img, key_index)
        cv.imshow('hide on sticker', temp)

    key = cv.waitKey(0) & 0xFF

    if 48 <= key <= 57:
        key_index = key

    if key == 13: # enter : 편집한 이미지 저장 후 종료
        cv.imwrite(path_r  + str(result_index).zfill(3) + '.png', temp)
        break
    elif key in (115, 83): # s키, S키 : 편집한 이미지 저장
        cv.imwrite(path_r  + str(result_index).zfill(3) + '.png', temp)
        result_index += 1
        temp_saved = temp
    elif key == 27:
        exit(0)

cv.destroyAllWindows()