import asyncio,sys
from playwright.async_api import async_playwright
async def main(url):
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        pg=await ctx.new_page()
        reqs=[]
        pg.on("request", lambda r: reqs.append((r.method,r.url)))
        pg.on("response", lambda r: reqs.append(("<<",f"{r.status} {r.url}")))
        try:
            await pg.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print("goto warn:",str(e)[:200])
        print("URL:",pg.url)
        print("TITLE:",await pg.title())
        await pg.screenshot(path="shot1.png", full_page=False)
        txt=await pg.inner_text("body")
        print("BODY:",txt[:1200])
        print("--- requests ---")
        seen=set()
        for m,u in reqs:
            if u in seen: continue
            seen.add(u); print(m,u[:150])
        await b.close()
asyncio.run(main(sys.argv[1] if len(sys.argv)>1 else "https://dashboard.aghanim.com/"))
