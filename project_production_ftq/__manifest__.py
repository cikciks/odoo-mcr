{
    "name": """Project FTQ Info""",
    "summary": """add First Time Quality Info""",
    "category": """Project Management""",
    "images": ['images/checklist_main.png'],
    "version": "11.0.1.0.0",
    "application": True,

    "author": "MCR",

    "depends": ['project_production'],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/project_production_ftq.xml'
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