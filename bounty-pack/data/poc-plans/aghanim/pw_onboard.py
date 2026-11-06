import asyncio,json
from playwright.async_api import async_playwright
async def dump(pg,t):
    print(f"--- {t} {pg.url}")
    try: print((await pg.inner_text("body"))[:1000].replace("\n"," | "))
    except: pass
    try: print("inputs:",await pg.eval_on_selector_all("input","e=>e.map(x=>({n:x.name,t:x.type,v:x.value}))"))
    except: pass
    try: print("buttons:",await pg.eval_on_selector_all("button","e=>e.map(x=>x.innerText.trim()).filter(Boolean)"))
    except: pass
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(storage_state="state.json",user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":1400,"height":1000})
        pg=await ctx.new_page()
        await pg.goto("https://dashboard.aghanim.com/onboarding",wait_until="domcontentloaded",timeout=60000)
        await pg.wait_for_timeout(6000)
        await dump(pg,"onboarding")
        # cookie banner
        for lbl in ["Accept","Accept all"]:
            try:
                await pg.get_by_role("button",name=lbl).first.click(timeout=2500); break
            except: pass
        await pg.wait_for_timeout(1000)
        # check all checkboxes
        boxes=await pg.query_selector_all('input[type="checkbox"]')
        print("checkboxes:",len(boxes))
        for bx in boxes:
            try:
                if not await bx.is_checked(): await bx.check(force=True)
            except Exception as e: print("chk err",str(e)[:80])
        await pg.wait_for_timeout(800)
        for lbl in ["Continue","Next","Submit","Agree and continue","Finish"]:
            try:
                await pg.get_by_role("button",name=lbl).first.click(timeout=3000)
                print("clicked",lbl); break
            except: pass
        await pg.wait_for_timeout(8000)
        await dump(pg,"after-submit")
        await pg.screenshot(path="shot_onboard.png",full_page=True)
        st=await ctx.storage_state(); json.dump(st,open("state.json","w"),indent=1)
        await b.close()
asyncio.run(main())
