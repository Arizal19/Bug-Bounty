import asyncio,json,time
from playwright.async_api import async_playwright
from gmail_otp import latest_code
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox","--disable-blink-features=AutomationControlled"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",viewport={"width":1400,"height":950})
        pg=await ctx.new_page()
        reqs=[]
        pg.on("response", lambda r: reqs.append(f"{r.status} {r.request.method} {r.url[:120]}") if "dashboard-api" in r.url else None)
        await pg.goto("https://dashboard.aghanim.com/",wait_until="domcontentloaded",timeout=60000)
        await pg.wait_for_timeout(3500)
        await pg.get_by_role("link",name="Sign up").first.click(timeout=15000)
        await pg.wait_for_timeout(3500)
        await pg.fill('input[name="email"]',EMAIL)
        await pg.click('button[type="submit"]')
        print("code requested at",time.strftime("%H:%M:%S"))
        code=None
        for i in range(14):
            await pg.wait_for_timeout(5000)
            r=latest_code(minutes=2)
            if r and r.get("code"):
                code=r["code"]; print("code:",code,r.get("subject")); break
        if not code:
            print("no code found"); await b.close(); return
        try:
            await pg.fill('input[name="code"], input[inputmode="numeric"]',code,timeout=15000)
            await pg.click('button[type="submit"]')
        except Exception as e:
            print("code fill fail",str(e)[:200])
        await pg.wait_for_timeout(12000)
        print("FINAL URL:",pg.url)
        try: print("BODY:",(await pg.inner_text("body"))[:800].replace("\n"," | "))
        except: pass
        await pg.screenshot(path="shot_logged.png",full_page=False)
        st=await ctx.storage_state()
        json.dump(st,open("state.json","w"),indent=1)
        print("COOKIES:",[c["name"] for c in st.get("cookies",[])])
        # try to read localStorage per origin
        for origin in st.get("origins",[]):
            print("ORIGIN",origin["origin"],[(i["name"],i["value"][:60]) for i in origin.get("localStorage",[])][:12])
        print("--- dashboard-api calls ---")
        for r in reqs[-25:]: print(r)
        await pg.screenshot(path="shot_logged2.png")
        await b.close()
asyncio.run(main())
