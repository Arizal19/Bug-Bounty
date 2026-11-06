import urllib.request, ssl, json
from concurrent.futures import ThreadPoolExecutor
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
hosts="api.aghanim.com dashboard.aghanim.com dashboard-api.aghanim.com events.aghanim.com events-web.aghanim.com hub-api.aghanim.com hub-api-global.aghanim.com my.aghanim.com my-api.aghanim.com pay.aghanim.com pay-api.aghanim.com s2s-api.aghanim.com sdk-api.aghanim.com upload.aghanim.com api.aghanim.store my-api.aghanim.store pay-api.aghanim.store hub-api.aghanim.store".split()
paths=["/","/robots.txt","/openapi.json","/swagger-ui/index.html","/api-docs","/health","/version"]
def get(u,timeout=10):
    r=urllib.request.Request(u,headers={"User-Agent":UA,"X-Bug-Bounty":"RESEARCHER_EMAIL","Accept":"*/*"})
    try:
        with urllib.request.urlopen(r,timeout=timeout,context=ctx) as resp:
            return resp.status, resp.headers.get("Content-Type",""), resp.headers.get("Server",""), resp.read(400)
    except urllib.error.HTTPError as e:
        try: b=e.read(300)
        except: b=b""
        return e.code, e.headers.get("Content-Type",""), e.headers.get("Server",""), b
    except Exception as e:
        return None, str(e)[:50], "", b""
def job(args):
    h,p=args
    s,ct,sv,b=get(f"https://{h}{p}")
    return (h,p,s,ct,sv,len(b),b[:100].decode('utf-8','replace').replace('\n',' '))
tasks=[(h,p) for h in hosts for p in paths]
with ThreadPoolExecutor(max_workers=24) as ex:
    res=list(ex.map(job,tasks))
cur=None
for h,p,s,ct,sv,n,sn in res:
    if h!=cur: print("="*78); print(h); cur=h
    print(f"  {p:22} {str(s):5} {ct[:26]:26} {n:4} | {sn}")
