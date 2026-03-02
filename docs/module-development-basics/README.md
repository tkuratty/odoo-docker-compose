# Odoo 18.0 モジュール開発入門

## はじめに

Odooのカスタマイズを始めるなら、まず「モジュール開発」の基礎を理解しましょう。

本記事では、シンプルな「タスク管理モジュール」を作りながら、Odooモジュール開発の基本を学びます。

## 完成形

```
my_task_module/
├── __manifest__.py      # モジュール情報
├── __init__.py          # Pythonパッケージ初期化
├── models/
│   ├── __init__.py
│   └── task.py          # モデル定義
├── views/
│   └── task_views.xml   # 画面定義
└── security/
    └── ir.model.access.csv  # アクセス権限
```

## ステップバイステップ

### Step 1: scaffoldで雛形作成

Odooにはモジュールの雛形を自動生成する `scaffold` コマンドがあります：

```bash
# Odooコンテナに入る
docker compose exec odoo bash

# モジュール雛形を作成
cd /mnt/extra-addons
odoo scaffold my_task_module /mnt/extra-addons
```

**生成されるファイル：**

```
my_task_module/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── controllers.py
├── demo/
│   └── demo.xml
├── models/
│   ├── __init__.py
│   └── models.py
├── security/
│   └── ir.model.access.csv
└── views/
    ├── templates.xml
    └── views.xml
```

### Step 2: __manifest__.py を編集

モジュールの基本情報を設定：

```python
{
    'name': "My Task Module",
    'summary': """シンプルなタスク管理モジュール""",
    'description': """
        このモジュールは基本的なタスク管理機能を提供します。
        - タスクの作成・編集・削除
        - ステータス管理
        - 担当者アサイン
    """,
    'author': "Your Name",
    'website': "https://www.example.com",
    'category': 'Productivity',
    'version': '1.0.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/task_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
```

### Step 3: モデルを作成

`models/task.py` を作成：

```python
from odoo import models, fields, api

class Task(models.Model):
    _name = 'my_task_module.task'
    _description = 'Task'

    name = fields.Char(string='タスク名', required=True)
    description = fields.Text(string='説明')
    
    status = fields.Selection([
        ('draft', '下書き'),
        ('in_progress', '進行中'),
        ('done', '完了'),
    ], string='ステータス', default='draft')
    
    priority = fields.Selection([
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ], string='優先度', default='medium')
    
    assignee_id = fields.Many2one('res.users', string='担当者')
    deadline = fields.Date(string='期限')
    
    # 計算フィールド
    is_overdue = fields.Boolean(
        string='期限切れ',
        compute='_compute_is_overdue',
        store=True
    )
    
    @api.depends('deadline', 'status')
    def _compute_is_overdue(self):
        for task in self:
            if task.deadline and task.status != 'done':
                task.is_overdue = task.deadline < fields.Date.today()
            else:
                task.is_overdue = False
```

`models/__init__.py` を更新：

```python
from . import task
```

### Step 4: ビューを作成

`views/task_views.xml` を作成：

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- ツリー（リスト）ビュー -->
    <record id="view_task_tree" model="ir.ui.view">
        <field name="name">my_task_module.task.tree</field>
        <field name="model">my_task_module.task</field>
        <field name="arch" type="xml">
            <tree string="タスク">
                <field name="name"/>
                <field name="status"/>
                <field name="priority"/>
                <field name="assignee_id"/>
                <field name="deadline"/>
                <field name="is_overdue"/>
            </tree>
        </field>
    </record>

    <!-- フォームビュー -->
    <record id="view_task_form" model="ir.ui.view">
        <field name="name">my_task_module.task.form</field>
        <field name="model">my_task_module.task</field>
        <field name="arch" type="xml">
            <form string="タスク">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="status"/>
                        <field name="priority"/>
                    </group>
                    <group>
                        <field name="assignee_id"/>
                        <field name="deadline"/>
                        <field name="is_overdue" readonly="1"/>
                    </group>
                    <notebook>
                        <page string="説明">
                            <field name="description"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- 検索ビュー -->
    <record id="view_task_search" model="ir.ui.view">
        <field name="name">my_task_module.task.search</field>
        <field name="model">my_task_module.task</field>
        <field name="arch" type="xml">
            <search string="タスク検索">
                <field name="name"/>
                <field name="assignee_id"/>
                <filter name="draft" string="下書き" domain="[('status', '=', 'draft')]"/>
                <filter name="in_progress" string="進行中" domain="[('status', '=', 'in_progress')]"/>
                <filter name="done" string="完了" domain="[('status', '=', 'done')]"/>
                <group expand="0" string="グループ化">
                    <filter name="group_by_status" string="ステータス" context="{'group_by': 'status'}"/>
                    <filter name="group_by_assignee" string="担当者" context="{'group_by': 'assignee_id'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- アクション -->
    <record id="action_task" model="ir.actions.act_window">
        <field name="name">タスク</field>
        <field name="res_model">my_task_module.task</field>
        <field name="view_mode">tree,form</field>
        <field name="search_view_id" ref="view_task_search"/>
    </record>

    <!-- メニュー -->
    <menuitem id="menu_task_root" name="タスク管理" sequence="10"/>
    <menuitem id="menu_task" name="タスク" parent="menu_task_root" action="action_task" sequence="10"/>
</odoo>
```

### Step 5: アクセス権限を設定

`security/ir.model.access.csv` を作成：

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_task_user,Task User,my_task_module.model_my_task_module_task,base.group_user,1,1,1,1
```

### Step 6: モジュールをインストール

1. Odooの「アプリ」メニューを開く
2. 「アプリを更新」ボタンをクリック
3. 「My Task Module」を検索してインストール

### Step 7: 動作確認

1. 「タスク管理」メニューが表示される
2. 「タスク」メニューからタスクを作成
3. フォームで各フィールドを入力
4. リストビューでタスク一覧を確認

## 次のステップ

基本ができたら、以下の機能を追加してみましょう：

- **カンバンビュー**: ステータス別のボード表示
- **メール通知**: 期限が近づいたら通知
- **レポート**: PDF出力機能
- **ワークフロー**: 承認フローの追加

（次回記事：Odooビュー詳細 - Kanban、Calendar、Gantt）

---

*本記事はAI自給自足計画の一環として作成されました*

#Odoo #モジュール開発 #入門 #Tutorial #AI自給自足計画
