import asyncio,json
from playwright.async_api import async_playwright
URL="https://pay.aghanim.com/link/lnk_eHriLMNNvUxvbFHm?player_id=bbtest-b1"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":932})
        pg=await ctx.new_page()
        log=[]
        async def on_req(r):
            if any(h in r.url for h in ("pay-api","my-api","api.aghanim")):
                body=None
                try: body=r.post_data
                except: pass
                log.append(("REQ",r.method,r.url,(body or "")[:400]))
        async def on_res(r):
            if any(h in r.url for h in ("pay-api","my-api","api.aghanim")):
                log.append(("RES",r.status,r.url,""))
        pg.on("request",lambda r: asyncio.create_task(on_req(r)))
        pg.on("response",lambda r: asyncio.create_task(on_res(r)))
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(5000)
        print("URL:",pg.url); print("TEXT:",(await pg.inner_text("body"))[:1200].replace("\n"," | "))
        await pg.screenshot(path="co1.png",full_page=True)
        print("--- net ---")
        for x in log: print(x[0],x[1],x[2][:110],x[3][:200])
        await b.close()
asyncio.run(main())
