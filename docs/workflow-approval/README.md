# Odoo ワークフローと承認フロー実装ガイド

## ワークフローとは？

レコードが状態遷移する際の**ビジネスロジック**を制御します。

```
下書き → 承認待ち → 承認済み → 完了
   ↓       ↓          ↓
キャンセル  却下      保留
```

## 基本的なステータス管理

### Step 1: モデルに状態を追加

```python
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class PurchaseRequest(models.Model):
    _name = 'my_module.purchase.request'
    _description = '購買依頼'
    
    name = fields.Char(string='依頼番号', required=True, copy=False, readonly=True, default='New')
    
    state = fields.Selection([
        ('draft', '下書き'),
        ('submit', '承認待ち'),
        ('approved', '承認済み'),
        ('rejected', '却下'),
        ('done', '完了'),
        ('cancel', 'キャンセル'),
    ], string='ステータス', default='draft', tracking=True)
    
    requester_id = fields.Many2one('res.users', string='依頼者', default=lambda self: self.env.user)
    approver_id = fields.Many2one('res.users', string='承認者')
    
    amount = fields.Float(string '金額')
    line_ids = fields.One2many('my_module.purchase.request.line', 'request_id', string='明細')
    
    # 承認権限チェック
    can_approve = fields.Boolean(string='承認可能', compute='_compute_can_approve')
    
    @api.depends('state', 'approver_id')
    def _compute_can_approve(self):
        for rec in self:
            rec.can_approve = (
                rec.state == 'submit' and 
                rec.approver_id == self.env.user
            )
```

### Step 2: ワークフローアクション

```python
    # ========== アクション定義 ==========
    
    def action_submit(self):
        """承認依頼を提出"""
        for rec in self:
            if rec.state != 'draft':
                raise UserError('下書き状態でのみ提出できます')
            
            # バリデーション
            if not rec.line_ids:
                raise UserError('明細を追加してください')
            
            if rec.amount <= 0:
                raise UserError('金額を入力してください')
            
            # 承認者を自動割り当て（例：上司）
            manager = rec.requester_id.employee_id.parent_id.user_id
            if not manager:
                raise UserError('承認者が設定されていません')
            
            rec.write({
                'state': 'submit',
                'approver_id': manager.id,
            })
            
            # 通知を送信
            self._send_notification(
                rec.approver_id,
                f'購買依頼 {rec.name} の承認が必要です'
            )
    
    def action_approve(self):
        """承認する"""
        for rec in self:
            if rec.state != 'submit':
                raise UserError('承認待ち状態でのみ承認できます')
            
            if rec.approver_id != self.env.user:
                raise UserError('承認者のみ承認できます')
            
            rec.write({
                'state': 'approved',
            })
            
            # 承認済み通知
            self._send_notification(
                rec.requester_id,
                f'購買依頼 {rec.name} が承認されました'
            )
    
    def action_reject(self):
        """却下する"""
        for rec in self:
            if rec.state != 'submit':
                raise UserError('承認待ち状態でのみ却下できます')
            
            rec.write({
                'state': 'rejected',
            })
    
    def action_cancel(self):
        """キャンセル"""
        for rec in self:
            if rec.state in ('done', 'cancel'):
                raise UserError('この状態ではキャンセルできません')
            
            rec.write({
                'state': 'cancel',
            })
    
    def action_reset_to_draft(self):
        """下書きに戻す"""
        for rec in self:
            if rec.state not in ('rejected', 'cancel'):
                raise UserError('却下またはキャンセル状態でのみ戻せます')
            
            rec.write({
                'state': 'draft',
                'approver_id': False,
            })
    
    def action_done(self):
        """完了"""
        for rec in self:
            if rec.state != 'approved':
                raise UserError('承認済みのもののみ完了できます')
            
            rec.write({
                'state': 'done',
            })
    
    # ========== ユーティリティ ==========
    
    def _send_notification(self, user, message):
        """通知を送信"""
        if user:
            self.env['bus.bus']._sendone(
                user.partner_id,
                'simple_notification',
                {
                    'title': 'ワークフロー通知',
                    'message': message,
                    'type': 'success',
                }
            )
```

