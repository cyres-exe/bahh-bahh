OAUTH SPAM TOOL — SETUP
=======================

HOW IT WORKS
------------
Users visit your site → click "Login with Discord"
→ their OAuth token saved to tokens.txt
→ spammer uses those tokens to send messages as them
→ shows as your app in their Authorized Apps

SETUP
-----
1. discord.com/developers/applications
   → New Application
   → OAuth2 → Redirects → Add: http://localhost:5000/callback
   → copy Client ID + Client Secret

2. install deps
   pip install -r requirements.txt

3. run the auth server
   python oauth_server.py
   → enter Client ID + Client Secret
   → visit http://localhost:5000
   → click authorize → token saved to tokens.txt

4. run the spammer
   python spammer.py
   → enter channel ID + message + count
   → fires all tokens at once

GET CHANNEL ID
--------------
Discord → right click any channel → Copy Channel ID
(needs Developer Mode: Settings → Advanced → Developer Mode)

FONTS (type in message field)
------------------------------
**bold**
*italic*
__underline__
***bold italic***
~~strikethrough~~
# heading
-# small
> quote
`code`
||spoiler||
