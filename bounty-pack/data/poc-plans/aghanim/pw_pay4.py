import asyncio,json,re
from playwright.async_api import async_playwright
URL="https://pay.aghanim.com/link/lnk_eHriLMNNvUxvbFHm?player_id=bbtest-p5"
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":1000})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:900])) if any(h in r.url for h in ("pay-api","my-api","api.aghanim")) else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if any(h in r.url for h in ("pay-api","my-api","api.aghanim")) else None)
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(3000)
        oid=re.search(r'/order/(ord_[A-Za-z0-9]+)',pg.url).group(1)
        print("order",oid)
        r=await pg.evaluate("""async (oid)=>{const res=await fetch('https://pay-api.aghanim.com/order/v1/orders/'+oid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({country:'GB'})}); return [res.status, (await res.text()).slice(0,120)]}""",oid)
        print("patch GB ->",r)
        await pg.reload(wait_until="networkidle")
        await pg.wait_for_timeout(4000)
        print("TEXT:",(await pg.inner_text("body"))[:400].replace("\n"," | "))
        try:
            await pg.fill('input[name="email"]',EMAIL)
            await pg.fill('input[name="cardNumber"]','4242424242424242')
            await pg.fill('input[name="expiryDate"]','12 / 30')
            await pg.fill('input[name="cvv"]','123')
            print("filled")
        except Exception as e: print("fill err",str(e)[:100])
        await pg.wait_for_timeout(2000)
        for sel in ['button:has-text("Pay £")','button:has-text("Pay")']:
            try:
                await pg.click(sel,timeout=6000); print("clicked",sel); break
            except: pass
        await pg.wait_for_timeout(30000)
        print("URL:",pg.url)
        print("TEXT:",(await pg.inner_text("body"))[:600].replace("\n"," | "))
        await pg.screenshot(path="pay_done3.png",full_page=True)
        st=await ctx.storage_state(); json.dump(st,open("state_pay.json","w"),indent=1)
        print("COOKIES:",[(c["name"],c["domain"]) for c in st["cookies"]])
        print("--- net ---")
        for x in log[-18:]: print(x[0],x[1],x[2][:100],x[3][:450])
        await b.close()
asyncio.run(main())
