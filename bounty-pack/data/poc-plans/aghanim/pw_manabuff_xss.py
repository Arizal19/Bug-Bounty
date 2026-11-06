import asyncio,json
from playwright.async_api import async_playwright
TOK=open("hub_tok_demo.txt").read().strip()
print("token loaded:", len(TOK)>100, "len_ok")
async def main():
    dialogs=[]; results=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
                                viewport={"width":430,"height":950})
        pg=await ctx.new_page()
        pg.on("dialog", lambda d: (dialogs.append(d.message), asyncio.create_task(d.accept())))
        for url in [f"https://manabuff.com/go/login?token={TOK}", "https://manabuff.com/"]:
            try:
                await pg.goto(url, wait_until="domcontentloaded", timeout=45000)
                await pg.wait_for_timeout(8000)
            except Exception as e:
                print("goto:",str(e)[:90]); continue
            info=await pg.evaluate("""()=>{
                const img=[...document.querySelectorAll('img')].filter(i=>i.getAttribute('src')==='x');
                const bbx=[...document.querySelectorAll('b')].filter(e=>e.textContent==='BBXSS');
                return {url:location.href, injectedImg:img.length, injectedB:bbx.length,
                        htmlHasOnError: document.documentElement.innerHTML.includes('onerror=alert'),
                        bodyText: document.body.innerText.slice(0,160)};
            }""")
            print(json.dumps(info)[:400])
            results.append(info)
            await pg.screenshot(path="mb_%d.png"%len(results), full_page=False)
        print("DIALOGS:",dialogs)
        await b.close()
asyncio.run(main())
