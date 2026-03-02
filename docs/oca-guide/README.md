# OCA（Odoo Community Association）完全ガイド

## OCAとは？

**Odoo Community Association（OCA）** は、Odooのオープンソースコミュニティを支える非営利組織です。

> **使命**: "Odooのエコシステムを促進し、オープンソースの協力的な開発を支えること"

## 組織構造

### 運営体制
- **非営利団体**: ベルギーに本部を置くNPO
- **ボランティア主導**: 世界中の開発者・ユーザーが参加
- **企業スポンサー**: 複数のOdooパートナー企業が支援

### 主要メンバー
- **Contributors**: コードを貢献する開発者
- **Maintainers**: リポジトリを管理するメンテナー
- **Project Leaders**: 各プロジェクト（モジュール群）の責任者
- **Board**: 理事会（戦略的な意思決定）

## 目的と理念

### コアバリュー
1. **オープンソース**: すべてのコードはオープンソース（LGPL/AGPL）
2. **協働**: 競合より協働を重視
3. **品質**: 厳格なコードレビューとテスト
4. **持続可能性**: 長期的なメンテナンスを保証

### なぜOCAが必要か？
- **ベンダーロックイン防止**: 特定企業に依存しない
- **品質保証**: 複数のレビューアーが品質を担保
- **知見の集約**: ベストプラクティスの共有
- **持続的開発**: 企業が撤退してもコードが残る

## 活動内容

### 1. モジュール開発
**GitHub Organization**: https://github.com/OCA

```
主要リポジトリ（例）:
├── account-financial-tools    # 会計・財務
├── account-invoicing          # 請求管理
├── bank-statement-import      # 銀行取り込み
├── connector                  # 外部連携フレームワーク
├── field-service              # フィールドサービス
├── helpdesk                   # ヘルプデスク
├── hr                         # 人事管理
├── partner-contact            # 取引先管理
├── pos                        # POS（店舗販売）
├── project                    # プロジェクト管理
├── purchase-workflow          # 購買ワークフロー
├── sale-workflow              # 販売ワークフロー
├── server-tools               # サーバー汎用ツール
├── stock-logistics            # 在庫・物流
├── web                        # Web UI拡張
└── website                    # Webサイト機能
```

### 2. 標準化活動
- **OCB (Odoo Community Backports)**: コミュニティ版Odooのメンテナンス
- **MIG（Migration）**: バージョン間の移行ツール
- **SET（Setup Tools）**: 開発環境標準化

### 3. イベント・コミュニティ
- **OCA Days**: 年次カンファレンス
- **Hackathons**: 開発者向けハッカソン
- **Webinars**: オンライン学習会

## コード開発フロー

### 1. 貢献の流れ
```
1. Issue作成
   └─ バグ報告や機能提案

2. 開発（Developer）
   └─ コード作成
   └─ ローカルテスト

3. Pull Request（PR）
   └─ GitHubでPR作成
   └─ CLA（Contributor License Agreement）署名

4. レビュー（Reviewers）
   └─ コードレビュー
   └─ 機能テスト
   └─ 承認（Approve）

5. マージ（Maintainers）
   └─ mainブランチへマージ
   └─ 自動デプロイ（PyPI/Apps Store）
```

### 2. 品質管理システム

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/OCA/odoo-pre-commit-hooks
    rev: v0.0.25
    hooks:
      - id: oca-checks-odoo-module  # XML/Pythonチェック
      - id: oca-checks-po             # 翻訳ファイルチェック

  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black  # Pythonフォーマット

  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8  # リントチェック
```

#### CI/CD Pipeline
```
GitHub Actions:
├── テスト実行（Runboat）
├── カバレッジ計測（Codecov）
├── ドキュメント生成
└─ PyPI公開（リリース時）
```

### 3. ブランチ戦略

```
リポジトリ構造:
├── 16.0      # Odoo 16.0対応
├── 17.0      # Odoo 17.0対応  
├── 18.0      # Odoo 18.0対応（現在）
└── main      # 開発用（最新）

各ブランチ:
├── 保護設定: Maintainersのみマージ可
├── 必須チェック: CI通過が必須
└── レビュー: 最低2名のApprove必要
```

## コードの利用方法

### 1. GitHubから直接インストール
```bash
# 特定モジュールをクローン
git clone -b 18.0 https://github.com/OCA/project.git

# addons_pathに追加
./odoo-bin --addons-path=./project,./addons
```

### 2. pipでインストール
```bash
# PyPIからインストール
pip install odoo18-addon-project-task-add-state
```

### 3. Odoo Apps Store
https://apps.odoo.com/apps/browse?author=OCA

## CLA（Contributor License Agreement）

### 貢献者同意書
OCAにコードを貢献するにはCLAへの同意が必要：

```
目的:
- OCAがコードを自由に配布・変更できることを保証
- 貢献者が自分の貢献物の権利を持っていることを宣言
- 将来の法的問題を防ぐ

署名方法:
1. GitHubアカウントで https://odoo-community.org/page/cla にアクセス
2. Individual CLA（個人）または Entity CLA（企業）を選択
3. 電子署名
```

## 貢献の始め方

### Step 1: 環境構築
```bash
# OCAリポジトリをフォーク
git clone https://github.com/OCA/project.git
cd project

# 開発ブランチを作成
git checkout -b 18.0-fix-task-bug origin/18.0
```

### Step 2: 開発
```bash
# モジュールを作成/修正
cd project_task_add_state

# Pre-commitを実行
pre-commit run --all-files

# テストを実行
pytest
```

### Step 3: PR作成
```bash
git add .
git commit -m "[FIX] project_task: Fix state transition bug

- Fix issue where task state doesn't update correctly
- Add test case for state machine

Fixes #123"

git push origin 18.0-fix-task-bug
```

GitHubでPR作成 → レビュー待ち → マージ

## OCA vs Odoo SA（公式）

| 項目 | OCA | Odoo SA（公式）|
|------|-----|---------------|
| **ライセンス** | LGPL/AGPL | LGPL/Proprietary（Enterprise）|
| **開発者** | コミュニティ | Odoo SA社員 |
| **価格** | 無料 | Community無料/Enterprise有料 |
| **サポート** | コミュニティ | 公式サポート（Enterprise）|
| **機能** | 拡張機能が豊富 | 基本機能＋Enterprise機能 |
| **品質** | レビュー制 | 社内QA |

## まとめ

OCAはOdooエコシステムにおいて：
- **品質の高い拡張機能**を提供
- **オープンソースの持続可能性**を担保
- **知見の集約と標準化**を推進
- **グローバルな開発者コミュニティ**を形成

OCAモジュールを使うことで、エンタープライズ版に依存せずに高度な機能を実現できます。

---

*本記事はAI自給自足計画の一環として作成されました*

#OCA #Odoo #オープンソース #コミュニティ #AI自給自足計画
