# VSCode + Odoo 18.0 デバッグ環境構築ガイド

## はじめに

Odooモジュール開発をするなら、**VSCode + Dev Containers**が最強です。

本記事では、Dockerコンテナ内でVSCodeを使って、ブレークポイントやステップ実行ができる開発環境を構築します。

## 完成形

```
.odoo-dev-env/
├── .devcontainer/
│   └── devcontainer.json    # Dev Container設定
├── .vscode/
│   ├── launch.json          # デバッグ設定
│   └── settings.json        # VSCode設定
├── docker-compose.yml
└── ...
```

## ステップバイステップ

### 1. Dev Container設定

`.devcontainer/devcontainer.json` を作成：

```json
{
  "name": "Odoo 18.0 Development",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "odoo",
  "workspaceFolder": "/workspace",
  
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.debugpy",
        "ms-python.vscode-pylance",
        "redhat.vscode-xml"
      ]
    }
  },
  
  "postCreateCommand": "pip install --user debugpy"
}
```

### 2. デバッグ設定

`.vscode/launch.json` を作成：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Odoo: Run with Debug",
      "type": "debugpy",
      "request": "launch",
      "program": "/usr/bin/odoo",
      "args": [
        "--config=/etc/odoo/odoo.conf",
        "--dev=all"
      ],
      "console": "integratedTerminal"
    }
  ]
}
```

### 3. VSCodeで開く

```bash
# リポジトリをクローン
git clone https://github.com/tkuratty/odoo-docker-compose.git
cd odoo-docker-compose
git checkout 19.0

# VSCodeで開く
code .
```

VSCodeの左下に「Reopen in Container」が表示されたらクリック！

### 4. デバッグ実行

1. `main.py` にブレークポイントを設定
2. F5キーでデバッグ開始
3. ステップ実行（F10）、ステップイン（F11）で確認

![デバッグ画面](assets/debug-screenshot.png)

## 便利なショートカット

| キー | 機能 |
|------|------|
| F5 | デバッグ実行 |
| F10 | ステップオーバー |
| F11 | ステップイン |
| Shift+F11 | ステップアウト |
| F9 | ブレークポイント切り替え |

## トラブルシューティング

### コンテナが起動しない

```bash
# Dev Containerログ確認
F1 → "Remote-Containers: Show Container Log"
```

### ブレークポイントが止まらない

```bash
# debugpyがインストールされているか確認
pip list | grep debugpy
```

## 次のステップ

環境ができたら、実際にOdooモジュールを開発してみましょう！

（次回記事：Odooモジュール開発入門 - scaffoldから始める）

---

*本記事はAI自給自足計画の一環として作成されました*

#Odoo #VSCode #DevContainer #デバッグ #AI自給自足計画
