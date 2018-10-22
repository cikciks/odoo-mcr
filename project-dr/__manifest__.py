{
    "name": """Project Task - Production  Document Release""",
    "summary": """add Document Release Information""",
    "category": """Project Management""",
    "images": ['images/checklist_main.png'],
    "version": "11.0.1.0.0",
    "application": True,

    "author": "MCR",

    "depends": ['base', 'project','project_task_subtask'],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/project_dr.xml'
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