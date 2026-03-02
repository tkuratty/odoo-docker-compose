# VSCode + Odoo 18.0 デバッグ環境構築

このブランチは「VSCode + Dev Container デバッグ環境構築ガイド」に対応しています。

## クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/tkuratty/odoo-docker-compose.git
cd odoo-docker-compose

# 2. このブランチをチェックアウト
git checkout article/vscode-debug-setup

# 3. VSCodeで開く
code .

# 4. 「Reopen in Container」をクリック
# 5. コンテナが起動したら http://localhost:8069 にアクセス
```

## 含まれるもの

- Odoo 18.0（最新版）
- PostgreSQL 16
- **Dev Container設定**（.devcontainer/）
- **VSCodeデバッグ設定**（.vscode/）
- GitHub CLI
- Pre-commit
- debugpy（デバッガー）

## デバッグ機能

- F5: デバッグ実行
- F10: ステップオーバー
- F11: ステップイン
- F9: ブレークポイント切り替え

## ディレクトリ構成

```
.
├── .devcontainer/        # Dev Container設定
│   └── devcontainer.json
├── .vscode/              # VSCode設定
│   ├── launch.json       # デバッグ設定
│   └── settings.json     # エディタ設定
├── docker-compose.yml    # Docker Compose設定
├── odoo18/
│   └── Dockerfile        # Odooカスタムイメージ
└── README.md             # このファイル
```

## トラブルシューティング

### "Reopen in Container"が表示されない

Remote - Containers拡張機能をインストール：
```
Ctrl+Shift+X → "Remote - Containers"を検索 → インストール
```

### ブレークポイントで止まらない

コンテナ内でdebugpyがインストールされているか確認：
```bash
docker compose exec odoo pip list | grep debugpy
```

---

*詳細な解説記事は別途参照*
