# Odoo Docker Compose

## ブランチ構成

- `main` - 安定版（Odoo 16）
- `19.0` - 開発版（Odoo 18.0 + 開発ツール）← 現在のブランチ

## 19.0ブランチの特徴

- **Odoo 18.0**（2024年10月リリースの最新版）対応
- **GitHub CLI (gh)** 同梱
- **Pre-commit** 設定済み
- **OCA準拠** の開発環境
- **技術記事** 付属（`docs/`）

## クイックスタート

```bash
git checkout 19.0
docker compose up -d
```

## 含まれるツール

- Odoo 18.0（最新版）
- PostgreSQL 16
- GitHub CLI
- Pre-commit
- pylint-odoo, flake8, black, isort
- debugpy

## 技術記事

- [Odoo 18.0 + Docker開発環境構築ガイド](docs/odoo18-docker-setup.md)

## License

MIT
