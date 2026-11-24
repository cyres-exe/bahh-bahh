# spammer.py | pip install aiohttp
import aiohttp, asyncio

async def spam_with_token(session, token: str, channel_id: int, message: str, count: int, username: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    async def _send():
        try:
            async with session.post(url, json={"content": message}, headers=headers) as r:
                if r.status == 429:
                    data = await r.json()
                    await asyncio.sleep(data.get("retry_after", 1))
                    await session.post(url, json={"content": message}, headers=headers)
        except Exception:
            pass

    await asyncio.gather(*[_send() for _ in range(count)])
    print(f"[+] done — {username} sent {count} messages")

async def main():
    if not __import__("os").path.exists("tokens.txt"):
        print("[-] tokens.txt not found — run oauth_server.py first")
        return

    with open("tokens.txt") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    if not lines:
        print("[-] no tokens found")
        return

    print(f"[*] {len(lines)} token(s) loaded")
    for l in lines:
        parts = l.split(" | ")
        print(f"  → {parts[1] if len(parts) > 1 else 'unknown'}")

    channel_id = int(input("\nchannel id: ").strip())
    message    = input("message: ").strip()
    count      = int(input("count per token: ").strip())

    async with aiohttp.ClientSession() as session:
        tasks = []
        for line in lines:
            parts    = line.split(" | ")
            token    = parts[0].strip()
            username = parts[1].strip() if len(parts) > 1 else "unknown"
            tasks.append(spam_with_token(session, token, channel_id, message, count, username))
        await asyncio.gather(*tasks)

    print("\n[*] all done")

asyncio.run(main())
