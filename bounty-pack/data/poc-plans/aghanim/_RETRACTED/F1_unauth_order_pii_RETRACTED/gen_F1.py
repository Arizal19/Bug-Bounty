import json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from aghanim_style import P, B, C, H1, H2, BODYS, SMALL, tbl, meta_table, make_docs
from reportlab.platypus import Spacer, Image, PageBreak

CFG = json.loads((HERE / "content_F1.json").read_text(encoding="utf-8"))
FIGDIR = HERE / "evidence"
OUT = HERE / "F1_unauth_order_pii.pdf"


def build():
    s = [P(CFG["title"], H1)]
    s.append(meta_table([
        ["Target", CFG["target"]],
        ["Asset", CFG["asset"]],
        ["Endpoint", CFG["endpoint"]],
        ["Severity", CFG["severity"] + " (" + CFG["score"] + ")"],
        ["CVSS v3.1", CFG["cvss"]],
        ["CWE", CFG["cwe"]],
        ["Researcher", CFG["researcher"] + " <" + CFG["contact"] + ">"],
        ["Found", CFG["date_found"] + " from " + CFG["test_location"] + ", " + CFG["test_ip"]],
    ]))
    s.append(Spacer(1, 12))
    for sec in CFG["sections"]:
        t = sec["t"]
        if t == "h2":
            s.append(P(sec["v"], H2))
        elif t == "p":
            s.append(P(sec["v"], BODYS))
        elif t == "small":
            s.append(P(sec["v"], SMALL))
        elif t == "code":
            s.append(C(sec["v"]))
        elif t == "pagebreak":
            s.append(PageBreak())
        elif t == "figure":
            s.append(Image(str(FIGDIR / sec["n"]), width=470, height=302))
            s.append(P(sec["cap"], SMALL))
        elif t == "table":
            s.append(tbl([tuple(r) for r in [sec["h"]] + sec["rows"]], widths=sec["w"]))
        s.append(Spacer(1, 8))
    return s


if __name__ == "__main__":
    make_docs(str(OUT), CFG["title"], CFG["researcher"], build)
    print("built", OUT)
