# Odoo QWebレポート作成完全ガイド

## QWebとは？

Odooの**テンプレートエンジン**です。XMLベースでPDFやHTMLを生成できます。

```
XMLテンプレート + データ = PDF/HTMLレポート
```

## 基本的なレポート作成

### Step 1: レポートアクションを定義

`reports/purchase_request_report.xml` を作成：

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- レポートアクション -->
    <record id="report_purchase_request" model="ir.actions.report">
        <field name="name">購買依頼書</field>
        <field name="model">my_module.purchase.request</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">my_module.report_purchase_request</field>
        <field name="report_file">my_module.report_purchase_request</field>
        <field name="print_report_name">'購買依頼書 - %s' % (object.name)</field>
        <field name="binding_model_id" ref="model_my_module_purchase_request"/>
        <field name="binding_type">report</field>
    </record>

    <!-- レポートテンプレート -->
    <template id="report_purchase_request">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <!-- ヘッダー -->
                        <div class="row">
                            <div class="col-12">
                                <h2 class="text-center">購買依頼書</h2>
                                <h4 class="text-center" t-field="doc.name"/>
                            </div>
                        </div>
                        
                        <!-- 基本情報 -->
                        <div class="row mt-4">
                            <div class="col-6">
                                <strong>依頼日:</strong>
                                <span t-field="doc.create_date" t-options="{'format': 'yyyy/MM/dd'}"/>
                            </div>
                            <div class="col-6 text-right">
                                <strong>ステータス:</strong>
                                <span t-field="doc.state"/>
                            </div>
                        </div>
                        
                        <div class="row mt-2">
                            <div class="col-6">
                                <strong>依頼者:</strong>
                                <span t-field="doc.requester_id.name"/>
                            </div>
                            <div class="col-6 text-right">
                                <strong>承認者:</strong>
                                <span t-field="doc.approver_id.name"/>
                            </div>
                        </div>
                        
                        <!-- 明細テーブル -->
                        <table class="table table-bordered mt-4">
                            <thead>
                                <tr>
                                    <th>No.</th>
                                    <th>商品名</th>
                                    <th>数量</th>
                                    <th>単価</th>
                                    <th>小計</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr t-foreach="doc.line_ids" t-as="line" t-key="line.id">
                                    <td><span t-esc="line_index + 1"/></td>
                                    <td><span t-field="line.product_id.name"/></td>
                                    <td class="text-right">
                                        <span t-field="line.quantity"/>
                                    </td>
                                    <td class="text-right">
                                        <span t-field="line.unit_price" 
                                              t-options="{'widget': 'monetary', 'display_currency': doc.currency_id}"/>
                                    </td>
                                    <td class="text-right">
                                        <span t-field="line.subtotal"
                                              t-options="{'widget': 'monetary', 'display_currency': doc.currency_id}"/>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <!-- 合計 -->
                        <div class="row">
                            <div class="col-12 text-right">
                                <h4>
                                    合計: <span t-field="doc.amount"
                                               t-options="{'widget': 'monetary', 'display_currency': doc.currency_id}"/>
                                </h4>
                            </div>
                        </div>
                        
                        <!-- フッター -->
                        <div class="row mt-5">
                            <div class="col-6">
                                <strong>依頼者署名:</strong>
                                <div style="border-bottom: 1px solid #000; height: 50px;"/>
                            </div>
                            <div class="col-6">
                                <strong>承認者署名:</strong>
                                <div style="border-bottom: 1px solid #000; height: 50px;"/>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>
```

### Step 2: __manifest__.py に追加

```python
'data': [
    ...
    'reports/purchase_request_report.xml',
],
```

### Step 3: 印刷ボタンを追加

フォームビューにボタンを追加：

```xml
<header>
    ...
    <button name="%(my_module.report_purchase_request)d" 
            string="印刷" 
            type="action"
            class="btn-secondary"
            invisible="state == 'draft'"/>
</header>
```

## QWebテンプレート構文

### 変数表示

```xml
<!-- フィールド表示 -->
<span t-field="doc.name"/>

<!-- 式評価 -->
<span t-esc="doc.amount * 1.1"/>

<!-- フォーマット付き -->
<span t-field="doc.date" t-options="{'format': 'yyyy年MM月dd日'}"/>
<span t-field="doc.amount" t-options="{'widget': 'monetary', 'display_currency': doc.currency_id}"/>
```

### 条件分岐

```xml
<t t-if="doc.state == 'approved'">
    <span class="badge badge-success">承認済み</span>
</t>
<t t-elif="doc.state == 'rejected'">
    <span class="badge badge-danger">却下</span>
</t>
<t t-else="">
    <span class="badge badge-secondary">その他</span>
</t>
```

### ループ

```xml
<!-- リスト走査 -->
<tr t-foreach="doc.line_ids" t-as="line" t-key="line.id">
    <td><span t-esc="line_index + 1"/></td>  <!-- カウンター -->
    <td><span t-field="line.product_id.name"/></td>
    <td><span t-field="line.quantity"/></td>
