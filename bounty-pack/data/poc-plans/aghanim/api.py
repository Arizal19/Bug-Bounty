import json,urllib.request,urllib.error,ssl,sys,time
ctx=ssl.create_default_context()
BASE="https://pay-api.aghanim.com"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
def call(method,path,body=None,extra=None,host=BASE,raw=False):
    url=host+path
    data=json.dumps(body).encode() if body is not None else None
    h={"User-Agent":UA,"X-Bug-Bounty":"RESEARCHER_EMAIL","Accept":"*/*","Origin":"https://pay.aghanim.com","Referer":"https://pay.aghanim.com/"}
    if data: h["Content-Type"]="application/json"
    if extra: h.update(extra)
    r=urllib.request.Request(url,data=data,headers=h,method=method)
    try:
        with urllib.request.urlopen(r,timeout=25,context=ctx) as resp:
            b=resp.read(); code=resp.status
    except urllib.error.HTTPError as e:
        b=e.read(); code=e.code
    except Exception as e:
        print(f"  !! {method} {path} -> {e}"); return None
    try: j=json.loads(b)
    except: j=b.decode('utf-8','replace')[:400]
    return code,j
