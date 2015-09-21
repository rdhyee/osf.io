from . import model
from . import routes
from . import views

MODELS = [
    model.AddonEvernoteUserSettings,
    model.AddonEvernoteNodeSettings,
]
USER_SETTINGS_MODEL = model.AddonEvernoteUserSettings
NODE_SETTINGS_MODEL = model.AddonEvernoteNodeSettings

ROUTES = [routes.api_routes, routes.web_routes]

SHORT_NAME = 'evernote'
FULL_NAME = 'Evernote'

OWNERS = ['user', 'node']  # can include any of ['user', 'node']

VIEWS = []  # page, widget
CONFIGS = ['node']  # any of ['user', 'node']

CATEGORIES = ['storage']

INCLUDE_JS = {
    'page': [],
    'files': []
}

INCLUDE_CSS = {
    'page': [],
    'files': []
}

HAS_HGRID_FILES = True  # set to True for storage addons that display in HGrid
#GET_HGRID_DATA = views.hgrid.evernote_hgrid_data
# MAX_FILE_SIZE = 10  # MB