</tr>

<!-- ファースト/ラスト判定 -->
<t t-if="line_first">最初の行</t>
<t t-if="line_last">最後の行</t>
```

### サブテンプレート

```xml
<!-- 呼び出し -->
<t t-call="my_module.custom_header"/>

<!-- 定義 -->
<template id="custom_header">
    <div class="header">
        <img src="/my_module/static/src/img/logo.png"/>
        <h1 t-esc="company.name"/>
    </div>
</template>
```

## 高度なレポート

### 集計レポート

```xml
<template id="report_monthly_summary">
    <t t-call="web.html_container">
        <div class="page">
            <h1>月次集計レポート</h1>
            
            <!-- グループ化して集計 -->
            <t t-set="total_amount" t-value="0"/>
            
            <table class="table">
                <thead>
                    <tr>
                        <th>カテゴリ</th>
                        <th>件数</th>
                        <th>合計金額</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="docs.groupby('category_id')" t-as="category_group">
                        <t t-set="category" t-value="category_group[0]"/>
                        <t t-set="records" t-value="category_group[1]"/>
                        <t t-set="category_total" t-value="sum(r.amount for r in records)"/>
                        
                        <td><span t-field="category.name"/></td>
                        <td><span t-esc="len(records)"/></td>
                        <td><span t-esc="category_total"/></td>
                        
                        <t t-set="total_amount" t-value="total_amount + category_total"/>
                    </tr>
                </tbody>
            </table>
            
            <h3>総計: <span t-esc="total_amount"/></h3>
        </div>
    </t>
</template>
```

### 複数ページ対応

```xml
<template id="report_multi_page">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <!-- 1レコード1ページ -->
            <div class="page">
                <h1 t-field="doc.name"/>
                ...
            </div>
            
            <!-- 改ページ -->
            <p style="page-break-after: always;"/>
        </t>
    </t>
</template>
```

### ロゴとヘッダー/フッター

```xml
<template id="external_layout_custom">
    <div class="header">
        <div class="row">
            <div class="col-3">
                <img t-if="company.logo" 
                     t-att-src="image_data_uri(company.logo)" 
                     style="max-height: 50px;"/>
            </div>
            <div class="col-9 text-right">
                <strong t-field="company.name"/>
                <div t-field="company.partner_id" 
                     t-field-options="{'widget': 'contact', 'fields': ['address', 'phone'], 'no_marker': true}"/>
            </div>
        </div>
    </div>
    
    <div class="article">
        <t t-raw="0"/>
    </div>
    
    <div class="footer">
        <div class="text-center">
            Page <span class="page"/> / <span class="topage"/>
        </div>
    </div>
</template>
```

## CSSスタイル

```xml
<template id="report_styled">
    <t t-call="web.html_container">
        <t t-set="o" t-value="docs[0]"/>
        
        <style>
            .custom-table {
                width: 100%;
                border-collapse: collapse;
            }
            .custom-table th {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                padding: 8px;
            }
            .custom-table td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            .highlight {
                background-color: #ffeb3b;
            }
            .text-right {
                text-align: right;
            }
            .total-row {
                font-weight: bold;
                font-size: 1.2em;
            }
        </style>
        
        <div class="page">
            <table class="custom-table">
                ...
            </table>
        </div>
    </t>
</template>
```

## レポートをメールで送信

```python
class PurchaseRequest(models.Model):
    _inherit = 'my_module.purchase.request'
    
    def action_send_report_by_email(self):
        """レポートをメールで送信"""
        self.ensure_one()
        
        # レポートを生成
        report = self.env.ref('my_module.report_purchase_request')
        pdf_content, _ = report._render_qweb_pdf([self.id])
        
        # メールを作成
        template = self.env.ref('my_module.email_template_purchase_request')
        template.attachment_ids = [(0, 0, {
            'name': f'購買依頼書_{self.name}.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'mimetype': 'application/pdf',
        })]
        
        template.send_mail(self.id, force_send=True)
```

## レポートの継承と変更

```xml
<!-- 既存レポートを継承 -->
<template id="report_purchase_request_inherit" inherit_id="my_module.report_purchase_request">
    <xpath expr="//div[@class='page']" position="before">
        <div class="alert alert-info">
            これは継承による追加要素です
        </div>
    </xpath>
    
    <xpath expr="//span[@t-field='doc.amount']" position="after">
        <span>（税込）</span>
    </xpath>
</template>
```

## ベストプラクティス

1. **外部レイアウトを活用**: `web.external_layout` を使用して統一感を出す
2. **Bootstrapクラス**: `table`, `row`, `col-*` などを活用
3. **画像パス**: `image_data_uri()` を使用して埋め込み
4. **通貨表示**: `monetary` ウィジェットを使用
5. **ページ区切り**: `page-break-after` で制御

---

*本記事はAI自給自足計画の一環として作成されました*

#Odoo #QWeb #レポート #PDF #テンプレート #AI自給自足計画
