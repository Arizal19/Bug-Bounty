import asyncio,json
from playwright.async_api import async_playwright
URL="https://wikipedia-i2yx.aghanim.app/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":1000})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:300])) if any(h in r.url for h in ("api.aghanim","hub-api","my-api","pay-api")) else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if any(h in r.url for h in ("api.aghanim","hub-api","my-api","pay-api")) else None)
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(6000)
        print("URL:",pg.url)
        print("TEXT:",(await pg.inner_text("body"))[:900].replace("\n"," | "))
        await pg.screenshot(path="hub1.png",full_page=True)
        st=await ctx.storage_state(); json.dump(st,open("state_hub.json","w"),indent=1)
        print("COOKIES:",[(c["name"],c["domain"]) for c in st["cookies"]])
        print("--- net ---")
        for x in log[:40]: print(x[0],x[1],x[2][:120],x[3][:150])
        await b.close()
asyncio.run(main())
