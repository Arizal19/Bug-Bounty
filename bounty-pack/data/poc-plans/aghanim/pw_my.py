import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":950})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:250])) if "my-api" in r.url else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if "my-api" in r.url else None)
        await pg.goto("https://my.aghanim.com/en",wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(4000)
        print("URL:",pg.url)
        print("TEXT:",(await pg.inner_text("body"))[:1000].replace("\n"," | "))
        await pg.screenshot(path="my1.png",full_page=True)
        print("links:",await pg.eval_on_selector_all("a","e=>e.map(x=>[x.innerText.trim().slice(0,30),x.getAttribute('href')])"))
        print("buttons:",await pg.eval_on_selector_all("button","e=>e.map(x=>x.innerText.trim()).filter(Boolean)"))
        print("--- net ---")
        for x in log[:25]: print(x[0],x[1],x[2][:110],x[3][:200])
        await b.close()
asyncio.run(main())
