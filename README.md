# Odoo 18.0 + Docker 開発環境構築

このブランチは「Odoo 18.0 + Docker開発環境構築ガイド」に対応しています。

## クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/tkuratty/odoo-docker-compose.git
cd odoo-docker-compose

# 2. このブランチをチェックアウト
git checkout article/odoo18-docker-setup

# 3. コンテナを起動
docker compose up -d

# 4. ブラウザでアクセス
open http://localhost:8069
```

## 含まれるもの

- Odoo 18.0（最新版）
- PostgreSQL 16
- GitHub CLI
- Pre-commit
- 開発用ツール一式

## ディレクトリ構成

```
.
├── docker-compose.yml    # Docker Compose設定
├── odoo18/
│   └── Dockerfile        # Odooカスタムイメージ
└── README.md             # このファイル
```

## 次のステップ

環境ができたら、モジュール開発やカスタマイズを始められます！

---

*詳細な解説記事は別途参照*
