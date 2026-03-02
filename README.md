# Odoo Docker Compose

## ブランチ構成

- `main` - 安定版（Odoo 16）
- `19.0` - 開発版（Odoo 17 + 開発ツール）← 現在のブランチ

## 19.0ブランチの特徴

- **Odoo 17**（最新版）対応
- **GitHub CLI (gh)** 同梱
- **Pre-commit** 設定済み
- **OCA準拠** の開発環境
- **技術記事** 付属（`articles/`）

## クイックスタート

```bash
git checkout 19.0
docker compose up -d
```

## 含まれるツール

- Odoo 17
- PostgreSQL 16
- GitHub CLI
- Pre-commit
- pylint-odoo, flake8, black, isort
- debugpy

## 技術記事

- [Odoo 17 + Docker開発環境構築ガイド](articles/odoo17-docker-setup.md)

## License

MIT
