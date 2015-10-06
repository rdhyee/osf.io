# OSF Dropbox Addon

Enabling the addon for development

1. In `website/settings/local.py` add, `"dropbox"` to `ADDONS_REQUESTED`.
2. If `website/addons/dropbox/settings/local.py` does not yet exist, Create a local dropbox settings file with `cp website/addons/dropbox/settings/local-dist.py website/addons/dropbox/setings/local.py`
3. Create an app and get a key and secret from https://www.dropbox.com/developers/apps.
5. At the Dropbox app console, add <http://localhost:5000/api/v1/addons/dropbox/oauth/finish/> to your list of Oauth2 redirect URIs. (or should it be <http://localhost:5000/oauth/callback/dropbox/>?)
4. Enter your dropbox `App key` and `App secret` as  `DROPBOX_KEY` key and `DROPBOX_SECRET` respectively in `website/addons/dropbox/settings/local.py`. 
