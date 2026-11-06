import asyncio
from playwright.async_api import async_playwright
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
PWD="Agh!bbTest2026#x7Q"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-blink-features=AutomationControlled"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",viewport={"width":1280,"height":900})
        pg=await ctx.new_page()
        await pg.goto("https://auth0.aghanim.com/u/signup/identifier?state=hKFo2SBvYTItVGJDQTBkZ25SeFh0TW1UUk5yeGZid3BBQ0g0SKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGNPT2hQbWdDTEhxYWFPZE9uSlJaSTRtZGFfTXpRYmoxo2NpZNkgRnFwQk5KaFhPeGVuRTBScW9DdlJUbkZucndlY0xWODA",wait_until="domcontentloaded",timeout=60000)
        await pg.wait_for_timeout(2500)
        await pg.fill('input[name="email"], input[type="email"]', EMAIL)
        await pg.click('button[type="submit"]')
        await pg.wait_for_timeout(6000)
        print("URL:",pg.url)
        print("BODY:",(await pg.inner_text("body"))[:900])
        await pg.screenshot(path="shot_signup2.png")
        await ctx.storage_state(path="state.json")
        await b.close()
asyncio.run(main())
