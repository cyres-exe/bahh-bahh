# oauth_server.py | pip install flask requests
from flask import Flask, redirect, request
import requests, os, json

app = Flask(__name__)

CLIENT_ID     = os.getenv("CLIENT_ID")     or input("Client ID: ").strip()
CLIENT_SECRET = os.getenv("CLIENT_SECRET") or input("Client Secret: ").strip()
REDIRECT_URI  = "http://localhost:5000/callback"
SCOPE         = "identify guilds.join"

@app.route("/")
def index():
    url = (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPE}"
    )
    return f'''
    <html><body style="background:#1e1e2e;color:#cdd6f4;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
    <div style="text-align:center">
        <h2>Authorize App</h2>
        <a href="{url}" style="background:#5865f2;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-size:16px">Login with Discord</a>
    </div></body></html>
    '''

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "error — no code"
    r = requests.post("https://discord.com/api/oauth2/token", data={
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  REDIRECT_URI,
    })
    data  = r.json()
    token = data.get("access_token")
    if not token:
        return f"error — {data}"
    # get user info
    user_r = requests.get("https://discord.com/api/v10/users/@me",
                          headers={"Authorization": f"Bearer {token}"})
    user = user_r.json()
    username = user.get("username", "unknown")
    # save token + username
    with open("tokens.txt", "a") as f:
        f.write(f"{token} | {username}\n")
    print(f"[+] token saved — {username}")
    return f'''
    <html><body style="background:#1e1e2e;color:#cdd6f4;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
    <div style="text-align:center"><h2>✅ Authorized!</h2><p>You can close this tab.</p></div>
    </body></html>
    '''

if __name__ == "__main__":
    print(f"[*] server running — http://localhost:5000")
    app.run(port=5000)
