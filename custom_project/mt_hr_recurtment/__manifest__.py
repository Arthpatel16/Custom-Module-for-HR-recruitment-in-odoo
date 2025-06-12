{
    'name' : 'HR Recurtment AI-Resume Filter',
    'version': '17.0',
    'category': 'HR',
    'sequence': 1,
    'summary': 'HR Recurtment AI-Resume Filter',
    "author": "Moltis LLP",
    "website": "https://moltis.net",
    'description': """
        HR Recurtment AI-Resume Filter
    """,
    'depends': ['base','hr_recruitment','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_applicant.xml',
        'views/hr_job.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'licence': 'OPL-1'
}
