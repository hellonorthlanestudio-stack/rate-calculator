#!/usr/bin/env python3
"""Render Northlane Studio pin images (1000x1500 PNG) from a JSON spec file.

Usage: python3 render_pin.py specs.json OUT_DIR [FONT_DIR]

FONT_DIR must contain the .woff2 files copied from @fontsource/fraunces
(latin-700/800-normal) and @fontsource/inter (latin-400/600/700-normal).
Each spec item: id, badge, headline (list of lines), subline, card_title,
rows [{name, meta, tag, tone}], cta.  tone: overdue | waiting | paid | plain
"""
import html, json, os, sys
from playwright.sync_api import sync_playwright

TONES = {
    "overdue": ("#FBE3E0", "#C2463E"),
    "waiting": ("#FDF1D3", "#9A6A00"),
    "paid": ("#E2F1E7", "#2E6B4F"),
    "plain": ("#ECE7DB", "#4A5A52"),
}


def build_html(s, font_dir):
    def ff(family, weight, fname):
        return (
            "@font-face{font-family:'%s';font-weight:%d;src:url('file://%s/%s') format('woff2');}"
            % (family, weight, font_dir, fname)
        )

    fonts = "".join(
        [
            ff("Fraunces", 700, "fraunces-latin-700-normal.woff2"),
            ff("Fraunces", 800, "fraunces-latin-800-normal.woff2"),
            ff("Inter", 400, "inter-latin-400-normal.woff2"),
            ff("Inter", 600, "inter-latin-600-normal.woff2"),
            ff("Inter", 700, "inter-latin-700-normal.woff2"),
        ]
    )
    headline = "<br>".join(html.escape(l).replace("-", "&#8209;") for l in s["headline"])
    rows = ""
    for r in s["rows"]:
        bg, fg = TONES.get(r.get("tone", "plain"), TONES["plain"])
        tag = (
            '<span class="tag" style="background:%s;color:%s">%s</span>'
            % (bg, fg, html.escape(r["tag"]))
            if r.get("tag")
            else ""
        )
        meta = '<div class="meta">%s</div>' % html.escape(r["meta"]) if r.get("meta") else ""
        rows += (
            '<div class="row"><div class="rl"><div class="name">%s</div>%s</div>%s</div>'
            % (html.escape(r["name"]), meta, tag)
        )
    return """<!doctype html><html><head><meta charset="utf-8"><style>
%s
*{box-sizing:border-box;margin:0;padding:0}
body{width:1000px;height:1500px;background:#1F4D3A;color:#fff;font-family:'Inter',sans-serif;position:relative;overflow:hidden}
.badge{position:absolute;left:70px;top:80px;background:#D7F27A;color:#1F4D3A;font-weight:800;font-size:26px;letter-spacing:1.5px;text-transform:uppercase;padding:14px 28px;border-radius:999px}
h1{position:absolute;left:70px;top:190px;width:860px;font-family:'Fraunces',serif;font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-1px}
.sub{position:absolute;left:70px;top:%dpx;width:830px;font-size:36px;line-height:1.3;color:#d9e6df}
.card{position:absolute;left:60px;right:60px;top:%dpx;background:#F4F0E8;border-radius:28px;padding:34px 36px;box-shadow:0 22px 50px rgba(0,0,0,.35)}
.ct{font-size:22px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:#6B7A72;margin-bottom:20px;display:flex;justify-content:space-between}
.row{background:#fff;border:1.5px solid #E3DDCF;border-radius:16px;padding:22px 26px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;gap:18px}
.row:last-child{margin-bottom:0}
.name{font-size:30px;font-weight:700;color:#1B2B24;line-height:1.2}
.meta{font-size:24px;color:#6B7A72;margin-top:6px}
.tag{font-size:24px;font-weight:700;padding:10px 20px;border-radius:999px;white-space:nowrap}
.foot{position:absolute;left:70px;right:70px;bottom:50px;height:70px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:18px}
.logo{width:64px;height:64px;background:#fff;border-radius:16px;color:#1F4D3A;font-family:'Fraunces',serif;font-weight:800;font-size:44px;display:flex;align-items:center;justify-content:center}
.bn{font-family:'Fraunces',serif;font-weight:700;font-size:34px}
.compact .row{padding:14px 22px;margin-bottom:10px}.compact .name{font-size:27px}.compact .meta{font-size:21px;margin-top:4px}.compact .tag{font-size:21px;padding:8px 16px}.compact .ct{margin-bottom:14px}
.cta{background:#D7F27A;color:#1F4D3A;font-weight:800;font-size:28px;padding:18px 34px;border-radius:999px}
</style></head><body>
<div class="badge">%s</div>
<h1>%s</h1>
<div class="sub">%s</div>
<div class="card %s"><div class="ct"><span>%s</span><span>%s</span></div>%s</div>
<div class="foot"><div class="brand"><div class="logo">N</div><div class="bn">Northlane Studio</div></div><div class="cta">%s</div></div>
</body></html>""" % (
        fonts,
        s.get("sub_top", 560),
        s.get("card_top", 710 if len(s["rows"]) >= 4 else 800),
        html.escape(s["badge"]),
        headline,
        html.escape(s["subline"]),
        "compact" if len(s["rows"]) >= 4 else "",
        html.escape(s["card_title"]),
        html.escape(s.get("label_right", "Sample data")),
        rows,
        html.escape(s["cta"]),
    )


def main():
    spec_file, out_dir = sys.argv[1], sys.argv[2]
    font_dir = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.abspath("fonts")
    os.makedirs(out_dir, exist_ok=True)
    specs = json.load(open(spec_file))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1000, "height": 1500}, device_scale_factor=1)
        for s in specs:
            pg.set_content(build_html(s, font_dir))
            pg.wait_for_timeout(800)
            card = pg.evaluate("(() => { const c=document.querySelector('.card').getBoundingClientRect(); const f=document.querySelector('.foot').getBoundingClientRect(); const h=document.querySelector('h1').getBoundingClientRect(); const sb=document.querySelector('.sub').getBoundingClientRect(); return {cardBottom:c.bottom, footTop:f.top, h1Bottom:h.bottom, subTop:sb.top, subBottom:sb.bottom, cardTop:c.top}; })()")
            gap = card["footTop"] - card["cardBottom"]
            ok = gap >= 40 and card["subBottom"] <= card["cardTop"] - 20 and card["subTop"] >= card["h1Bottom"] - 5
            out = os.path.join(out_dir, "pin-%s.png" % s["id"])
            pg.screenshot(path=out, full_page=False)
            print(s["id"], out, "gap=%d" % gap, "layout_ok=%s" % ok, card)
        b.close()


if __name__ == "__main__":
    main()
