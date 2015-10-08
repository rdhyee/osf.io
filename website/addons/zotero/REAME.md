# OSF Zotero Addon

Enabling the addon for development

1. In `website/settings/local.py` add, `"zotero"` to the `ADDONS_REQUESTED` list.
2. If `website/addons/zotero/settings/local.py` does not yet exist, create a local zotero settings file with `cp website/addons/zotero/settings/local-dist.py website/addons/zotero/settings/local.py`
3. [Register a new Zotero application](https://www.zotero.org/oauth/apps/new) and get a key and secret  (listed as `Client Key` and `Client Secret`) from <https://www.zotero.org/oauth/apps>.  
4. At the Zotero app console, add <http://localhost:5000/oauth/callback/zotero/> to your list of Oauth2 `redirect_uri`.
5. Enter your Zotero `Client Key` and `Client Secret` as `ZOTERO_CLIENT_ID` and `ZOTERO_CLIENT_SECRET` in `website/addons/zotero/settings/local.py`. 
