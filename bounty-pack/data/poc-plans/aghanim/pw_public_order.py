import asyncio, json
from playwright.async_api import async_playwright
URL="https://pay.aghanim.com/en/order/ord_eFnCYslSTNAhPSCm"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":900})
        pg=await ctx.new_page()
        calls=[]
        async def on_res(r):
            if any(h in r.url for h in ("aghanim.com")) and "pay-api" in r.url or "checkout/v1" in r.url:
                calls.append((r.status, r.request.method, r.url))
        pg.on("response", lambda r: asyncio.create_task(on_res(r)))
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(5000)
        print("FINAL URL:",pg.url)
        txt=await pg.inner_text("body")
        print("\n=== RENDERED PAGE TEXT ===")
        print(txt[:1200])
        print("\n=== API CALLS THE PAGE MADE ===")
        for c in calls: print(" ",c[0],c[1],c[2][:110])
        await pg.screenshot(path="public_order.png",full_page=True)
        await b.close()
asyncio.run(main())
