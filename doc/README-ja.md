# Python ゲームコレクション
[English](../README.md) | [中文](README-cn.md) | 日本語 | [한국어](README-ko.md) | [Français](README-fr.md) | [فارسی](README-fa.md)

## プロジェクト構造

```
.
├── main.py          # メインプログラムエントリー
├── games/           # ゲームモジュールディレクトリ
│   ├── __init__.py
│   ├── breakout.py  # ブロック崩しゲーム
│   ├── snake.py     # スネークゲーム
│   ├── pacman.py    # パックマンゲーム
│   ├── tetris.py    # テトリスゲーム
│   ├── pong.py      # ポンゲーム
│   ├── gomoku.py    # 五目並べゲーム
│   └── game2048.py  # 2048ゲーム
├── requirements.txt  # プロジェクトの依存関係
├── build.py         # ビルドスクリプト
└── resources/       # リソースファイル
    └── icon.ico     # アプリケーションアイコン
```

## 開発ガイド
### 新しいゲームの追加

新しいゲームを追加するには、以下の手順に従ってください：

1. 新しいPythonファイルを作成
2. 以下の必須メソッドを含むGameクラスを実装：
   - `__init__()`: ゲーム状態の初期化
   - `run()`: メインゲームループ
   - `handle_input()`: ユーザー入力の処理
   - `update()`: ゲーム状態の更新
   - `draw()`: グラフィックスのレンダリング
3. `main.py`にゲーム情報を追加