### Step 3: フォームビューにボタンを追加

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_purchase_request_form" model="ir.ui.view">
        <field name="name">my_module.purchase.request.form</field>
        <field name="model">my_module.purchase.request</field>
        <field name="arch" type="xml">
            <form string="購買依頼">
                <header>
                    <!-- ステータスバー -->
                    <field name="state" widget="statusbar" 
                           statusbar_visible="draft,submit,approved,done"/>
                    
                    <!-- ボタン（ステータス別） -->
                    <button name="action_submit" string="提出" type="object"
                            class="oe_highlight" invisible="state != 'draft'"/>
                    
                    <button name="action_approve" string="承認" type="object"
                            class="oe_highlight" invisible="state != 'submit' or not can_approve"/>
                    
                    <button name="action_reject" string="却下" type="object"
                            class="btn-danger" invisible="state != 'submit' or not can_approve"/>
                    
                    <button name="action_done" string="完了" type="object"
                            class="oe_highlight" invisible="state != 'approved'"/>
                    
                    <button name="action_cancel" string="キャンセル" type="object"
                            invisible="state in ('done', 'cancel')"/>
                    
                    <button name="action_reset_to_draft" string="下書きに戻す" type="object"
                            invisible="state not in ('rejected', 'cancel')"/>
                </header>
                
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" readonly="1"/>
                        </h1>
                    </div>
                    
                    <group>
                        <group>
                            <field name="requester_id" readonly="1"/>
                            <field name="approver_id" invisible="state == 'draft'"/>
                            <field name="can_approve" invisible="1"/>
                        </group>
                        <group>
                            <field name="amount"/>
                        </group>
                    </group>
                    
                    <notebook>
                        <page string="明細">
                            <field name="line_ids">
                                <tree editable="bottom">
                                    <field name="product_id"/>
                                    <field name="quantity"/>
                                    <field name="unit_price"/>
                                    <field name="subtotal"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
                
                <!-- チャットと履歴 -->
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>
</odoo>
```

## 多段階承認（階層承認）

```python
class PurchaseRequest(models.Model):
    _inherit = 'my_module.purchase.request'
    
    approval_level = fields.Integer(string='承認段階', default=0)
    max_approval_level = fields.Integer(string='最大承認段階', default=2)
    
    def action_approve(self):
        """多段階承認"""
        for rec in self:
            if rec.approval_level < rec.max_approval_level - 1:
                # 次の承認者へ
                next_manager = rec.approver_id.employee_id.parent_id.user_id
                rec.write({
                    'approval_level': rec.approval_level + 1,
                    'approver_id': next_manager.id if next_manager else False,
                })
                
                self._send_notification(
                    rec.approver_id,
                    f'購買依頼 {rec.name} の第{rec.approval_level + 1}段階承認が必要です'
                )
            else:
                # 最終承認
                super(PurchaseRequest, rec).action_approve()
```

## 自動ワークフロー（Automated Actions）

### 期限切れ自動キャンセル

```xml
<!-- data/automated_actions.xml -->
<record id="ir_cron_cancel_expired_requests" model="ir.cron">
    <field name="name">期限切れ依頼の自動キャンセル</field>
    <field name="model_id" ref="model_my_module_purchase_request"/>
    <field name="state">code</field>
    <field name="code">
expired_requests = model.search([
    ('state', '=', 'submit'),
    ('create_date', '&lt;', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
])
for request in expired_requests:
    request.action_cancel()
    </field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
</record>
```

## レコードロック

```python
class PurchaseRequest(models.Model):
    _inherit = 'my_module.purchase.request'
    
    # 編集可能かどうか
    is_editable = fields.Boolean(compute='_compute_is_editable')
    
    @api.depends('state', 'requester_id')
    def _compute_is_editable(self):
        for rec in self:
            rec.is_editable = (
                rec.state == 'draft' and 
                rec.requester_id == self.env.user
            )
    
    def write(self, vals):
        """更新時のチェック"""
        for rec in self:
            if not rec.is_editable and not self.env.user.has_group('base.group_system'):
                raise UserError('このレコードは編集できません')
        return super(PurchaseRequest, self).write(vals)
```

## ワークフローログ

```python
class PurchaseRequest(models.Model):
    _inherit = 'my_module.purchase.request'
    
    history_ids = fields.One2many('my_module.request.history', 'request_id', string='履歴')
    
    def write(self, vals):
        """状態変更時に履歴を記録"""
        if 'state' in vals:
            for rec in self:
                self.env['my_module.request.history'].create({
                    'request_id': rec.id,
                    'old_state': rec.state,
                    'new_state': vals['state'],
                    'user_id': self.env.user.id,
                    'date': fields.Datetime.now(),
                })
        return super(PurchaseRequest, self).write(vals)

class RequestHistory(models.Model):
    _name = 'my_module.request.history'
    _description = '依頼履歴'
    
    request_id = fields.Many2one('my_module.purchase.request', required=True)
    old_state = fields.Char(string='旧ステータス')
    new_state = fields.Char(string='新ステータス')
    user_id = fields.Many2one('res.users', string='実行者')
    date = fields.Datetime(string='実施日時')
    note = fields.Text(string='備考')
```

## ベストプラクティス

1. **常にバリデーション**: 状態遷移前に条件チェック
2. **権限管理**: 誰がどのアクションを実行できるか明確に
3. **通知**: ステータス変更時は関係者に通知
4. **履歴**: 重要な変更はログに残す
5. **戻し機能**: 間違えた時に元に戻せるように

---

*本記事はAI自給自足計画の一環として作成されました*

#Odoo #ワークフロー #承認フロー #ステータス管理 #ビジネスロジック #AI自給自足計画
