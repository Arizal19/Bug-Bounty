import asyncio,json
from playwright.async_api import async_playwright
from gmail_otp import latest_code
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":950})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:400])) if "my-api" in r.url else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if "my-api" in r.url else None)
        await pg.goto("https://my.aghanim.com/en",wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(2500)
        try: await pg.get_by_role("button",name="Accept").first.click(timeout=3000)
        except: pass
        ins=await pg.eval_on_selector_all("input","e=>e.map(x=>({n:x.name,t:x.type,ph:x.placeholder}))")
        print("inputs:",ins)
        try:
            await pg.fill('input[type="email"], input[name="email"]',EMAIL,timeout=8000)
            await pg.get_by_role("button",name="Continue").first.click(timeout=8000)
        except Exception as e: print("fill/click:",str(e)[:120])
        await pg.wait_for_timeout(6000)
        print("URL:",pg.url)
        print("TEXT:",(await pg.inner_text("body"))[:600].replace("\n"," | "))
        await pg.screenshot(path="my2.png",full_page=True)
        ins=await pg.eval_on_selector_all("input","e=>e.map(x=>({n:x.name,t:x.type,ph:x.placeholder}))")
        print("inputs2:",ins)
        print("--- net ---")
        for x in log[:20]: print(x[0],x[1],x[2][:110],x[3][:300])
        await ctx.storage_state(path="state_my.json")
        await b.close()
asyncio.run(main())
