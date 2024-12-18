{
    'name':"To-Do App",
    'author': "Fatma",
    'category':"",
    'version':'17.0.0.1.0',
    'depends':['base','mail'],
    'data':['security/security.xml',
            'security/ir.model.access.csv',
            'data/sequence.xml',
            'views/base_menu.xml',
            'views/todo_task_view.xml',
            'wizard/assign_task_wizard_view.xml',
            'reports/todo_report.xml',
            ],
    'installable': True,
    'application':True

}


