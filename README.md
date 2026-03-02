# Odoo Docker Compose

## ブランチ構成

- `main` - 安定版（Odoo 16）
- `18.0` - 開発版（Odoo 18.0 + 開発ツール）← 現在のブランチ

## 18.0ブランチの特徴

- **Odoo 18.0**（2024年10月リリースの最新版）対応
- **GitHub CLI (gh)** 同梱
- **Pre-commit** 設定済み
- **OCA準拠** の開発環境
- **VSCode Dev Container** 対応

## クイックスタート

```bash
git checkout 18.0
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

技術記事は別リポジトリで管理しています：

📚 **[my-documents](https://github.com/tkuratty/my-documents)** - Odoo技術記事集

- Odoo 18.0 + Docker開発環境構築ガイド
- VSCode + Dev Containerデバッグ環境構築ガイド
- Odooモジュール開発入門
- OCA（Odoo Community Association）完全ガイド
- Kanbanビュー完全ガイド
- ワークフローと承認フロー実装ガイド
- QWebレポート作成完全ガイド

## License

MIT
