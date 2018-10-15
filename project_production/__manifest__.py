{
    "name": """Project Production Info""",
    "summary": """add field for Production Info""",
    "category": """Project Management""",
    "images": ['images/checklist_main.png'],
    "version": "11.0.1.0.0",
    "application": True,

    "author": "MCR",

    "depends": ['base', 'project'],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/project_production.xml'
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