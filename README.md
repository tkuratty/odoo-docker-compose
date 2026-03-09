# Odoo 18.0 モジュール開発入門

このブランチは「Odoo 18.0 モジュール開発入門」に対応しています。

## クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/tkuratty/odoo-docker-compose.git
cd odoo-docker-compose

# 2. このブランチをチェックアウト
git checkout article/module-development

# 3. コンテナを起動
docker compose up -d

# 4. ブラウザでアクセスしてモジュールをインストール
open http://localhost:8069
```

## サンプルモジュール

このブランチには「タスク管理モジュール」のサンプルが含まれています。

```
my_task_module/
├── __manifest__.py       # モジュール情報
├── __init__.py           # パッケージ初期化
├── models/
│   ├── __init__.py
│   └── task.py           # タスクモデル
├── views/
│   └── task_views.xml    # 画面定義
└── security/
    └── ir.model.access.csv  # アクセス権限
```

## インストール手順

1. Odooにログイン
2. 「アプリ」メニューを開く
3. 「アプリを更新」ボタンをクリック
4. 「My Task Module」を検索してインストール
5. 「タスク管理」メニューから利用開始

## 機能

- ✅ タスクの作成・編集・削除
- ✅ ステータス管理（下書き/進行中/完了）
- ✅ 優先度設定（低/中/高）
- ✅ 担当者アサイン
- ✅ 期限管理
- ✅ 期限切れ自動検出

## 学べること

- `__manifest__.py` の書き方
- モデル定義（fields, Selection, Many2one）
- 計算フィールド（compute）
- ビュー定義（tree, form, search）
- アクセス権限設定
- メニューとアクション

## カスタマイズしてみよう

`my_task_module/models/task.py` を編集して、新しいフィールドを追加してみてください！

---

*詳細な解説記事は別途参照*
