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
    'installable': True,
    'application': True,
}
