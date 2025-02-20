# Python 게임 모음
[English](../README.md) | [中文](README-cn.md) | [日本語](README-ja.md) | 한국어 | [Français](README-fr.md) | [فارسی](README-fa.md)

Pygame으로 제작된 고전 아케이드 및 퍼즐 게임 모음입니다. 벽돌 깨기, 뱀, 팩맨, 테트리스, 퐁, 오목, 2048 등 7가지의 재미있는 게임을 포함하고 있습니다. 부드러운 메뉴 전환, 게임패드 지원, 현대적인 UI 디자인을 구현했습니다. 게임 개발 학습과 엔터테인먼트에 최적화되어 있습니다.

## 빠른 시작

### 시스템 요구사항

- Python 3.8 이상
- Pygame 2.0 이상
- requirements.txt에 명시된 기타 의존성

### 설치

1. Python 3.8 이상이 설치되어 있는지 확인
2. 필요한 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

### 게임 실행

```bash
# 게임 메뉴 실행
python main.py
```

## 게임 목록

1. **벽돌 깨기**
   - 고전적인 벽돌 깨기 게임
   - 다양한 색상의 벽돌과 점수 시스템
   - 각도 기반 공 반사 메커니즘

2. **뱀**
   - 고전 뱀 게임의 현대적 해석
   - 부드러운 조작과 충돌 감지
   - 점수 추적과 단계별 난이도

3. **팩맨**
   - 단순화된 팩맨 스타일 게임
   - 다양한 색상의 적
   - 점수를 위한 도트 수집

4. **테트리스**
   - 고전적인 블록 쌓기 퍼즐 게임
   - 다양한 블록 모양
   - 라인 제거 메커니즘

5. **퐁**
   - 2인용 대전 퐁 게임
   - 각도 기반 공 물리
   - 5점 선취 승리

6. **오목**
   - 전통적인 오목 게임
   - 간단하고 직관적인 조작
   - 승리 조건: 5개의 돌을 일렬로 배치

7. **2048**
   - 인기 있는 퍼즐 게임
   - 타일을 합쳐 2048 달성
   - 최고 점수 도전

## 프로젝트 구조

```
.
├── main.py          # 메인 프로그램 진입점
├── games/           # 게임 모듈 디렉토리
│   ├── __init__.py
│   ├── breakout.py  # 벽돌 깨기 게임
│   ├── snake.py     # 뱀 게임
│   ├── pacman.py    # 팩맨 게임
│   ├── tetris.py    # 테트리스 게임
│   ├── pong.py      # 퐁 게임
│   ├── gomoku.py    # 오목 게임
│   └── game2048.py  # 2048 게임
├── requirements.txt  # 프로젝트 의존성
├── build.py         # 빌드 스크립트
└── resources/       # 리소스 파일
    └── icon.ico     # 애플리케이션 아이콘
```

## 조작 방법

### 키보드 조작
- 방향키: 메뉴 이동 및 게임 조작
- Enter: 메뉴 항목 선택
- ESC: 게임 일시정지/메뉴로 돌아가기
- R: 게임 재시작
- I: 설명 표시/숨기기

### 게임패드 조작
- 왼쪽 스틱/방향패드: 메뉴 이동 및 게임 조작
- A 버튼: 선택/확인
- B 버튼: 뒤로가기/취소
- 시작 버튼: 게임 일시정지
- X/Y 버튼: 게임별 추가 조작

### 게임별 조작 방법

#### 벽돌 깨기
- 좌우 방향키: 패들 이동
- 게임패드: 왼쪽 스틱 또는 방향패드로 패들 이동

#### 뱀
- 방향키: 방향 전환
- 게임패드: 왼쪽 스틱 또는 방향패드로 이동

#### 팩맨
- 방향키: 캐릭터 이동
- 게임패드: 왼쪽 스틱 또는 방향패드로 이동

#### 테트리스
- 좌우: 블록 이동
- 위: 블록 회전
- 아래: 낙하 속도 증가
- 스페이스: 즉시 낙하
- 게임패드: 왼쪽 스틱/방향패드로 이동, A 버튼으로 회전

#### 퐁
- 플레이어 1: W/S 키
- 플레이어 2: 위/아래 방향키
- 게임패드 1: 왼쪽 스틱으로 왼쪽 패들 조작
- 게임패드 2: 왼쪽 스틱으로 오른쪽 패들 조작

#### 오목
- 마우스: 돌 놓기
- 게임패드: 왼쪽 스틱/방향패드로 커서 이동, A 버튼으로 돌 놓기

#### 2048
- 방향키: 타일 이동
- 게임패드: 왼쪽 스틱/방향패드로 타일 이동

## 기능

- 부드러운 메뉴 전환 및 크기 조절 애니메이션
- 완벽한 게임패드 지원
- 각 게임의 튜토리얼 시스템
- 저장/종료 옵션이 있는 일시정지 메뉴
- 단계별 게임 난이도
- 점수 추적 시스템
- 현대적인 UI와 시각적 피드백

## 배포용 빌드

이 프로젝트는 PyInstaller를 사용하여 독립 실행 파일로 패키징할 수 있습니다.

### 빌드 단계

1. PyInstaller 설치:
   ```bash
   pip install pyinstaller
   ```

2. 빌드 명령 실행:
   ```bash
   # Windows
   pyinstaller build.py --onefile --noconsole --icon=icon.ico --name="GameCollection"
   ```

3. 실행 파일은 `dist` 디렉토리에 생성됩니다

## 개발 가이드
### 새로운 게임 추가

새로운 게임을 추가하려면 다음 단계를 따르세요:

1. 새로운 Python 파일 생성
2. 다음 필수 메서드를 포함하는 Game 클래스 구현:
   - `__init__()`: 게임 상태 초기화
   - `run()`: 메인 게임 루프
   - `handle_input()`: 사용자 입력 처리
   - `update()`: 게임 상태 업데이트
   - `draw()`: 그래픽 렌더링
3. `main.py`에 게임 정보 추가

## 라이선스

이 프로젝트는 MIT 라이선스로 제공됩니다.

## 기여

기여는 언제나 환영합니다! 자유롭게 Pull Request를 보내주세요.