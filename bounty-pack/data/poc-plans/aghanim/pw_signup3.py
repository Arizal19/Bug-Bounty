import asyncio,re
from playwright.async_api import async_playwright
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"; PWD="Agh!bbTest2026#x7Q"
async def dump(pg,tag):
    print(f"--- {tag}: {pg.url}")
    try: print((await pg.inner_text("body"))[:700].replace("\n"," | "))
    except: pass
    try:
        ins=await pg.eval_on_selector_all("input", "els=>els.map(e=>({name:e.name,type:e.type,id:e.id,ph:e.placeholder}))")
        print("inputs:",ins)
    except Exception as e: print("inputs err",e)
    try:
        bs=await pg.eval_on_selector_all("button","els=>els.map(e=>e.innerText.trim())")
        print("buttons:",bs)
    except: pass
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-blink-features=AutomationControlled"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",viewport={"width":1280,"height":900})
        pg=await ctx.new_page()
        await pg.goto("https://dashboard.aghanim.com/",wait_until="domcontentloaded",timeout=60000)
        await pg.wait_for_timeout(3500)
        await pg.get_by_role("link",name="Sign up").first.click(timeout=15000)
        await pg.wait_for_timeout(4000)
        await dump(pg,"signup-identifier")
        await pg.fill('input[name="email"]',EMAIL)
        await pg.click('button[type="submit"]')
        await pg.wait_for_timeout(7000)
        await dump(pg,"after-email")
        await pg.screenshot(path="shot_a.png")
        # try password step
        try:
            await pg.fill('input[name="password"]',PWD,timeout=8000)
            await pg.click('button[type="submit"]')
            await pg.wait_for_timeout(8000)
            await dump(pg,"after-password")
            await pg.screenshot(path="shot_b.png")
        except Exception as e: print("no password step:",str(e)[:120])
        await ctx.storage_state(path="state.json")
        await b.close()
asyncio.run(main())
