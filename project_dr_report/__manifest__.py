{
    "name": """Project Task - Document Release Report""",
    "summary": """Report for Document Release""",
    "category": """Project Management""",
    "images": ['images/checklist_main.png'],
    "version": "11.0.1.0.0",
    "application": False,

    "author": "MCR",

    "depends": ['base', 'project','project_task_subtask','project-dr'],
    "data": [
        'views/release_report.xml'
    ],
    "qweb": [
    ],
    "demo": [
        ''
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}