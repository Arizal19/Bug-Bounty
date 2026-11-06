import asyncio,json
from playwright.async_api import async_playwright
SLUG="wikipedia-i2yx"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        # reuse dashboard session (auth0 cookies for dashboard.aghanim.com)
        ctx=await b.new_context(storage_state="state.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
            viewport={"width":430,"height":950})
        pg=await ctx.new_page()
        r=await pg.goto(f"https://dashboard.aghanim.com/api/auth/hub/{SLUG}?redirect_to=https%3A%2F%2F{SLUG}.aghanim.app",
                        wait_until="domcontentloaded",timeout=60000)
        print("auth/hub status:",r.status if r else None,"final:",pg.url)
        await pg.wait_for_timeout(4000)
        ck=await ctx.cookies()
        print("COOKIES:",[(c["name"],c["domain"],len(c["value"])) for c in ck])
        ss=[c for c in ck if c["name"]=="__ssid"]
        print("__ssid present:",bool(ss), ss[0]["domain"] if ss else "")
        await ctx.storage_state(path="state_hub2.json")
        await b.close()
asyncio.run(main())
