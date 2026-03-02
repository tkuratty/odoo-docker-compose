# Odoo Kanbanビュー完全ガイド

## Kanbanビューとは？

タスク管理に最適な**カード式ボード表示**です。ステータス別にカードをドラッグ＆ドロップで移動できます。

![Kanbanビュー例](images/kanban-example.png)

## 基本的なKanbanビュー

### Step 1: ビューを作成

`views/task_kanban_views.xml` を作成：

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_task_kanban" model="ir.ui.view">
        <field name="name">my_task_module.task.kanban</field>
        <field name="model">my_task_module.task</field>
        <field name="arch" type="xml">
            <kanban default_group_by="status">
                <!-- カードテンプレート -->
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_card">
                            <!-- ヘッダー -->
                            <div class="oe_kanban_content">
                                <div class="o_kanban_record_title">
                                    <field name="name"/>
                                </div>
                                
                                <!-- 担当者 -->
                                <div class="o_kanban_record_body">
                                    <field name="assignee_id"/>
                                </div>
                                
                                <!-- フッター -->
                                <div class="o_kanban_record_bottom">
                                    <span class="oe_kanban_list_many2many">
                                        <field name="deadline"/>
                                    </span>
                                    <span class="oe_kanban_list_many2many">
                                        <field name="priority" widget="priority"/>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- アクションを更新 -->
    <record id="action_task" model="ir.actions.act_window">
        <field name="name">タスク</field>
        <field name="res_model">my_task_module.task</field>
        <field name="view_mode">kanban,tree,form</field>
        <field name="search_view_id" ref="view_task_search"/>
    </record>
</odoo>
```

### Step 2: __manifest__.py に追加

```python
'data': [
    'security/ir.model.access.csv',
    'views/task_views.xml',
    'views/task_kanban_views.xml',  # 追加
],
```

### Step 3: モジュールを更新

```bash
# Odooを再起動
docker compose restart odoo

# アプリ → タスク管理 → モジュールを更新
```

## 高度なKanban設定

### カラー分け

```xml
<kanban default_group_by="status" 
        color_field="priority">  <!-- 優先度で色分け -->
```

### Quick Create（クイック作成）

```xml
<kanban quick_create="true" 
        quick_create_view="my_task_module.view_task_quick_create"
        on_create="quick_create">
```

### ドラッグ＆ドロップ制御

```xml
<kanban records_draggable="true"
        groups_draggable="true">
```

### カスタムカードデザイン

```xml
<t t-name="kanban-box">
    <div t-attf-class="oe_kanban_card oe_kanban_color_#{record.color.raw_value}">
        <!-- 優先度バッジ -->
        <div class="o_kanban_image">
            <field name="priority" widget="badge"/>
        </div>
        
        <!-- メインコンテンツ -->
        <div class="oe_kanban_details">
            <strong class="o_kanban_record_title">
                <field name="name"/>
            </strong>
            
            <!-- 期限切れ警告 -->
            <t t-if="record.is_overdue.raw_value">
                <span class="badge badge-danger">期限切れ</span>
            </t>
            
            <!-- 担当者アバター -->
            <div class="o_kanban_record_bottom">
                <img t-att-src="kanban_image('res.users', 'image_128', record.assignee_id.raw_value)"
                     class="oe_avatar oe_kanban_avatar_small"/>
            </div>
        </div>
    </div>
</t>
```

## プログレスバー

カラム上部に進捗バーを表示：

```xml
<kanban>
    <field name="status"/>
    <field name="priority"/>
    
    <progressbar field="priority" 
                 colors='{"high": "danger", "medium": "warning", "low": "success"}'/>
    
    <templates>
        ...
    </templates>
</kanban>
```

## カラム制御

### カスタムカラム作成

```xml
<kanban>
    <!-- +ボタンで新規カラム作成を許可 -->
    <field name="status" options="{'group_create': True}"/>
