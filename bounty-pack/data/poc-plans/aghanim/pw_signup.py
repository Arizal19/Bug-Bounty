import asyncio,sys,json
from playwright.async_api import async_playwright
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
PWD="Agh!bbTest2026#x7Q"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-blink-features=AutomationControlled"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",viewport={"width":1280,"height":900})
        pg=await ctx.new_page()
        await pg.goto("https://dashboard.aghanim.com/",wait_until="domcontentloaded",timeout=60000)
        await pg.wait_for_timeout(4000)
        print("URL0:",pg.url)
        # click Sign up
        try:
            await pg.get_by_role("link", name="Sign up").first.click(timeout=10000)
        except Exception as e:
            try: await pg.click("text=Sign up", timeout=8000)
            except Exception as e2: print("signup click fail",e2)
        await pg.wait_for_timeout(5000)
        print("URL1:",pg.url); print((await pg.inner_text("body"))[:800])
        await pg.screenshot(path="shot_signup.png")
        await ctx.storage_state(path="state.json")
        await b.close()
asyncio.run(main())
