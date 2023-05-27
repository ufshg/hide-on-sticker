# Hide on Sticker

## 팀원

| 학과         | 학번     | 이름   |
| ------------ | -------- | ------ |
| 컴퓨터공학과 | 18101229 | 신현규 |
| 컴퓨터공학과 | 18101281 | 최해솔 |

## 프로젝트 설명

스마트폰이 보급됨에 따라 많은 사람들이 전보다 손쉽게 인터넷을 통해 자신의 일상을 공유하게 되었습니다.

특히 스마트폰으로 사진을 찍어 공유하는 것은 흔히 볼수있는 광경입니다.

하지만 무분별하게 공유하는 경우 초상권 침해등의 문제가 생길 수 있습니다.

따라서 인터넷에 사진을 올리는 경우, 편집을 통해 모르는 사람들을 가리고 올리는 편이 안전합니다.

저희 팀은 이미지 편집에 익숙하지 않은 일반인이 쉽게 사용할 수 있는 툴을 개발하였습니다.

Hide on Sticker는 사진에 등장하는 인물들의 얼굴을 감지하여 모자이크 처리를 하거나, 아기자기한 스티커로 덮어줄 것입니다.

*(본 프로젝트의 얼굴 인식 구현에는 OpenCV Haar Cascades가 사용되었습니다.)*

## 프로젝트 실행 방법

- 아래와 같이 필요한 패키지를 설치합니다.
```
pip install opencv-python opencv-contrib-python
pip install numpy
```
- 환경이 준비되었다면, **[resource](https://github.com/ufshg/hide-on-sticker/tree/main/resource)** 폴더 안에 원하는 이미지를 넣습니다. **(파일명 - resource.png)**
- 프로그램 조작법은 아래와 같습니다. (모든 작업 단계에서 esc키를 눌러 즉시 프로그램을 종료할 수 있습니다.)

  ### [1단계](#step1) - 가리고 싶지 않은 얼굴 제외 <a id="back1"></a>
    - 원하는 이미지를 넣고 프로그램을 실행하면 얼굴로 인식된 영역에 **빨간 박스**가 그려져있습니다.
    
    - 가리고싶지 않은 얼굴 영역을 클릭하면 **파란 박스**로 바뀌며, 처리 대상에서 제외됩니다. (파란 박스를 다시 클릭하여 처리 대상에 포함시킬 수 있습니다.)
    
    - 제외할 영역을 모두 선택했다면 `Enter`키를 눌러 다음 단계를 진행합니다.
  ### [2단계](#step2) - 처리가 필요한 영역 추가 선택 <a id="back2"></a>
    - 얼굴 인식이 제대로 되지 않았거나 추가로 가리고 싶은 영역을 직접 선택할 수 있습니다.
    
    - 마우스로 드래그하여 원하는 영역에 적절한 크기의 사각형을 그립니다.
    
    - 잘못 그려진 사각형은 마우스 우클릭으로 취소할 수 있습니다. (가장 최근에 그려진 사각형부터 취소됩니다.)
    
    - 영역 선택 완료 후 `Enter`키를 눌러 다음 단계로 넘어갑니다.
  ### [3단계](#step3) - 선택한 영역 가림 처리 <a id="back3"></a>
    - 키보드 조작으로 사용자가 선택한 영역에 대하여 가림 처리를 진행합니다.
    - **[sticker](https://github.com/ufshg/hide-on-sticker/tree/main/sticker)** 폴더 안에 원하는 png 이미지를 넣어 적용할 스티커로 사용할 수 있습니다.
    - 1.png 부터 7.png 까지의 스티커는 숫자키 `2`~`8` 로 선택하여 일괄 적용이 가능합니다.
    
      | 키         | 기능     | 
      | ------------ | -------- | 
      | 숫자키 `0` | 원본으로 되돌리기 | 
      | 숫자키 `1` | 모자이크 처리 | 
      | 숫자키 `2`~`8` | 스티커 1 ~ 7번 일괄 적용 | 
      | 숫자키 `9` | sticker 폴더 내 모든 스티커 랜덤 적용 | 
      | `s`, `S` | 현재 이미지 저장 |
      | `Enter` | 현재 이미지 저장 후 프로그램 종료 | 
      | `ESC` | 이미지를 저장하지 않고 즉시 프로그램 종료 | 
</br>

## 프로젝트 실행 결과 예시

  ### [1단계](#back1) - 가리고 싶지 않은 얼굴 제외 <a id="step1"></a>
  
  - 얼굴이 인식된 영역 표시
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/15118e92-c1c1-4d4d-8680-af283ab3604c" width="620" height="420"/>
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/a62dd456-856f-4d9d-bfa8-2fcc58c8581f" width="620" height="420"/>
  
  <br/>
  <br/>
  
  - 제외할 영역 선택 (각각 선택 O, X의 경우)
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/68f5fabf-ab77-4e1c-b6fa-9206d6e5d8fa" width="620" height="420"/>
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/a62dd456-856f-4d9d-bfa8-2fcc58c8581f" width="620" height="420"/>
  
  <br/>
  <br/>
    
  ### [2단계](#back2) - 처리가 필요한 영역 추가 선택 <a id="step2"></a>
  
  - 추가로 처리하고 싶은 영역 선택 (각각 추가 선택 O, X의 경우)
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/45a05280-8c74-4159-b787-445f47b1c210" width="620" height="420"/>
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/50cb71e6-266c-491c-be73-ec363b878cae" width="620" height="420"/>
  
  <br/>
  <br/>
    
  ### [3단계](#back3) - 선택한 영역 가림 처리 <a id="step3"></a>
  
  - 모자이크 처리
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/46f0fad9-0593-4bda-8a47-1e889888b07e" width="620" height="420"/>
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/5eabaf8c-7153-4099-9f8a-99b4c710e411" width="620" height="420"/>
  
  <br/>
  <br/>
  
  - 스티커 랜덤 적용
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/d88cb45a-8a41-41c2-ae06-6bad41dd99dd" width="620" height="420"/>
  <img src="https://github.com/ufshg/hide-on-sticker/assets/81071456/0b4c5d79-adac-4fc4-8f27-80422526275b" width="620" height="420"/>
  
  
  #### [프로젝트 데모 영상](https://www.youtube.com/watch?v=BDetAVbNI70)

## 참조

프로젝트를 개발하면서 코드 일부 인용 및 참고한 사이트 목록 입니다.

- [[Practice]스노우 앱처럼 얼굴에 스티커 붙이기](https://hazel-developer.tistory.com/103)
```
png 파일을 스티커처럼 선택 영역 위에 덮어씌우는 코드 일부 인용
```
- [[OpenCV] Python으로 Mouse Event, 드래그로 사각형 그리기](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=rhrkdfus&logNo=221612919440)
```
드래그 Mouse Event로 선택하고 싶은 영역 위에 사각형을 그리는 코드 참고
```
- 그 외 도움 - [chatGPT](https://openai.com/blog/chatgpt)
