import json,re,time,sys,requests
TOK=r"C:\Users\WINDOWS10\AppData\Local\hermes\google_token.json"
d=json.load(open(TOK))
def access():
    r=requests.post(d["token_uri"],data={"client_id":d["client_id"],"client_secret":d["client_secret"],
        "refresh_token":d["refresh_token"],"grant_type":"refresh_token"},timeout=30)
    r.raise_for_status(); t=r.json()["access_token"]
    d["token"]=t; json.dump(d,open(TOK,"w")); return t
def get(url,t,**kw):
    r=requests.get(url,headers={"Authorization":f"Bearer {t}"},timeout=30,**kw); r.raise_for_status(); return r.json()
def latest_code(sender=None,minutes=10,pattern=r"\b(\d{6})\b"):
    t=access()
    q=f'newer_than:{minutes}m'
    if sender: q+=f' from:{sender}'
    m=get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages?q={requests.utils.quote(q)}&maxResults=5",t)
    for msg in m.get("messages",[]):
        full=get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}?format=full",t)
        hdrs={h['name'].lower():h['value'] for h in full['payload'].get('headers',[])}
        body=""
        def walk(p):
            nonlocal body
            if p.get('body',{}).get('data'): body+=p['body']['data']
            for c in p.get('parts',[]) or []: walk(c)
        walk(full['payload'])
        import base64
        try: txt=base64.urlsafe_b64decode(body+"="*(-len(body)%4)).decode('utf-8','replace')
        except: txt=""
        plain=re.sub(r'<[^>]+>',' ',txt)
        mm=re.search(pattern, plain) or re.search(pattern, hdrs.get('subject',''))
        if mm:
            return dict(id=msg['id'],subject=hdrs.get('subject'),from_=hdrs.get('from'),date=hdrs.get('date'),code=mm.group(1),snippet=plain[:200])
    return None
if __name__=="__main__":
    print(latest_code(sys.argv[1] if len(sys.argv)>1 else None))
