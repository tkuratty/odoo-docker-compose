# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class TaskController(http.Controller):
    
    @http.route('/my_task_module/tasks', auth='user', type='json')
    def get_tasks(self):
        """タスク一覧をJSONで返す"""
        tasks = request.env['my_task_module.task'].search([])
        return {
            'tasks': [{
                'id': task.id,
                'name': task.name,
                'status': task.status,
                'priority': task.priority,
                'deadline': task.deadline.isoformat() if task.deadline else None,
                'is_overdue': task.is_overdue,
            } for task in tasks]
        }
    
    @http.route('/my_task_module/task/<int:task_id>', auth='user', type='json')
    def get_task(self, task_id):
        """特定のタスクをJSONで返す"""
        task = request.env['my_task_module.task'].browse(task_id)
        if not task.exists():
            return {'error': 'Task not found'}
        return {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'is_overdue': task.is_overdue,
            'assignee': task.assignee_id.name if task.assignee_id else None,
        }
