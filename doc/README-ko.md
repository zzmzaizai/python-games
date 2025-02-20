# Python 게임 모음
[English](../README.md) | [中文](README-cn.md) | [日本語](README-ja.md) | 한국어 | [Français](README-fr.md) | [فارسی](README-fa.md)

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