from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from . import views

api_routes = {
    'rules': [
        Rule(
            '/settings/dmptool/',
            'get',
            views.dmptool_user_config_get,
            json_renderer,
        ),
        Rule(
            '/settings/dmptool/accounts/',
            'post',
            views.dmptool_add_user_account,
            json_renderer,
        ),
        Rule(
            '/settings/dmptool/accounts/',
            'get',
            views.dmptool_account_list,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/settings/',
                '/project/<pid>/node/<nid>/dmptool/settings/',
            ],
            'get',
            views.dmptool_get_config,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/settings/',
                '/project/<pid>/node/<nid>/dmptool/settings/',
            ],
            'post',
            views.dmptool_set_config,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/user-auth/',
                '/project/<pid>/node/<nid>/dmptool/user-auth/',
            ],
            'put',
            views.dmptool_import_auth,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/user-auth/',
                '/project/<pid>/node/<nid>/dmptool/user-auth/',
            ],
            'delete',
            views.dmptool_deauthorize_node,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/list-datasets/',
                '/project/<pid>/node/<nid>/dmptool/list-datasets/',
            ],
            'post',
            views.dmptool_get_datasets,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/hgrid/root/',
                '/project/<pid>/node/<nid>/dmptool/hgrid/root/',
            ],
            'get',
            views.dmptool_root_folder,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/publish/',
                '/project/<pid>/node/<nid>/dmptool/publish/',
            ],
            'put',
            views.dmptool_publish_dataset,
            json_renderer,
        ),
        Rule(
            [
                '/project/<pid>/dmptool/widget/',
                '/project/<pid>/node/<nid>/dmptool/widget/',
            ],
            'get',
            views.dmptool_widget,
            OsfWebRenderer('../addons/dmptool/templates/dmptool_widget.mako'),
        ),
        Rule(
            [
                '/project/<pid>/dmptool/widget/contents/',
                '/project/<pid>/node/<nid>/dmptool/widget/contents/',
            ],
            'get',
            views.dmptool_get_widget_contents,
            json_renderer,
        ),
    ],
    'prefix': '/api/v1'
}
