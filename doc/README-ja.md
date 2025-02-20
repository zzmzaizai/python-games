# Python ゲームコレクション
[English](../README.md) | [中文](README-cn.md) | 日本語 | [한국어](README-ko.md) | [Français](README-fr.md) | [فارسی](README-fa.md)

Pygameで構築された古典的なアーケードゲームとパズルゲームのコレクションです。ブロック崩し、スネーク、パックマン、テトリス、ポン、五目並べ、2048の7つの楽しいゲームを収録しています。スムーズなメニュー遷移、ゲームパッドのサポート、モダンなUIデザインを実装しています。ゲーム開発の学習と娯楽に最適です。

## クイックスタート

### システム要件

- Python 3.8以上
- Pygame 2.0以上
- requirements.txtに記載されているその他の依存関係

### インストール

1. Python 3.8以上がインストールされていることを確認
2. 必要な依存関係をインストール：
   ```bash
   pip install -r requirements.txt
   ```

### ゲームの実行

```bash
# ゲームメニューを実行
python main.py
```

## ゲーム一覧

1. **ブロック崩し**
   - 古典的なブロック崩しゲーム
   - 異なる色のブロックで異なる得点
   - 角度に基づくボールの跳ね返り機構

2. **スネーク**
   - 古典的なスネークゲームの現代的解釈
   - スムーズな操作と衝突判定
   - スコアトラッキングと段階的な難易度

3. **パックマン**
   - シンプル化されたパックマン風ゲーム
   - 複数の色の敵
   - ドットを集めてポイント獲得

4. **テトリス**
   - 古典的なブロック積みパズルゲーム
   - 複数のブロック形状
   - ライン消去の仕組み

5. **ポン**
   - 2プレイヤー対戦型ポンゲーム
   - 角度に基づくボール物理演算
   - 5点先取で勝利

6. **五目並べ**
   - 伝統的な五目並べゲーム
   - シンプルで直感的な操作
   - 勝利条件：5つの石を一列に並べる

7. **2048**
   - 人気のパズルゲーム
   - タイルを結合して2048を目指す
   - ハイスコアに挑戦

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

## 操作方法

### キーボード操作
- 矢印キー：メニュー操作とゲーム操作
- Enter：メニュー項目の選択
- ESC：ゲーム一時停止/メニューに戻る
- R：ゲームのリスタート
- I：説明の表示/非表示

### ゲームパッド操作
- 左スティック/十字キー：メニュー操作とゲーム操作
- Aボタン：選択/確認
- Bボタン：戻る/キャンセル
- スタートボタン：ゲーム一時停止
- X/Yボタン：ゲーム固有の追加操作

### ゲーム別の操作方法

#### ブロック崩し
- 左右矢印キー：パドル移動
- ゲームパッド：左スティックまたは十字キーでパドル移動

#### スネーク
- 矢印キー：方向転換
- ゲームパッド：左スティックまたは十字キーで移動

#### パックマン
- 矢印キー：キャラクター移動
- ゲームパッド：左スティックまたは十字キーで移動

#### テトリス
- 左右：ブロック移動
- 上：ブロック回転
- 下：落下速度上昇
- スペース：即時落下
- ゲームパッド：左スティック/十字キーで移動、Aボタンで回転

#### ポン
- プレイヤー1：W/Sキー
- プレイヤー2：上下矢印キー
- ゲームパッド1：左スティックで左パドル操作
- ゲームパッド2：左スティックで右パドル操作

#### 五目並べ
- マウス：石を置く
- ゲームパッド：左スティック/十字キーでカーソル移動、Aボタンで石を置く

#### 2048
- 矢印キー：タイル移動
- ゲームパッド：左スティック/十字キーでタイル移動

## 機能

- スムーズなメニュー遷移とスケーリングアニメーション
- 完全なゲームパッドサポート
- 各ゲームのチュートリアルシステム
- セーブ/終了オプション付きの一時停止メニュー
- 段階的なゲーム難易度
- スコアトラッキングシステム
- モダンなUIとビジュアルフィードバック

## 配布用ビルド

このプロジェクトはPyInstallerを使用してスタンドアロン実行ファイルにパッケージ化できます。

### ビルド手順

1. PyInstallerのインストール：
   ```bash
   pip install pyinstaller
   ```

2. ビルドコマンドの実行：
   ```bash
   # Windows
   pyinstaller build.py --onefile --noconsole --icon=icon.ico --name="GameCollection"
   ```

3. 実行ファイルは`dist`ディレクトリに生成されます

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

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

貢献は歓迎します！お気軽にプルリクエストを送ってください。