</kanban>
```

### カラム折りたたみ

```xml
<kanban archivable="true">
```

## 実用的な例

### タスク管理ボード

```xml
<record id="view_task_kanban_board" model="ir.ui.view">
    <field name="name">my_task_module.task.kanban.board</field>
    <field name="model">my_task_module.task</field>
    <field name="arch" type="xml">
        <kanban default_group_by="status" 
                quick_create="true">
            <field name="name"/>
            <field name="description"/>
            <field name="deadline"/>
            <field name="priority"/>
            <field name="assignee_id"/>
            <field name="is_overdue"/>
            
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_card">
                        <!-- カードヘッダー -->
                        <div class="o_kanban_record_head">
                            <strong>
                                <field name="name"/>
                            </strong>
                            <field name="priority" widget="priority"/>
                        </div>
                        
                        <!-- 説明（2行まで） -->
                        <div class="o_kanban_record_body">
                            <small class="text-muted">
                                <t t-esc="record.description.value.slice(0, 100)"/>
                            </small>
                        </div>
                        
                        <!-- フッター -->
                        <div class="o_kanban_record_bottom">
                            <span>
                                <i class="fa fa-calendar"></i>
                                <field name="deadline"/>
                            </span>
                            
                            <!-- 期限切れ警告 -->
                            <t t-if="record.is_overdue.raw_value">
                                <span class="badge badge-danger">
                                    <i class="fa fa-exclamation"></i> 期限切れ
                                </span>
                            </t>
                            
                            <!-- 担当者 -->
                            <field name="assignee_id" widget="many2one_avatar_user"/>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

## メニュー追加

```xml
<!-- Kanbanビュー専用メニュー -->
<record id="action_task_kanban" model="ir.actions.act_window">
    <field name="name">タスクボード</field>
    <field name="res_model">my_task_module.task</field>
    <field name="view_mode">kanban,tree,form</field>
    <field name="search_view_id" ref="view_task_search"/>
    <field name="context">{'group_by': 'status'}</field>
</record>

<menuitem id="menu_task_kanban" 
          name="タスクボード" 
          parent="menu_task_root" 
          action="action_task_kanban" 
          sequence="5"/>
```

## よくあるパターン

### 1. 営業パイプライン（CRM風）

```xml
<kanban default_group_by="stage_id">
    <field name="stage_id"/>
    <field name="expected_revenue"/>
    
    <templates>
        <t t-name="kanban-box">
            <div>
                <strong><field name="name"/></strong>
                <div class="text-right">
                    <strong><field name="expected_revenue" widget="monetary"/></strong>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

### 2. 在庫管理（倉庫別）

```xml
<kanban default_group_by="warehouse_id">
    <field name="product_id"/>
    <field name="quantity"/>
    <field name="image_small"/>
    
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <img t-att-src="kanban_image('product.product', 'image_128', record.product_id.raw_value)"
                     class="o_kanban_image"/>
                <div><field name="product_id"/></div>
                <div><field name="quantity"/> 個</div>
            </div>
        </t>
    </templates>
</kanban>
```

## カスタマイズTips

### CSSスタイル適用

```xml
<div class="oe_kanban_card" style="border-left: 4px solid #ff0000;">
```

### 条件付き表示

```xml
<t t-if="record.priority.raw_value == 'high'">
    <span class="badge badge-danger">重要</span>
</t>
<t t-elif="record.priority.raw_value == 'medium'">
    <span class="badge badge-warning">普通</span>
</t>
<t t-else="">
    <span class="badge badge-success">低</span>
</t>
```

### アクションボタン

```xml
<div class="oe_kanban_footer">
    <button type="object" name="action_done" class="btn btn-success btn-sm">
        完了
    </button>
    <button type="object" name="action_cancel" class="btn btn-danger btn-sm">
        キャンセル
    </button>
</div>
```

## 次のステップ

- [Calendarビューで予定管理](../calendar-view/README.md)
- [Ganttビューでプロジェクト管理](../gantt-view/README.md)

---

*本記事はAI自給自足計画の一環として作成されました*

#Odoo #Kanban #ビュー #UI #タスク管理 #AI自給自足計画
