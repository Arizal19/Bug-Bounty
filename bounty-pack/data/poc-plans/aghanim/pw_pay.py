import asyncio,json
from playwright.async_api import async_playwright
URL="https://pay.aghanim.com/link/lnk_eHriLMNNvUxvbFHm?player_id=bbtest-p1"
EMAIL="RESEARCHER_USERNAME+agh1@gmail.com"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        ctx=await b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",viewport={"width":430,"height":1000})
        pg=await ctx.new_page()
        log=[]
        pg.on("request",lambda r: log.append(("REQ",r.method,r.url,(r.post_data or "")[:500])) if any(h in r.url for h in ("pay-api","my-api","api.aghanim")) else None)
        pg.on("response",lambda r: log.append(("RES",str(r.status),r.url,"")) if any(h in r.url for h in ("pay-api","my-api","api.aghanim")) else None)
        await pg.goto(URL,wait_until="networkidle",timeout=60000)
        await pg.wait_for_timeout(4000)
        # print inputs
        ins=await pg.eval_on_selector_all("input","e=>e.map(x=>({n:x.name,id:x.id,ph:x.placeholder,t:x.type,ae:x.autocomplete}))")
        print("inputs:",ins)
        await pg.screenshot(path="pay1.png",full_page=True)
        print("TEXT:",(await pg.inner_text("body"))[:600].replace("\n"," | "))
        await b.close()
        print("--- net ---")
        for x in log: print(x[0],x[1],x[2][:110],x[3][:160])
asyncio.run(main())
