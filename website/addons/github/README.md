# OSF Github Addon

## Enabling the addon for development

1. On your Github user settings, go to “Applications” -> [Register new application](https://github.com/settings/applications/new).
2. Enter any name for the application name, e..g “OSF Github Addon (local)”
3. In the Homepage URL field, enter "http://localhost:5000/callback/“
4. In the Authorization Callback URL field, enter "http://localhost:5000/api/v1/addons/github/callback/".
5. Submit the form.
6. If `website/addons/github/settings/local.py` doesn't already exist, `cp website/addons/github/settings/defaults.py website/addons/github/settings/local.py`
7. Copy your `Client ID` and `Client Secret` from Github into the new local.py file.
8. In `website/settings/local.py` add, `"github"` to the `ADDONS_REQUESTED` list.
9. Restart your app server.

## Testing webhooks

To test Github webhooks, your development server must be exposed to the web using a service like ngrok:
* `brew install ngrok`
* `ngrok 5000`
* Copy forwarding address to `website/addons/github/settings/local.py:HOOK_DOMAIN`

