import asyncio,json
from playwright.async_api import async_playwright
URL="https://pay.aghanim.com/link/lnk_eHriLMNNvUxvbFHm?player_id=bbtest-p2"
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":1000})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:600])) if any(h in r.url for h in ("pay-api","my-api","api.aghanim")) else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if any(h in r.url for h in ("pay-api","my-api","api.aghanim")) else None)
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(3000)
        await pg.fill('input[name="email"]',EMAIL)
        await pg.fill('input[name="cardNumber"]','4242424242424242')
        await pg.fill('input[name="expiryDate"]','12 / 30')
        await pg.fill('input[name="cvv"]','123')
        await pg.wait_for_timeout(1500)
        # click pay button
        clicked=False
        for sel in ['button:has-text("Pay")','button:has-text("Bayar")']:
            try:
                await pg.click(sel,timeout=5000); clicked=True; print("clicked",sel); break
            except: pass
        if not clicked: print("pay button not found"); print((await pg.inner_text("body"))[:800])
        await pg.wait_for_timeout(20000)
        print("URL:",pg.url)
        print("TEXT:",(await pg.inner_text("body"))[:800].replace("\n"," | "))
        await pg.screenshot(path="pay_done.png",full_page=True)
        st=await ctx.storage_state(); json.dump(st,open("state_pay.json","w"),indent=1)
        print("COOKIES:",[(c["name"],c["domain"]) for c in st["cookies"]])
        for o in st["origins"]:
            print("ORIGIN",o["origin"],[ (i["name"],i["value"][:80]) for i in o["localStorage"]][:10])
        print("--- net ---")
        for x in log: print(x[0],x[1],x[2][:110],x[3][:300])
        await b.close()
asyncio.run(main())
