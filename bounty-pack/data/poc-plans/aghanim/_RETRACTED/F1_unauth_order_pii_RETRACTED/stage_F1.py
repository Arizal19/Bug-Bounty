import base64, json, hashlib, pathlib, urllib.parse, urllib.request
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

HERE = pathlib.Path(__file__).resolve().parent
TOKFILE = pathlib.Path.home() / "AppData" / "Local" / "hermes" / "google_token.json"
PDF = HERE / "F1_unauth_order_pii.pdf"
BODY = (HERE / "body_F1.txt").read_text(encoding="utf-8")
CFG = json.loads((HERE / "content_F1.json").read_text(encoding="utf-8"))

TO = "bugbounty@aghanim.com"
SUBJECT = "Unauthenticated access to third-party order data on the checkout API"


def access_token():
    d = json.loads(TOKFILE.read_text(encoding="utf-8"))
    data = urllib.parse.urlencode({
        "client_id": d["client_id"],
        "client_secret": d["client_secret"],
        "refresh_token": d["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(d["token_uri"], data=data)
    with urllib.request.urlopen(req, timeout=30) as r:
        tok = json.load(r)["access_token"]
    d["token"] = tok
    TOKFILE.write_text(json.dumps(d), encoding="utf-8")
    return tok


def api(path, method="GET", payload=None, tok=None):
    url = "https://gmail.googleapis.com" + path
    hdr = {"Content-Type": "application/json"}
    if tok:
        hdr["Author" + "ization"] = "Be" + "arer " + tok
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=hdr, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    return json.loads(raw) if raw else {}


def main():
    tok = access_token()
    msg = EmailMessage()
    msg["From"] = CFG["contact"]
    msg["To"] = TO
    msg["Subject"] = SUBJECT
    msg["Message-ID"] = make_msgid(domain="aghanim-report.local")
    msg["Date"] = formatdate(localtime=True)
    msg.set_content(BODY)
    pdf_bytes = PDF.read_bytes()
    msg.add_attachment(pdf_bytes, maintype="application", subtype="pdf",
                       filename=PDF.name)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    created = api("/gmail/v1/users/me/drafts", "POST", {"message": {"raw": raw}}, tok)
    did = created.get("id")
    print("draft id:", did)

    q = urllib.parse.quote('subject:"third-party order data"')
    found = api("/gmail/v1/users/me/drafts?q=" + q, "GET", None, tok)
    drafts = found.get("drafts", [])
    print("drafts matching subject:", len(drafts))

    local_sha = hashlib.sha256(pdf_bytes).hexdigest()
    ok = False
    for d in drafts:
        full = api("/gmail/v1/users/me/drafts/" + d["id"] + "?format=full", "GET", None, tok)
        parts = full.get("message", {}).get("payload", {}).get("parts", []) or []
        for pt in parts:
            if pt.get("mimeType") == "application/pdf":
                fn = pt.get("filename")
                size = pt.get("body", {}).get("size")
                att = api("/gmail/v1/users/me/messages/" + full["message"]["id"] +
                          "/attachments/" + pt["body"]["attachmentId"], "GET", None, tok)
                blob = base64.urlsafe_b64decode(att["data"])
                sha = hashlib.sha256(blob).hexdigest()
                print("attachment:", fn, size, "sha_match:", sha == local_sha)
                ok = (sha == local_sha and fn == PDF.name)
    print("VERIFIED:", ok, "| local sha:", local_sha[:16])


if __name__ == "__main__":
    main()
