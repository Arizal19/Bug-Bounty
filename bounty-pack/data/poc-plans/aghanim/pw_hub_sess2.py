import asyncio,json
from playwright.async_api import async_playwright
SLUG="wikipedia-i2yx"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(storage_state="state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
            viewport={"width":430,"height":950})
        pg=await ctx.new_page()
        api=[]
        pg.on("response", lambda r: api.append(f"{r.status} {r.request.method} {r.url[:110]}") if "aghanim" in r.url and ("auth" in r.url or "sso" in r.url or "__ssid" in r.url) else None)
        # 1) let the dashboard SPA route run (client-side) to mint hub session
        await pg.goto(f"https://dashboard.aghanim.com/api/auth/hub/{SLUG}", wait_until="networkidle", timeout=60000)
        await pg.wait_for_timeout(6000)
        print("A) url:",pg.url)
        ck=await ctx.cookies()
        print("A) __ssid:",[ (c["name"],c["domain"]) for c in ck if c["name"]=="__ssid"])
        print("A) net:",api[-6:])
        # 2) now open the hub itself with the same context
        await pg.goto(f"https://{SLUG}.aghanim.app/", wait_until="domcontentloaded", timeout=60000)
        await pg.wait_for_timeout(9000)
        print("B) url:",pg.url)
        try: print("B) text:",(await pg.inner_text("body"))[:300].replace("\n"," | "))
        except: pass
        ck=await ctx.cookies()
        print("B) all cookies:",[(c["name"],c["domain"]) for c in ck])
        await pg.screenshot(path="hub_sess.png",full_page=True)
        await ctx.storage_state(path="state_hub2.json")
        await b.close()
asyncio.run(main())
