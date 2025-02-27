from os import environ


SESSION_CONFIGS = [
    
    dict(
         name='cazadores', display_name="Juego de cazadores", app_sequence=['cazadores'], num_demo_participants=2
     ),
    dict(
        name='public_goods_simple',
        display_name="Juego de bienes públicos",
        app_sequence=['consentimiento','public_goods_simple', 'survey','payment_info'],
        num_demo_participants=6,
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.100, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'S/ '
USE_POINTS = True

ROOMS = [
    dict(
        name='leel25',
        display_name='LEEL- Room para sesiones online',
        participant_label_file='_rooms/leel25.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '8225406367998'

INSTALLED_APPS = ['otree']
