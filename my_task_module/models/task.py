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
