import json, html, os
OUT = "/home/claude/site"
BASE = "https://koerber-stellium.com/our-services/innovation/ai-agents/"
E = html.escape

CSS = r"""
/* Layout: Körber Stellium site chrome (white header, blue hero band, cream sections, black footer); content in a 1200px column with 12-col feel */
:root{
  --blue:#0060FF; --ink:#000000; --paper:#FFFFFF; --cream:#F5F3F1; --sand:#E6E2DC; --pebble:#BFB8AF; --stone:#9D968D;
  --lemon:#FFE32F; --amber:#FEC037; --orange:#FE8623; --green:#00A310;
  --muted:rgba(0,0,0,.68); --line:rgba(0,0,0,.12); --on-blue-muted:rgba(255,255,255,.82);
  --sans:Arial,"Helvetica Neue",Helvetica,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --s1:.8125rem; --s2:1rem; --s3:1.1875rem; --s4:1.5rem; --s5:2rem; --s6:clamp(2rem,4.4vw,3.25rem);
  color-scheme:light;
}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:var(--s2);line-height:1.6;margin:0}
a{color:var(--blue)}
a:focus-visible,button:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
h1,h2,h3{text-wrap:balance;line-height:1.15;margin:0;font-weight:700}
h1{font-size:var(--s6);letter-spacing:-.01em}
h2{font-size:var(--s5);letter-spacing:-.005em}
h3{font-size:var(--s3)}
p{margin:0}
.wrap{max-width:1200px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.eyebrow{font-size:var(--s1);text-transform:uppercase;letter-spacing:.09em;font-weight:700}
.lead{font-size:var(--s3);max-width:60ch}
.measure{max-width:65ch}
section{padding-block:72px}
.cream{background:var(--cream)}
.stack{display:flex;flex-direction:column;gap:16px}
.sec-head{display:flex;flex-direction:column;gap:12px;margin-bottom:40px;max-width:760px}
.sec-head p{color:var(--muted)}

/* review bar */
.review{background:var(--ink);color:var(--paper);font-size:var(--s1)}
.review .wrap{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding-block:10px}
.review b{color:var(--lemon);letter-spacing:.06em;text-transform:uppercase}
.review nav{display:flex;flex-wrap:wrap;gap:4px 16px}
.review a{color:var(--paper);text-decoration:none;opacity:.8}
.review a[aria-current]{opacity:1;text-decoration:underline;text-underline-offset:4px}
.review a:hover{opacity:1}

/* header */
header.site{background:var(--paper);border-bottom:1px solid var(--line);position:sticky;top:env(safe-area-inset-top,0px);z-index:20}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:30;background:var(--ink)}
header.site .wrap{display:flex;align-items:center;gap:32px;padding-block:14px}
.logo img{height:38px;width:auto;display:block}
.mainnav{display:flex;gap:28px;font-size:.95rem;margin-left:auto}
.mainnav a{color:var(--ink);text-decoration:none}
.mainnav a.on{color:var(--blue);font-weight:700}
.mainnav a:hover{color:var(--blue)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 22px;border-radius:999px;font-weight:700;text-decoration:none;font-size:.95rem;border:2px solid transparent;transition:background .15s,color .15s}
.btn-blue{background:var(--blue);color:var(--paper)}
.btn-blue:hover{background:var(--ink)}
.btn-white{background:var(--paper);color:var(--blue)}
.btn-white:hover{background:var(--ink);color:var(--paper)}
.btn-ghost{border-color:var(--paper);color:var(--paper)}
.btn-ghost:hover{background:var(--paper);color:var(--blue)}
@media (max-width:900px){.mainnav{display:none}header.site .btn{margin-left:auto}}

/* breadcrumb */
.crumbs{font-size:var(--s1);padding-block:12px;color:var(--muted)}
.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0}
.crumbs li+li::before{content:"›";margin-right:6px;color:var(--stone)}
.crumbs a{color:var(--muted);text-decoration:none}
.crumbs a:hover{color:var(--blue)}

/* hero */
.hero{background:var(--blue);color:var(--paper);position:relative;overflow:hidden;padding-block:72px 80px}
.hero .wrap{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:48px;align-items:center}
.hero .copy{display:flex;flex-direction:column;gap:20px;min-width:0}
.hero .lead{color:var(--on-blue-muted)}
.hero .ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px}
.rings{position:absolute;right:-140px;top:50%;width:760px;height:440px;transform:translateY(-50%);pointer-events:none}
.rings i{position:absolute;top:0;width:440px;height:440px;border:2px solid rgba(255,255,255,.22);border-radius:50%}
.rings i:first-child{left:0}.rings i:last-child{left:320px}
@media (max-width:900px){.hero .wrap{grid-template-columns:1fr}.rings{right:-380px}}

/* console sample */
.console{background:var(--ink);color:var(--paper);border-radius:14px;padding:20px;font-family:var(--mono);font-size:.8125rem;line-height:1.55;min-width:0;box-shadow:0 24px 60px rgba(0,0,0,.25)}
.console .bar{display:flex;justify-content:space-between;gap:12px;font-family:var(--sans);font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--pebble);margin-bottom:14px}
.console .scroll{overflow-x:auto}
.console pre{margin:0;white-space:pre;font-family:inherit}
.console table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;white-space:nowrap}
.console th{color:var(--pebble);font-weight:400;text-align:left;padding:4px 10px 6px 0;border-bottom:1px solid rgba(255,255,255,.18)}
.console td{padding:6px 10px 6px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.console .note{font-family:var(--sans);font-size:.75rem;color:var(--pebble);margin-top:12px}
.k-esc{color:var(--orange)}.k-rec{color:var(--amber)}.k-ok{color:#5BD36A}.k-hold{color:var(--lemon)}

/* chips */
.chip{display:inline-block;font-family:var(--sans);font-size:.72rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:3px 10px;border-radius:999px;white-space:nowrap}
.c-watch{background:var(--sand);color:var(--ink)}.c-advise{background:var(--lemon);color:var(--ink)}
.c-rec{background:var(--amber);color:var(--ink)}.c-esc{background:var(--orange);color:var(--ink)}
.c-ok{background:var(--green);color:var(--paper)}.c-blue{background:var(--blue);color:var(--paper)}

/* fact strip */
.facts{border-bottom:1px solid var(--line)}
.facts .wrap{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;padding-block:28px}
.facts div{display:flex;flex-direction:column;gap:4px}
.facts b{font-size:var(--s4);color:var(--blue)}
.facts span{color:var(--muted);font-size:.9rem}
@media (max-width:800px){.facts .wrap{grid-template-columns:repeat(2,minmax(0,1fr))}}

/* assistant cards */
.assistants{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.acard{display:flex;flex-direction:column;gap:16px;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:28px;min-width:0}
.acard .sys{display:flex;justify-content:space-between;align-items:center;gap:12px}
.acard .sys strong{font-size:1.75rem;color:var(--blue);letter-spacing:-.01em}
.acard .role{color:var(--muted)}
.acard ul{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.acard li{padding:10px 0;border-bottom:1px solid var(--line);font-size:.95rem}
.acard .more{margin-top:auto;font-weight:700;text-decoration:none}
.acard .more:hover{text-decoration:underline}
@media (max-width:960px){.assistants{grid-template-columns:1fr}}

/* steps */
.steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:0;counter-reset:s;border-top:2px solid var(--ink)}
.steps li{counter-increment:s;padding:18px 18px 0 0;display:flex;flex-direction:column;gap:6px;min-width:0}
.steps li::before{content:counter(s,decimal-leading-zero);font-weight:700;color:var(--blue);font-size:var(--s1);letter-spacing:.08em}
.steps b{font-size:1rem}
.steps span{color:var(--muted);font-size:.9rem}
.steps li.human b{color:var(--blue)}
@media (max-width:960px){.steps{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:24px}}

/* feature grid */
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px}
@media (max-width:900px){.grid4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:700px){.grid2,.grid4{grid-template-columns:1fr}}
.feat{display:flex;flex-direction:column;gap:8px;min-width:0}
.feat p{color:var(--muted)}
.feat .ico{width:44px;height:44px;border-radius:50%;border:2px solid var(--blue);display:grid;place-items:center;color:var(--blue);font-weight:700}

/* agent cards (detail pages) */
.agent{background:var(--paper);border-radius:16px;padding:28px;display:flex;flex-direction:column;gap:14px;min-width:0;border:1px solid var(--line)}
.agent .top{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap}
.agent dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:6px 16px;font-size:.92rem}
.agent dt{color:var(--muted);text-transform:uppercase;font-size:.72rem;letter-spacing:.07em;padding-top:3px;font-weight:700}
.agent dd{margin:0;min-width:0}
.agent code,.tbl code{font-family:var(--mono);font-size:.82rem;background:var(--cream);padding:1px 6px;border-radius:4px;overflow-wrap:anywhere}

/* tables */
.tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--paper)}
.tbl{border-collapse:collapse;width:100%;font-size:.93rem;font-variant-numeric:tabular-nums}
.tbl th{text-align:left;background:var(--cream);font-size:.75rem;text-transform:uppercase;letter-spacing:.07em;padding:12px 16px;border-bottom:1px solid var(--line)}
.tbl td{padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr:last-child td{border-bottom:0}
.tbl td:first-child{font-weight:700}

/* guardrail list */
.guards{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px}
.guards li{padding:16px 0 16px 36px;border-bottom:1px solid var(--line);position:relative}
.guards li::before{content:"";position:absolute;left:0;top:19px;width:20px;height:20px;border-radius:50%;border:2px solid var(--blue)}
.guards li::after{content:"";position:absolute;left:7px;top:23px;width:5px;height:9px;border:solid var(--blue);border-width:0 2px 2px 0;transform:rotate(45deg)}
@media (max-width:700px){.guards{grid-template-columns:1fr}}

/* faq */
.faq{border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;padding:20px 40px 20px 0;font-weight:700;font-size:1.05rem;list-style:none;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:4px;top:16px;font-size:1.5rem;color:var(--blue)}
.faq details[open] summary::after{content:"–"}
.faq details p{padding:0 0 20px;color:var(--muted);max-width:70ch}

/* related + cta */
.related{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.related a{display:flex;flex-direction:column;gap:6px;padding:24px;border-radius:16px;background:var(--paper);border:1px solid var(--line);text-decoration:none;color:var(--ink)}
.related a:hover{border-color:var(--blue)}
.related a span{color:var(--blue);font-weight:700;font-size:var(--s1);text-transform:uppercase;letter-spacing:.07em}
@media (max-width:700px){.related{grid-template-columns:1fr}}
.talk{background:var(--blue);color:var(--paper)}
.talk .wrap{display:flex;flex-wrap:wrap;gap:24px;align-items:center;justify-content:space-between}
.talk p{color:var(--on-blue-muted);max-width:56ch;margin-top:10px}

/* footer */
footer{background:var(--ink);color:var(--paper);font-size:.9rem}
footer .wrap{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.4fr;gap:32px;padding-block:56px 32px}
footer h4{margin:0 0 12px;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--pebble)}
footer ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
footer a{color:var(--paper);text-decoration:none}
footer a:hover{text-decoration:underline}
footer .logo img{height:34px}
footer .legal{grid-column:1/-1;border-top:1px solid rgba(255,255,255,.18);padding-top:20px;color:var(--pebble);font-size:.8rem}
@media (max-width:800px){footer .wrap{grid-template-columns:1fr 1fr}}

/* placement page */
.tree{font-size:.95rem;line-height:1.9;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:24px;overflow-x:auto}
.tree ul{list-style:none;margin:0;padding-left:22px;border-left:1px dashed var(--pebble)}
.tree>ul{border-left:0;padding-left:0}
.tree li{white-space:nowrap}
.tree .new{background:var(--blue);color:var(--paper);padding:2px 10px;border-radius:6px;font-weight:700}
.tree .touch{border-bottom:2px solid var(--amber)}
.legend{display:flex;flex-wrap:wrap;gap:16px;font-size:var(--s1);color:var(--muted);margin-top:12px}
.serp{border:1px solid var(--line);border-radius:12px;padding:16px 20px;background:var(--paper);display:flex;flex-direction:column;gap:2px;min-width:0}
.serp .u{font-size:.8rem;color:var(--muted);overflow-wrap:anywhere}
.serp .t{color:#1a0dab;font-size:1.1rem;font-family:Arial,sans-serif}
.serp .d{font-size:.88rem;color:var(--muted)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap">'

PAGES = [("index.html","AI Agents hub"),("ewm-outbound-supervisor-agent.html","EWM Outbound Supervisor"),
         ("tm-invoice-dispute-agent.html","TM Invoice Dispute"),("dm-order-release-agent.html","DM Order Release"),
         ("placement-plan.html","Placement & SEO plan")]

def review(cur):
    links = "".join(f'<a href="{f}"{" aria-current=\"page\"" if f==cur else ""}>{E(n)}</a>' for f,n in PAGES)
    return f'<div class="review"><div class="wrap"><b>Preview for review</b><span>Not live · proposed pages for koerber-stellium.com</span><nav aria-label="Preview pages">{links}</nav></div></div>'

def header():
    return '''<header class="site"><div class="wrap">
<a class="logo" href="index.html" aria-label="Körber Stellium home"><img src="logo-black.png" alt="Körber Stellium" width="180" height="38"></a>
<nav class="mainnav" aria-label="Main"><a href="https://koerber-stellium.com/who-is-korber-stellium/">About us</a><a class="on" href="https://koerber-stellium.com/our-services/">Services</a><a href="https://koerber-stellium.com/our-solutions/">Solutions</a><a href="https://koerber-stellium.com/insights-events/">Insights &amp; events</a><a href="https://koerber-stellium.com/careers-at-stellium/">Careers</a></nav>
<a class="btn btn-blue" href="https://koerber-stellium.com/contact-us/">Request a Demo</a>
</div></header>'''

def crumbs(items):
    lis = "".join(f'<li>{"<a href=%s>%s</a>" % (json.dumps(h), E(n)) if h else "<span aria-current=page>"+E(n)+"</span>"}</li>' for n,h in items)
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

def footer():
    return '''<footer><div class="wrap">
<div class="stack"><a class="logo" href="index.html"><img src="logo-white.png" alt="Körber Stellium" width="160" height="34"></a><p style="color:var(--pebble);max-width:34ch">The trusted leader in digital transformation for SAP supply chain execution.</p></div>
<div><h4>Quick links</h4><ul><li><a href="https://koerber-stellium.com/who-is-korber-stellium/">Who is Körber Stellium</a></li><li><a href="https://koerber-stellium.com/stellium-give/">Körber Stellium GIVE</a></li><li><a href="https://koerber-stellium.com/careers-at-stellium/">Careers</a></li><li><a href="https://koerber-stellium.com/insights-events/">Insights &amp; events</a></li></ul></div>
<div><h4>AI agents</h4><ul><li><a href="ewm-outbound-supervisor-agent.html">SAP EWM Outbound Supervisor</a></li><li><a href="tm-invoice-dispute-agent.html">SAP TM Invoice Dispute</a></li><li><a href="dm-order-release-agent.html">SAP DM Order Release</a></li><li><a href="https://koerber-stellium.com/faq/">FAQs</a></li></ul></div>
<div><h4>Offices</h4><ul><li>Bengaluru, India</li><li>Houston, TX, USA</li><li>Markham, ON, Canada</li><li>Dubai, UAE</li></ul></div>
<p class="legal">© 2026 Körber Stellium. All rights reserved. · Preview build for internal approval.</p>
</div></footer>'''

def talk(text):
    return f'''<section class="talk"><div class="wrap"><div><h2>Talk to us</h2><p>{text}</p></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-white" href="https://koerber-stellium.com/contact-us/">Request a demo</a><a class="btn btn-ghost" href="placement-plan.html">View placement plan</a></div></div></section>'''

def faq_html(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faqs) + '</div>'

def jsonld(objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in objs)

def faq_ld(faqs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def crumb_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}

CR = [("Home","https://koerber-stellium.com/"),("Services","https://koerber-stellium.com/our-services/"),
      ("Innovation","https://koerber-stellium.com/our-services/innovation/"),("AI Agents",BASE)]

def meta(title, desc, canon, kw, img="ewm-outbound-supervisor"):
    return f'''<title>{E(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{E(desc)}">
<meta name="keywords" content="{E(kw)}">
<meta name="robots" content="noindex, nofollow"><!-- preview only: switch to "index, follow" on koerber-stellium.com -->
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Körber Stellium">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="https://koerber-stellium.com/wp-content/uploads/ai-agents/{img}.jpg"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="720"><meta property="og:image:alt" content="{E(title)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://koerber-stellium.com/wp-content/uploads/ai-agents/{img}.jpg"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}">
{FONTS}<link rel="stylesheet" href="styles.css">'''

def page(fname, head, body, full=True):
    if full:
        doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{head}</head><body>{body}</body></html>'
    else:
        doc = head + body  # index: skeleton supplies html/head/body
    open(os.path.join(OUT,fname),"w").write(doc)

VIDEOS = {
 "ewm-outbound-supervisor-agent.html":("ewm-outbound-supervisor","SAP EWM Outbound Supervisor AI Agent in action","How the outbound supervisor assistant answers one question across waves, queues and labor in SAP EWM.","PT35S"),
 "tm-invoice-dispute-agent.html":("tm-dispute-agent","SAP TM Carrier Invoice Dispute AI Agent in action","How the dispute assistant checks carrier invoices against the agreed freight cost in SAP TM and decides the next step.","PT35S"),
 "dm-order-release-agent.html":("dm-order-release-agent","SAP DM Order Release AI Agent in action","How the order release assistant decides which SAP Digital Manufacturing orders to release next.","PT30S"),
}
MEDIA = "https://koerber-stellium.com/wp-content/uploads/ai-agents/"
LINKEDIN = {"ewm-outbound-supervisor-agent.html":"https://www.linkedin.com/posts/koerber-stellium_outbound-ai-sapewm-activity-7511827923889209345-TGrz"}
def video_ld(fname):
    f,n,d,dur = VIDEOS[fname]
    return {"@context":"https://schema.org","@type":"VideoObject","name":n,"description":d,"thumbnailUrl":MEDIA+f+".jpg","contentUrl":MEDIA+f+".mp4","uploadDate":"2026-10-21","duration":dur,"publisher":{"@type":"Organization","name":"Körber Stellium"}}
def video_tag(fname, pre="metadata"):
    f,n,d,dur = VIDEOS[fname]
    li = LINKEDIN.get(fname)
    lk = f' <a class="li" href="{li}" target="_blank" rel="noopener">See the post on LinkedIn ↗</a>' if li else ""
    return f'<figure class="vid"><video controls playsinline preload="{pre}" poster="media/{f}.jpg" aria-label="{E(n)}"><source src="media/{f}.mp4" type="video/mp4"></video><figcaption>{E(d)}{lk}</figcaption></figure>'

# ---------------- HUB ----------------
hub_faqs = [
 ("What are Körber Stellium AI agents?","They are AI assistants that work inside your SAP execution systems. Each one reads live data from SAP EWM, SAP TM or SAP Digital Manufacturing, applies your business rules, and hands your team a ranked recommendation or a ready-to-approve action."),
 ("Which SAP systems do the agents connect to?","SAP Extended Warehouse Management (EWM), SAP Transportation Management (TM) and SAP Digital Manufacturing (DM), on S/4HANA and SAP cloud tenants, through the Körber Stellium SAP Connector and SAP DM APIs."),
 ("How do recommendations reach my team?","As Action Tickets with the finding, the impact, the recommended step and the SAP transaction or Fiori app to use. Tickets can be posted to a Microsoft Teams channel, where a flow creates Planner tasks automatically."),
 ("How long does it take to get started?","A typical pilot starts with one assistant, one site and read-only access. Talk to us about an assessment of your EWM, TM or DM landscape to scope it."),
]
hub_head = meta("AI Agents for SAP EWM, TM & DM | Körber Stellium",
 "AI agents for SAP EWM outbound supervision, SAP TM freight invoice disputes and SAP DM order release. Live SAP data, clear recommendations, human approval.",
 BASE, "SAP AI agents, SAP EWM AI, SAP TM invoice dispute automation, SAP Digital Manufacturing order release, supply chain AI agents")
hub_head += jsonld([crumb_ld(CR), faq_ld(hub_faqs),
 {"@context":"https://schema.org","@type":"ItemList","name":"Körber Stellium AI agents for SAP","itemListElement":[
  {"@type":"ListItem","position":1,"url":BASE+"sap-ewm-outbound-supervisor-agent/","name":"SAP EWM Outbound Supervisor AI Agent"},
  {"@type":"ListItem","position":2,"url":BASE+"sap-tm-freight-invoice-dispute-agent/","name":"SAP TM Freight Invoice Dispute AI Agent"},
  {"@type":"ListItem","position":3,"url":BASE+"sap-dm-order-release-agent/","name":"SAP DM Order Release AI Agent"}]}])

def acard(sys, chip, name, role, agents, href):
    lis = "".join(f"<li>{E(a)}</li>" for a in agents)
    return f'''<article class="acard"><div class="sys"><strong>{sys}</strong><span class="chip c-blue">{chip}</span></div>
<h3>{E(name)}</h3><p class="role">{E(role)}</p><ul>{lis}</ul><a class="more" href="{href}">Explore the {sys} assistant →</a></article>'''

hub_body = review("index.html") + header() + crumbs([("Home","https://koerber-stellium.com/"),("Services","https://koerber-stellium.com/our-services/"),("Innovation","https://koerber-stellium.com/our-services/innovation/"),("AI Agents",None)]) + f'''
<main>
<section class="hero"><div class="rings" aria-hidden="true"><i></i><i></i></div><div class="wrap">
<div class="copy"><p class="eyebrow">Innovation · AI agents for SAP</p>
<h1>AI agents that run supply chain decisions with your team</h1>
<p class="lead">Three assistants for SAP EWM, SAP TM and SAP Digital Manufacturing. They read live SAP data, apply your rules and bring your supervisors a clear next step. People stay in charge of every change.</p>
<div class="ctas"><a class="btn btn-white" href="https://koerber-stellium.com/contact-us/">Request a demo</a><a class="btn btn-ghost" href="#assistants">Meet the assistants</a></div></div>
<div class="console" role="img" aria-label="Example of an agent decision loop">
<div class="bar"><span>Agent loop</span><span>every cycle</span></div>
<pre>observe    live SAP EWM · TM · DM data
understand business rules + thresholds
predict    cutoff · dispute · capacity risk
recommend  <span class="k-rec">Action Ticket</span>
approve    <span class="k-ok">supervisor, in chat or Teams</span>
execute    SAP app / transaction · verify</pre>
<p class="note">The same loop powers all three assistants.</p></div>
</div></section>

<div class="facts"><div class="wrap">
<div><b>3</b><span>assistants, one per SAP execution system</span></div>
<div><b>12</b><span>specialist agents working underneath</span></div>
<div><b>100%</b><span>of figures traced to a live SAP query</span></div>
</div></div>

<section id="assistants" class="cream"><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">The assistants</p><h2>One assistant for each SAP execution system</h2><p>Each assistant is a team of specialist agents. It works the way your supervisor already works, in the same SAP objects, transactions and Fiori apps.</p></div>
<div class="assistants">
{acard("EWM","Warehouse","Warehouse Outbound Supervisor","Protects the ship schedule across waves, pick, pack, stage and load.",["Wave Throughput & Cutoff agent","Bottleneck Prediction agent","Labor & Resource Balancing agent","Exception Management agent"],"ewm-outbound-supervisor-agent.html")}
{acard("TM","Freight","Carrier Invoice Dispute Resolution","Checks every carrier invoice against the Freight Settlement Document and resolves disputes.",["Invoice Match & Classify agent","Tolerance Approval agent","Carrier Counter-mail agent","Fuel-price Check & Escalation agent"],"tm-invoice-dispute-agent.html")}
{acard("DM","Manufacturing","Order Release & Dispatch","Decides which production orders to release next, so the shop floor never starves or floods.",["Candidate Screening agent","Material Availability agent","Load & WIP Capacity agent","Rank & Release agent"],"dm-order-release-agent.html")}
</div></div></section>

<section><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">See them in action</p><h2>Three short films, one per assistant</h2><p>Each runs about 30 seconds.</p></div>
<div class="vidgrid">{"".join(f'<div class="stack" style="gap:10px;min-width:0"><h3>{t}</h3>{video_tag(k,"none")}</div>' for k,t in [("ewm-outbound-supervisor-agent.html","SAP EWM Outbound Supervisor"),("tm-invoice-dispute-agent.html","SAP TM Invoice Dispute"),("dm-order-release-agent.html","SAP DM Order Release")])}</div>
</div></section>
<section class="cream"><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">How it works</p><h2>From live SAP data to an approved action</h2><p>Every assistant follows the same six steps. The agent does the first four. Your team owns the decision.</p></div>
<ol class="steps">
<li><b>Connect</b><span>Health check and secure login to SAP before any number is reported.</span></li>
<li><b>Read</b><span>Targeted queries on live SAP objects. No full-table scans.</span></li>
<li><b>Classify</b><span>Your business rules, thresholds and tolerances applied consistently.</span></li>
<li><b>Recommend</b><span>An Action Ticket: finding, impact, fix and where to execute it.</span></li>
<li class="human"><b>Approve</b><span>A supervisor approves in chat or in Microsoft Teams.</span></li>
<li><b>Execute &amp; verify</b><span>The change is made in SAP and read back to confirm it.</span></li>
</ol></div></section>

<section><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">Built for control</p><h2>Your team stays in control</h2></div>
<ul class="guards">
<li><b>Read-only by default.</b> Agents look and recommend. Nothing changes in SAP until your team approves it.</li>
<li><b>No invented numbers.</b> Every metric comes from an SAP query in that session. Gaps are stated plainly.</li>
<li><b>Severity you can act on.</b> Watch, Advise, Recommend and Escalate tiers match how a shift is run.</li>
<li><b>Fits your tools.</b> Action Tickets post to Microsoft Teams and become Planner tasks automatically.</li>
<li><b>One click into SAP.</b> Findings link straight to the Fiori app or transaction to fix them.</li>
<li><b>Your rules, your thresholds.</b> SLAs, tolerances and capacity limits are configurable per site.</li>
</ul></div></section>

<section class="cream"><div class="wrap grid2" style="align-items:start">
<div class="sec-head" style="margin:0"><p class="eyebrow" style="color:var(--blue)">FAQ</p><h2>Questions about AI agents for SAP</h2><p>More answers on our <a href="https://koerber-stellium.com/faq/">FAQ page</a>, or see our <a href="https://koerber-stellium.com/our-services/sap-services/sap-business-ai/">SAP Business AI</a> and <a href="https://koerber-stellium.com/our-services/innovation/enterprise-ai/">Enterprise AI</a> services.</p></div>
{faq_html(hub_faqs)}
</div></section>
</main>
''' + talk("See an assistant run against your own SAP EWM, TM or DM data. We start with a read-only pilot on one site.") + footer()
page("index.html", hub_head, hub_body, full=False)

# ---------------- DETAIL TEMPLATE ----------------
def detail(fname, slug, title, desc, kw, crumbname, eyebrow, h1, lead, console, problem_h, problem, agents_h, agents, rules_h, rules_intro, rules_table, outputs, guards, faqs, related, talktext, app_name, app_desc):
    canon = BASE + slug + "/"
    head = meta(title, desc, canon, kw, VIDEOS[fname][0]) + jsonld([crumb_ld(CR+[(crumbname, canon)]), faq_ld(faqs), video_ld(fname),
      {"@context":"https://schema.org","@type":"SoftwareApplication","name":app_name,"applicationCategory":"BusinessApplication",
       "operatingSystem":"SAP S/4HANA, SAP BTP","description":app_desc,"url":canon,
       "provider":{"@type":"Organization","name":"Körber Stellium","url":"https://koerber-stellium.com/"}}])
    acards = "".join(f'''<article class="agent"><div class="top"><h3>{E(n)}</h3><span class="chip {c}">{E(t)}</span></div><p>{E(d)}</p>
<dl><dt>Reads</dt><dd>{r}</dd><dt>Delivers</dt><dd>{E(o)}</dd></dl></article>''' for n,t,c,d,r,o in agents)
    outs = "".join(f'<div class="feat"><div class="ico" aria-hidden="true">{i+1}</div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for i,(a,b) in enumerate(outputs))
    gl = "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a,b in guards)
    rel = "".join(f'<a href="{h}"><span>{E(s)}</span><b>{E(n)}</b><p style="color:var(--muted)">{E(d)}</p></a>' for s,n,d,h in related)
    body = review(fname) + header() + crumbs([("Home","https://koerber-stellium.com/"),("Services","https://koerber-stellium.com/our-services/"),("Innovation","https://koerber-stellium.com/our-services/innovation/"),("AI Agents","index.html"),(crumbname,None)]) + f'''
<main>
<section class="hero"><div class="rings" aria-hidden="true"><i></i><i></i></div><div class="wrap">
<div class="copy"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p>
<div class="ctas"><a class="btn btn-white" href="https://koerber-stellium.com/contact-us/">Request a demo</a><a class="btn btn-ghost" href="#agents">See the agents</a></div></div>
{console}
</div></section>
<section class="vidsec"><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">See it in action</p><h2>Watch the assistant work</h2></div>
{video_tag(fname)}</div></section>
<section class="cream"><div class="wrap grid2" style="align-items:start;gap:48px">
<div class="sec-head" style="margin:0"><p class="eyebrow" style="color:var(--blue)">The challenge</p><h2>{problem_h}</h2></div>
<div class="stack measure">{problem}</div></div></section>
<section id="agents"><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">Meet the agents</p><h2>{agents_h}</h2></div>
<div class="grid2">{acards}</div></div></section>
<section><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">Business rules</p><h2>{rules_h}</h2><p>{rules_intro}</p></div>
<div class="tblwrap">{rules_table}</div></div></section>
<section class="cream"><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">What your team gets</p><h2>Outputs built for the shift, not for a binder</h2></div>
<div class="grid4">{outs}</div></div></section>
<section><div class="wrap">
<div class="sec-head"><p class="eyebrow" style="color:var(--blue)">Guardrails</p><h2>Safe to run on production SAP</h2></div>
<ul class="guards">{gl}</ul></div></section>
<section class="cream"><div class="wrap grid2" style="align-items:start">
<div class="sec-head" style="margin:0"><p class="eyebrow" style="color:var(--blue)">FAQ</p><h2>Frequently asked questions</h2></div>
{faq_html(faqs)}</div></section>
<section><div class="wrap"><div class="sec-head"><p class="eyebrow" style="color:var(--blue)">Related</p><h2>More AI agents for SAP</h2></div><div class="related">{rel}</div></div></section>
</main>''' + talk(talktext) + footer()
    page(fname, head, body)

def tbl(heads, rows):
    th = "".join(f"<th>{h}</th>" for h in heads)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

REL = {
 "ewm":("SAP EWM","Warehouse Outbound Supervisor","Wave throughput, bottlenecks, labor and exceptions in one sweep.","ewm-outbound-supervisor-agent.html"),
 "tm":("SAP TM","Carrier Invoice Dispute Resolution","Match, approve, negotiate and escalate freight invoice disputes.","tm-invoice-dispute-agent.html"),
 "dm":("SAP DM","Order Release & Dispatch","Release the right production orders, with material and capacity checked.","dm-order-release-agent.html"),
}

# ---------------- EWM ----------------
ewm_console = '''<div class="console" role="img" aria-label="Example Action Ticket raised by the EWM agent">
<div class="bar"><span>Action Ticket · example</span><span class="k-esc">Escalate</span></div>
<div class="scroll"><pre>ACTION TICKET  AT-014             <span class="k-esc">Escalate</span>
Finding    : Wave 4100023 at 61% complete,
             40 min to cutoff
Impact     : 18 deliveries miss the 16:30
             carrier pickup
Recommend  : Move 3 pickers from replenishment
             to pick area B, split wave
Execute in : EWM Warehouse Monitor
Raised     : 14:52   Status: <span class="k-rec">OPEN</span></pre></div>
<p class="note">Illustrative ticket. Format matches the live agent.</p></div>'''
detail("ewm-outbound-supervisor-agent.html","sap-ewm-outbound-supervisor-agent",
 "SAP EWM AI Agent for Outbound Supervisors | Körber Stellium",
 "AI agent for SAP EWM outbound: wave throughput, cutoff risk, bottlenecks, labor balancing and exceptions, with Action Tickets in Microsoft Teams.",
 "SAP EWM AI agent, warehouse outbound supervisor, wave cutoff risk, warehouse bottleneck prediction, labor balancing SAP EWM, OTIF exceptions",
 "EWM Outbound Supervisor","SAP EWM · Warehouse outbound",
 "The AI outbound supervisor for SAP EWM",
 "Four agents sweep your waves, tasks, bins, labor and deliveries in minutes. Your shift lead gets one headline: will we hit cutoff today, and what to do if not.",
 ewm_console,
 "Outbound problems show up late, when the truck is already at the dock",
 "<p>Supervisors juggle wave monitors, task queues and delivery lists across several screens. A bottleneck that is easy to fix at 60% of the shift turns into a missed carrier at 95%.</p><p>The Warehouse Outbound Supervisor assistant watches the whole outbound flow in SAP EWM. It sees problems early, ranks them by severity and recommends a specific fix, naming the wave, area or resource and the EWM app to use.</p>",
 "Four specialist agents, one shift handover",
 [("Wave Throughput & Cutoff","Agent 1","c-blue","Tracks every wave in flight against plan and flags the ones at risk of missing cutoff.","Wave progress and outbound deliveries","% complete per wave, cutoff-ordered, with risk tier"),
  ("Bottleneck Prediction","Agent 2","c-blue","Spots task aging, storage congestion and queue build-up before they stop a wave.","Open warehouse tasks and storage bins","Top 3 bottlenecks by area or storage type"),
  ("Labor & Resource Balancing","Agent 3","c-blue","Compares actual pace with target by queue and activity area to show where to move people.","Confirmed tasks and warehouse orders","Over- and under-staffed areas, efficiency vs target"),
  ("Exception Management","Agent 4","c-blue","Triages delayed shipments, short picks and blocked deliveries, and finds the root cause.","Outbound deliveries and pick exceptions","Exceptions by severity, with a Fiori link to each delivery")],
 "Severity tiers that match how a shift is run",
 "Every finding gets one of four tiers. Recommend and Escalate findings always become an Action Ticket. Thresholds are regional-DC defaults and adopt your site's SLAs.",
 tbl(["Tier","Meaning","What the agent does"],[
  ['<span class="chip c-watch">Watch</span>',"Normal variance","Notes it and keeps monitoring"],
  ['<span class="chip c-advise">Advise</span>',"Worth attention this shift","Surfaces it with a specific fix"],
  ['<span class="chip c-rec">Recommend</span>',"Needs a decision soon","Raises an Action Ticket"],
  ['<span class="chip c-esc">Escalate</span>',"Time-critical or customer-impacting","Surfaces it immediately with an Action Ticket"]]),
 [("Shift handover","Six sections: headline, throughput, bottlenecks, labor, exceptions and open tickets. Read standing up at the huddle."),
  ("Action Tickets","Finding, impact, recommendation, where to execute and age. Carried forward across the shift."),
  ("Charts","Wave progress, queue depth, rate vs target and exception counts. Shape before digits."),
  ("Teams & Planner","Tickets post to a Teams channel as cards and become Planner tasks automatically.")],
 [("Read-only. No exceptions.","The agent identifies and recommends. It never releases a wave, reassigns a task or touches a delivery."),
  ("Every number traced.","Each metric comes from a live query in that session. Failed queries are reported, never filled in."),
  ("Unpopulated fields are called out.","A blank field means missing data, not an idle team or an empty warehouse."),
  ("Customer data stays minimal.","Names and addresses are pulled only for delayed or exception rows."),
  ("No guesswork on status.","Statuses are reported as SAP shows them, never assumed."),
  ("Efficient by design.","A full sweep is about eight targeted queries, so it can run every 15 to 30 minutes.")],
 [("What does the SAP EWM outbound AI agent monitor?","Wave progress against cutoff, open task aging and bin congestion, labor pace against target by area, and outbound delivery exceptions such as delayed shipments and short picks."),
  ("Can the agent release or change waves in SAP EWM?","No. It is read-only. It recommends a specific change and names the EWM app or transaction, and your supervisor makes the change."),
  ("How often does it run?","On demand when a supervisor asks, and on a standing 15 to 30 minute cadence during active wave execution, with a full handover at shift change."),
  ("Where do the Action Tickets go?","They appear in the handover report and can be posted to a Microsoft Teams channel, where a Power Automate flow turns them into Planner tasks.")],
 [REL["tm"],REL["dm"]],
 "See the outbound supervisor run a live sweep on your SAP EWM warehouse.",
 "Körber Stellium SAP EWM Outbound Supervisor AI Agent",
 "AI agent that monitors SAP EWM outbound wave throughput, bottlenecks, labor and exceptions and raises Action Tickets.")

# ---------------- TM ----------------
tm_console = '''<div class="console" role="img" aria-label="Example dispute classification by the TM agent">
<div class="bar"><span>Dispute run · example</span><span>last 30 days</span></div>
<div class="scroll"><table><thead><tr><th>Invoice</th><th>Diff</th><th>Class</th><th>Action</th></tr></thead><tbody>
<tr><td>INV-2270</td><td>0.0%</td><td class="k-ok">Case 1</td><td>Clean</td></tr>
<tr><td>INV-2268</td><td>+1.8%</td><td class="k-ok">Case 2</td><td>Approve</td></tr>
<tr><td>INV-2265</td><td>+19.6%</td><td class="k-esc">Case 3</td><td>Counter-mail · round 1</td></tr>
<tr><td>INV-2261</td><td>+3.1%</td><td class="k-hold">Gap</td><td>Human review</td></tr>
</tbody></table></div>
<p class="note">Illustrative data. Classes follow the agent's business rules.</p></div>'''
detail("tm-invoice-dispute-agent.html","sap-tm-freight-invoice-dispute-agent",
 "SAP TM Freight Invoice Dispute AI Agent | Körber Stellium",
 "AI agent for SAP TM freight settlement: matches carrier invoices to the FSD, approves tolerance cases, counter-mails carriers and escalates.",
 "SAP TM invoice dispute, freight invoice audit, carrier invoice dispute automation, freight settlement document, fuel surcharge check, SAP TM AI agent",
 "TM Invoice Dispute","SAP TM · Freight settlement",
 "Resolve carrier invoice disputes in SAP TM, case by case",
 "The agent checks every carrier invoice against the Freight Settlement Document, approves what is within tolerance, writes to carriers about what is not, and escalates what stays open.",
 tm_console,
 "Freight audit teams spend their week on disputes that follow the same rules",
 "<p>Most carrier invoice disputes in SAP TM fall into a few patterns: a clean match, a small difference SAP already accepted within tolerance, or an overcharge that needs a conversation with the carrier.</p><p>The Carrier Invoice Dispute assistant applies those patterns consistently. It reads dispute cases, charge lines and tolerance logs in SAP TM, checks fuel surcharges against public diesel prices, and keeps every carrier conversation to a short, fixed format.</p>",
 "Four specialist agents, one dispute workflow",
 [("Invoice Match & Classify","Agent 1","c-blue","Compares each carrier invoice with its FSD and sorts it into Case 1, 2, 3 or the review gap.","Settlement documents and dispute cases in SAP TM","Case class with total and per-charge-line differences"),
  ("Tolerance Approval","Agent 2","c-blue","Approves disputes SAP already passed in its tolerance check, with the agreed reason.","Disputes SAP already accepted within tolerance","Approved case in the Freight Settlement Dispute Case app, verified"),
  ("Carrier Counter-mail","Agent 3","c-blue","Writes to the carrier about disputed lines, differences and the amount you will accept. Two rounds maximum.","Disputed charge lines, carrier email from the business partner","Short, fixed-format counter-mail per case"),
  ("Fuel-price Check & Escalation","Agent 4","c-blue","Validates fuel surcharges against the U.S. EIA diesel average and escalates unresolved cases to people.","EIA weekly diesel prices, tolerance check log","Reasonable fuel amount and an escalation with full history")],
 "Three business cases, applied the same way every time",
 "The agent looks at how SAP TM rated the dispute and how large the difference is. The 5% threshold is configurable.",
 tbl(["Case","Condition","Agent action"],[
  ['<span class="chip c-ok">Case 1</span>',"Invoice matches the FSD exactly, no dispute case","Reports it as clean"],
  ['<span class="chip c-ok">Case 2</span>',"Mismatch, but SAP already accepted it within tolerance","Approves the dispute after your confirmation"],
  ['<span class="chip c-esc">Case 3</span>',"New dispute, difference above 5%","Counter-mails the carrier, adds a fuel check if needed, escalates after round 2"],
  ['<span class="chip c-advise">Gap</span>',"New dispute, difference of 5% or less","Flags it for human review, no email"],
  ['<span class="chip c-watch">Skip</span>',"A person or the carrier already acted, or the case is canceled","Reports only"]]),
 [("Dispute report","One table: case, invoice, expected, billed, difference, status, class, action, mail round and recipient."),
  ("Carrier counter-mails","A short fixed layout with the disputed lines, the amount to accept and the round number."),
  ("Fuel evidence","The latest EIA diesel price, week-on-week change and the reasonable surcharge, with the source cited."),
  ("Escalations","After two rounds, the case goes to your team with amounts, both mail dates and the tolerance log.")],
 [("Asks before acting.","Every SAP approval and every carrier email is confirmed by a person in a live session."),
  ("Recipient read fresh from SAP.","The carrier email comes from the business partner record at send time. Never guessed or reused."),
  ("Two rounds, then people.","The agent never sends a third mail. It escalates with the full history."),
  ("Checks before every send.","If the carrier has already responded in SAP, the mail is not sent."),
  ("Verifies every write.","After an approval, the agent re-reads SAP to confirm the status changed."),
  ("Transparent evidence.","Fuel prices come from public U.S. EIA data, cited in the mail.")],
 [("What is a freight invoice dispute in SAP TM?","When a carrier invoice differs from the Freight Settlement Document, SAP TM opens a dispute case showing the overall difference and the difference per charge. The agent reads both to decide the next step."),
  ("Does the agent approve disputes automatically?","It prepares approvals for disputes SAP already passed in its tolerance check and asks you to confirm before it approves them in the Fiori app. Scheduled runs stop before any write unless you have given standing approval."),
  ("How does the fuel surcharge check work?","It takes the latest weekly U.S. on-highway diesel average from the EIA and scales the FSD fuel amount by the change in diesel price. A flat or falling diesel price never justifies an increase."),
  ("What happens if a carrier does not respond?","The agent sends at most two rounds, at least two business days apart, then escalates the case to your freight settlement team.")],
 [REL["ewm"],REL["dm"]],
 "See the dispute agent work through last month's carrier invoices in your SAP TM system.",
 "Körber Stellium SAP TM Freight Invoice Dispute AI Agent",
 "AI agent that classifies SAP TM carrier invoice disputes, approves tolerance cases, counter-mails carriers and escalates.")

# ---------------- DM ----------------
dm_console = '''<div class="console" role="img" aria-label="Example release cycle by the DM agent">
<div class="bar"><span>Release cycle · example</span><span>recommend mode</span></div>
<div class="scroll"><table><thead><tr><th>Order</th><th>Due</th><th>Decision</th><th>Reason</th></tr></thead><tbody>
<tr><td>1000417</td><td>Oct 21</td><td class="k-ok">RELEASE</td><td>Full qty · batch FIFO</td></tr>
<tr><td>1000422</td><td>Oct 21</td><td class="k-hold">HELD</td><td>Material short 12 kg</td></tr>
<tr><td>1000425</td><td>Oct 22</td><td class="k-hold">HELD</td><td>Assembly at 91%</td></tr>
<tr><td>1000431</td><td>Oct 23</td><td class="k-rec">NEXT</td><td>Cycle cap reached</td></tr>
</tbody></table></div>
<p class="note">Illustrative data. Decisions follow the agent's release rules.</p></div>'''
detail("dm-order-release-agent.html","sap-dm-order-release-agent",
 "SAP DM Order Release AI Agent | Körber Stellium",
 "AI agent for SAP Digital Manufacturing: checks material, load and WIP, then recommends or releases the next best production orders.",
 "SAP Digital Manufacturing order release, SAP DM AI agent, production order dispatch, MES order release automation, WIP capacity check",
 "DM Order Release","SAP Digital Manufacturing · Order release",
 "Release the right production orders in SAP DM, every cycle",
 "The agent checks material, work-center load and work in progress before any order reaches the shop floor. It recommends the next best orders, or releases them once a supervisor approves.",
 dm_console,
 "Releasing by due date alone starves some lines and floods others",
 "<p>Planners release orders that look urgent, only to find a component is short or the work center is already full. Meanwhile, old test orders and stale work in progress cloud the picture.</p><p>The Order Release & Dispatch assistant runs a full release cycle in SAP Digital Manufacturing. It allocates stock from a shared pool so two orders never count the same kilogram, checks load against capacity, and ignores stale WIP that would distort the numbers.</p>",
 "Four specialist agents, one release decision",
 [("Candidate Screening","Agent 1","c-blue","Finds unreleased orders due in the release window and separates out data errors and long-overdue orders.","Open production orders in SAP DM","Candidate list, with stale and data-error orders set aside for cleanup"),
  ("Material Availability","Agent 2","c-blue","Checks every component against available inventory, oldest batch first.","Bills of material and live inventory","Shortfalls by material and the batches each order will use"),
  ("Load & WIP Capacity","Agent 3","c-blue","Adds setup and machine time to each work center and counts only recent work in progress.","Planned run times and work in progress","Load per work center as % of capacity"),
  ("Rank & Release","Agent 4","c-blue","Ranks by due date, priority and size, then releases full or partial quantities that fit.","Results of agents 1 to 3","Decision table and the exact release request")],
 "Clear decisions with configurable limits",
 "Every candidate gets one decision. Defaults are shown below and can be changed for each run.",
 tbl(["Decision","When","Default setting"],[
  ['<span class="chip c-ok">Release</span>',"Material available and load fits","Up to 5 orders per cycle"],
  ['<span class="chip c-advise">Held: material</span>',"Any component is short after earlier allocations","Shared stock pool, FIFO batches"],
  ['<span class="chip c-rec">Held: capacity</span>',"A work center would pass its load or WIP limit","85% of shift capacity per work center"],
  ['<span class="chip c-watch">Next cycle</span>',"Fits, but the cycle cap was reached","Release window of 3 days ahead"],
  ['<span class="chip c-esc">Cleanup</span>',"Missing master data, or more than 14 days past due","Listed for the planner, never released"]]),
 [("Decision table","Order, material, open quantity, due date, late flag, decision, reason and batches used."),
  ("Work-center load","Recent and stale WIP, current load, added load and total % of capacity per work center."),
  ("Material shortages","Shortfall by material and the orders it blocks, ready to post to Teams."),
  ("Cleanup list","Stale orders, data-error orders and stale WIP per work center for the planner.")],
 [("Recommend mode by default.","The agent shows the exact release request without sending it."),
  ("Approve mode for control.","Only the orders a supervisor names in chat are released."),
  ("Auto mode only on request.","Used when the run or a scheduled task explicitly says so, one order at a time."),
  ("Never discards or changes orders.","Data-error, stale and held orders are never released."),
  ("Stops on the first error.","If a release fails, the cycle stops and reports the error."),
  ("Assumptions stated.","Capacity source, standard value reading and estimated loads are listed in every run.")],
 [("How does the agent decide which SAP DM orders to release?","It screens orders due in the release window, checks material availability and work-center load, ranks them by due date, priority and open quantity, and releases those that fit within the limits."),
  ("Can it release partial quantities?","Yes. If the full quantity would exceed a work-center limit, it tries a partial quantity that fits before holding the order."),
  ("What is stale WIP and why does it matter?","Work in progress with no activity for more than 48 hours. The agent counts them separately so old, open jobs do not block new releases."),
  ("Does it work with other SAP DM agents?","Yes. It works alongside the DM Supervisor agent for shop-floor monitoring and the Breakdown Recovery agent, which plans recovery when a machine goes down.")],
 [REL["ewm"],REL["tm"]],
 "See a release cycle run on your SAP Digital Manufacturing plant in recommend mode.",
 "Körber Stellium SAP DM Order Release AI Agent",
 "AI agent that checks material, load and WIP in SAP Digital Manufacturing and recommends or releases production orders.")

# ---------------- PLACEMENT PLAN ----------------
pl_head = '<title>AI Agents Placement Plan</title><meta name="robots" content="noindex, nofollow">' + FONTS + '<link rel="stylesheet" href="styles.css"><meta name="claude:viewport-fit-sides" content="cover">'
U = "https://koerber-stellium.com"
place_rows = [
 ["1",'Services › Innovation menu',f'<a href="{U}/our-services/innovation/">/our-services/innovation/</a>',"Add <b>AI Agents</b> as a sub-service next to Enterprise AI and Products &amp; Add-ons. New hub page plus three child pages.",'<span class="chip c-esc">Must</span>'],
 ["2","Homepage",f'<a href="{U}/">/</a>',"Add a launch strip after <i>Our services</i>: “New: AI agents for SAP EWM, TM and DM”, linking to the hub. Optionally a 9th services card.",'<span class="chip c-esc">Must</span>'],
 ["3","Products &amp; Add-ons",f'<a href="{U}/our-services/innovation/products-add-ons/">/products-add-ons/</a>',"Add three cards beside AWA and ATMA, each linking to its agent page.",'<span class="chip c-esc">Must</span>'],
 ["4","SAP Business AI",f'<a href="{U}/our-services/sap-services/sap-business-ai/">/sap-business-ai/</a>',"Link the existing <i>AI Agents</i> capability block to the hub and name the three assistants.",'<span class="chip c-rec">Should</span>'],
 ["5","Warehouse Management service",f'<a href="{U}/our-services/digital-supply-chain-and-logistics/warehouse-management/">/warehouse-management/</a>',"Add a “Meet the EWM Outbound Supervisor agent” band under <i>Labor Optimization</i>.",'<span class="chip c-rec">Should</span>'],
 ["6","Transportation Management service",f'<a href="{U}/our-services/digital-supply-chain-and-logistics/transportation-management/">/transportation-management/</a>',"Add a band linking to the TM Invoice Dispute agent.",'<span class="chip c-rec">Should</span>'],
 ["7","Digital Manufacturing service",f'<a href="{U}/our-services/digital-supply-chain-and-logistics/digital-manufacturing/">/digital-manufacturing/</a>',"Add a band linking to the DM Order Release agent.",'<span class="chip c-rec">Should</span>'],
 ["8","Solution pages: SAP EWM, SAP TM, SAP DM",f'<a href="{U}/our-solutions/sap-digital-supply-chain/">/our-solutions/sap-digital-supply-chain/…</a>',"Same agent band on each matching solution page, for a second internal link.",'<span class="chip c-rec">Should</span>'],
 ["9","Enterprise AI",f'<a href="{U}/our-services/innovation/enterprise-ai/">/enterprise-ai/</a>',"Add the hub to the closing section as a proof point of production AI.",'<span class="chip c-advise">Could</span>'],
 ["10","Insights &amp; events, FAQ, Contact",f'<a href="{U}/insights-events/">/insights-events/</a>',"One launch blog per agent, add the hub FAQs to /faq/, add “AI agents” to the contact form interest list.",'<span class="chip c-advise">Could</span>'],
]
seo_rows = [
 ["Hub","/our-services/innovation/ai-agents/","AI Agents for SAP EWM, TM &amp; DM | Körber Stellium","SAP AI agents","BreadcrumbList, ItemList, FAQPage"],
 ["EWM","/ai-agents/sap-ewm-outbound-supervisor-agent/","SAP EWM AI Agent for Outbound Supervisors | Körber Stellium","SAP EWM AI agent, wave cutoff","SoftwareApplication, BreadcrumbList, FAQPage"],
 ["TM","/ai-agents/sap-tm-freight-invoice-dispute-agent/","SAP TM Freight Invoice Dispute AI Agent | Körber Stellium","SAP TM invoice dispute, freight audit","SoftwareApplication, BreadcrumbList, FAQPage"],
 ["DM","/ai-agents/sap-dm-order-release-agent/","SAP DM Order Release AI Agent | Körber Stellium","SAP DM order release","SoftwareApplication, BreadcrumbList, FAQPage"],
]
fix_rows = [
 ["Warehouse Management","H1 typo “Iiventory” and H2 typo “aptimize”.","Fix spelling. Both are in headings Google weights heavily."],
 ["Products &amp; Add-ons","The ATMA link points to the AWA page URL.","Point ATMA to its own page."],
 ["Several service pages","H3 blocks appear twice in the HTML (desktop and mobile copies).","Use one responsive block so headings aren’t duplicated."],
 ["Homepage","Stat counters render as “0 +” before JavaScript runs.","Server-render the final numbers."],
 ["Footer","GIVE link uses both /stellium-give/ and /stellium-gives/; one quick link has no URL.","Use one URL and fill the empty link."],
 ["Older pages","Titles and copy still say “Stellium”, not “Körber Stellium”.","Update brand name in titles and meta descriptions."],
]
def serp(path,t,d):
    return f'<div class="serp"><span class="u">koerber-stellium.com › {E(path)}</span><span class="t">{t}</span><span class="d">{E(d)}</span></div>'
pl_body = review("placement-plan.html") + header() + f'''
<main>
<section class="cream" style="padding-block:56px"><div class="wrap stack" style="gap:16px">
<p class="eyebrow" style="color:var(--blue)">For reviewers · Web, Marketing, Innovation</p>
<h1>Where the AI agents go on koerber-stellium.com</h1>
<p class="lead measure" style="color:var(--muted)">We reviewed the homepage, Services, Solutions, SAP Business AI, Enterprise AI, Products &amp; Add-ons and the Warehouse Management pages. The site has no page for AI agents today. The best home is a new <b>AI Agents</b> hub under Services › Innovation, linked from every page a buyer of SAP EWM, TM or DM already visits.</p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Proposed site structure</h2><p>New pages in blue. Existing pages that get a link or band are underlined.</p></div>
<div class="tree"><ul><li>Home <span class="touch">(launch strip)</span><ul>
<li>Services<ul>
<li>Digital supply chain &amp; logistics<ul><li><span class="touch">Warehouse Management</span></li><li><span class="touch">Transportation Management</span></li><li><span class="touch">Digital Manufacturing</span></li></ul></li>
<li>SAP services<ul><li><span class="touch">SAP Business AI</span></li></ul></li>
<li>Innovation<ul><li>Körber Stellium Technology and Innovation Center</li><li><span class="touch">Enterprise AI</span></li><li><span class="touch">Products &amp; Add-ons</span></li>
<li><a class="new" href="index.html">AI Agents</a><ul>
<li><a class="new" href="ewm-outbound-supervisor-agent.html">SAP EWM Outbound Supervisor Agent</a></li>
<li><a class="new" href="tm-invoice-dispute-agent.html">SAP TM Freight Invoice Dispute Agent</a></li>
<li><a class="new" href="dm-order-release-agent.html">SAP DM Order Release Agent</a></li></ul></li></ul></li></ul></li>
<li>Solutions › SAP digital supply chain<ul><li><span class="touch">SAP EWM</span> · <span class="touch">SAP TM</span> · <span class="touch">SAP Digital Manufacturing</span></li></ul></li>
<li>Insights &amp; events <span class="touch">(3 launch blogs)</span> · FAQ <span class="touch">(new entries)</span></li>
</ul></li></ul></div>
</div></section>

<section class="cream"><div class="wrap">
<div class="sec-head"><h2>Placement, in priority order</h2><p>Items 1 to 3 are needed for launch. The rest build internal links, which help the new pages rank.</p></div>
<div class="tblwrap">{tbl(["#","Location","Existing URL","Change","Priority"], place_rows)}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>SEO set-up for the new pages</h2><p>Each page has one H1, a title under 60 characters, a meta description under 160, a canonical URL, Open Graph tags, structured data and breadcrumbs. URLs follow the site’s existing lowercase, hyphenated pattern.</p></div>
<div class="tblwrap">{tbl(["Page","URL","Title tag","Primary keyword","Structured data"], seo_rows)}</div>
<div class="grid2" style="margin-top:32px">
{serp("our-services › innovation › ai-agents","AI Agents for SAP EWM, TM &amp; DM | Körber Stellium","AI agents for SAP EWM outbound supervision, SAP TM freight invoice disputes and SAP DM order release. Live SAP data, clear recommendations, human approval.")}
{serp("ai-agents › sap-tm-freight-invoice-dispute-agent","SAP TM Freight Invoice Dispute AI Agent | Körber Stellium","AI agent for SAP TM freight settlement: matches carrier invoices to the FSD, approves tolerance cases, counter-mails carriers and escalates.")}
</div>
<p style="color:var(--muted);margin-top:16px;font-size:.9rem">Search result previews. The preview pages carry <code>noindex</code>; switch to <code>index, follow</code> and add the URLs to the XML sitemap at go-live.</p>
</div></section>

<section class="cream"><div class="wrap">
<div class="sec-head"><h2>Existing SEO issues found during the review</h2><p>Quick fixes worth bundling with the launch.</p></div>
<div class="tblwrap">{tbl(["Page","Issue","Fix"], fix_rows)}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Go-live checklist</h2></div>
<ul class="guards">
<li>Rebuild the four pages in Elementor using these layouts and copy.</li>
<li>Add AI Agents to the Services › Innovation menu.</li>
<li>Paste title, meta description and canonical into the SEO plugin for each page.</li>
<li>Add the JSON-LD blocks from the page source.</li>
<li>Replace illustrative samples with approved screenshots if preferred.</li>
<li>Switch robots to index, follow and submit the sitemap in Search Console.</li>
<li>Add internal links from the ten placements above.</li>
<li>Publish the three launch blogs and link them to their agent pages.</li>
</ul></div></section>
</main>''' + footer()
page("placement-plan.html", pl_head, pl_body)
open(os.path.join(OUT,"styles.css"),"w").write(CSS)
print("ok", os.listdir(OUT))
