# -*- coding: utf-8 -*-
"""Routes for the evernote addon.
"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from . import views

# Routes that use the web renderer
web_routes = {
    'rules': [

        ##### View file #####
    #     Rule(
    #         [
    #             '/project/<pid>/evernote/files/<path:path>',
    #             '/project/<pid>/node/<nid>/evernote/files/<path:path>',
    #         ],
    #         'get',
    #         views.crud.evernote_view_file,
    #         OsfWebRenderer('../addons/evernote/templates/evernote_view_file.mako'),
    #     ),


    #     ##### Download file #####
    #     Rule(
    #         [
    #             '/project/<pid>/evernote/files/<path:path>/download/',
    #             '/project/<pid>/node/<nid>/evernote/files/<path:path>/download/',
    #         ],
    #         'get',
    #         views.crud.evernote_download,
    #         notemplate,
    #     ),
    ],
}

# JSON endpoints
api_routes = {
    'rules': [

        ##### Node settings #####

        Rule(
            ['/project/<pid>/evernote/config/',
            '/project/<pid>/node/<nid>/evernote/config/'],
            'get',
            views.evernote_config_get,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/evernote/config/',
            '/project/<pid>/node/<nid>/evernote/config/'],
            'put',
            views.evernote_config_put,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/evernote/config/',
            '/project/<pid>/node/<nid>/evernote/config/'],
            'delete',
            views.evernote_deauthorize,
            json_renderer
        ),

        Rule(
            ['/project/<pid>/evernote/config/import-auth/',
            '/project/<pid>/node/<nid>/evernote/config/import-auth/'],
            'put',
            views.evernote_import_user_auth,
            json_renderer
        ),
    ],

    ## Your routes here

    'prefix': '/api/v1'
}
