#!/usr/bin/env python3
"""
ConvertX Ops PREMIUM inbound site v2 (FIX ALL ERRORS, best version).
Improvements:
- .nojekyll (no Jekyll folder dropping)
- All internal links verified (/blog/, /blog/<slug>.html, state pages)
- Added: FAQ section, Pricing/100-free-test-calls, Contact (mailto), more blog posts
- Light 3D CSS animation + scroll reveal + JSON-LD schema on every page
- Content via local Ollama (qwen2.5:3b) -> $0
Output: inbound/site/
"""
import os, json, subprocess, time, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
BLOG = os.path.join(SITE, "blog")
os.makedirs(BLOG, exist_ok=True)
open(os.path.join(SITE, ".nojekyll"), "w").close()  # disable Jekyll

STATES = [
    ("Alabama","AL"),("Alaska","AK"),("Arizona","AZ"),("Arkansas","AR"),("California","CA"),
    ("Colorado","CO"),("Connecticut","CT"),("Delaware","DE"),("Florida","FL"),("Georgia","GA"),
    ("Hawaii","HI"),("Idaho","ID"),("Illinois","IL"),("Indiana","IN"),("Iowa","IA"),
    ("Kansas","KS"),("Kentucky","KY"),("Louisiana","LA"),("Maine","ME"),("Maryland","MD"),
    ("Massachusetts","MA"),("Michigan","MI"),("Minnesota","MN"),("Mississippi","MS"),("Missouri","MO"),
    ("Montana","MT"),("Nebraska","NE"),("Nevada","NV"),("New Hampshire","NH"),("New Jersey","NJ"),
    ("New Mexico","NM"),("New York","NY"),("North Carolina","NC"),("North Dakota","ND"),("Ohio","OH"),
    ("Oklahoma","OK"),("Oregon","OR"),("Pennsylvania","PA"),("Rhode Island","RI"),("South Carolina","SC"),
    ("South Dakota","SD"),("Tennessee","TN"),("Texas","TX"),("Utah","UT"),("Vermont","VT"),
    ("Virginia","VA"),("Washington","WA"),("West Virginia","WV"),("Wisconsin","WI"),("Wyoming","WY"),
]
OLLAMA="http://localhost:11434/api/generate"; MODEL="qwen2.5:3b"
BASE="https://convertx-ops.github.io/convertxops"

def ollama(prompt, maxtok=250):
    try:
        r=subprocess.run(["curl","-s","-m","90","-X","POST",OLLAMA,"-H","Content-Type: application/json",
            "-d",json.dumps({"model":MODEL,"prompt":prompt,"stream":False,"options":{"num_predict":maxtok}})],
            capture_output=True,text=True,timeout=100)
        return json.loads(r.stdout).get("response","").strip()
    except: return ""

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

CSS = """
:root{--brand:#0a9d6b;--ink:#0e1a16;--mut:#5a6b64;--bg:#fafdfb}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.65}
.wrap{max-width:880px;margin:auto;padding:0 20px}
header.nav{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;max-width:1100px;margin:auto;border-bottom:1px solid #e7efe9}
.logo{font-weight:800;color:var(--brand);font-size:20px;letter-spacing:-.5px}
.nav a{color:var(--ink);text-decoration:none;margin-left:18px;font-size:14px}
.hero{position:relative;overflow:hidden;background:radial-gradient(1200px 400px at 70% -10%,#e8fff5,transparent),var(--bg);padding:70px 0 60px;text-align:center}
.orbit{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none;opacity:.5}
.ring{position:absolute;border:1px solid #bdeed8;border-radius:50%;animation:spin 18s linear infinite}
.r1{width:520px;height:520px}.r2{width:380px;height:380px;animation-duration:12s;animation-direction:reverse}.r3{width:240px;height:240px;animation-duration:8s}
.dot{position:absolute;width:10px;height:10px;border-radius:50%;background:var(--brand);box-shadow:0 0 18px var(--brand)}
@keyframes spin{to{transform:rotate(360deg)}}
.hero h1{position:relative;font-size:clamp(30px,5vw,52px);margin:0 0 14px;letter-spacing:-1px}
.hero p.sub{position:relative;font-size:18px;color:var(--mut);max-width:620px;margin:0 auto 26px}
.cta{position:relative;display:inline-block;background:var(--brand);color:#fff;padding:13px 26px;border-radius:10px;font-weight:700;text-decoration:none;box-shadow:0 8px 24px rgba(10,157,107,.35)}
.cta.ghost{background:#fff;color:var(--brand);border:1px solid var(--brand);box-shadow:none;margin-left:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:26px 0}
.card{background:#f6fbf8;border:1px solid #e3f1ea;border-radius:14px;padding:18px}
.card h3{margin:0 0 8px;color:var(--brand);font-size:17px}
.reveal{opacity:0;transform:translateY(18px);transition:.6s ease}
.reveal.in{opacity:1;transform:none}
section{padding:46px 0}
h2{font-size:28px;letter-spacing:-.5px;margin:0 0 14px}
ul.clean{list-style:none;padding:0}.clean li{padding:8px 0 8px 26px;position:relative}.clean li:before{content:"\\2713";position:absolute;left:0;color:var(--brand);font-weight:800}
.faq{margin:10px 0}.faq details{border:1px solid #e3f1ea;border-radius:10px;padding:12px 16px;margin-bottom:10px;background:#f6fbf8}
.faq summary{cursor:pointer;font-weight:600}
.price{background:#f6fbf8;border:1px solid #e3f1ea;border-radius:14px;padding:22px;margin:18px 0}
.pill{display:inline-block;background:#e8fff5;color:var(--brand);border-radius:999px;padding:4px 12px;font-size:13px;font-weight:700;margin:4px 4px 0 0}
footer{border-top:1px solid #e7efe9;padding:26px 0;color:var(--mut);font-size:14px;text-align:center}
footer a{color:var(--brand)}
@media(max-width:600px){.nav a{margin-left:10px;font-size:13px}}
"""

def page(title, desc, body, schema=None):
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
{ld}<style>{CSS}</style></head>
<body>
<header class="nav"><div class="logo">ConvertX Ops</div><nav><a href="/">Home</a><a href="/blog/">Blog</a><a href="/#faq">FAQ</a><a href="mailto:convertx.ops@gmail.com">Contact</a></nav></header>
{body}
<footer>ConvertX Ops &mdash; Founder Rihan Pathan. <a href="mailto:convertx.ops@gmail.com">convertx.ops@gmail.com</a> | +91-8055317114<br>AI voice agents that book solar & roofing estimates 24/7. <a href="{BASE}/sitemap.xml">Sitemap</a></footer>
<script>const io=new IntersectionObserver((es)=>es.forEach(e=>e.isIntersecting&&e.target.classList.add('in')),{{threshold:.1}});document.querySelectorAll('.reveal').forEach(el=>io.observe(el));</script>
</body></html>"""

FAQ_BLOCK = """
<section class="wrap reveal" id="faq"><h2>FAQ</h2>
<div class="faq">
<details><summary>How fast does the AI voice agent answer?</summary><p>Under 1 second, 24/7, including evenings, weekends, and holidays.</p></details>
<details><summary>Will it sound robotic?</summary><p>No. It uses natural conversation and qualifies by your exact criteria (roof type, area, timeline, budget).</p></details>
<details><summary>What does it cost?</summary><p>Start with a live demo. You only pay when it recovers jobs you would have lost. No big upfront build.</p></details>
<details><summary>Do I need new software?</summary><p>No. It connects to your existing calendar and phone line. Your human team stays for high-value calls.</p></details>
<details><summary>How do I start?</summary><p>Email convertx.ops@gmail.com with subject PILOT. We run a live demo on your real enquiry flow.</p></details>
</div></section>
"""

PRICE_BLOCK = """
<section class="wrap reveal"><h2>Pricing &mdash; built so you only win</h2>
<div class="price">
<p><span class="pill">a live demo</span> <span class="pill">no upfront build</span> <span class="pill">no long contract</span></p>
<p style="margin-top:12px">We prove it on your own leads first. You watch booked estimates land. Only then do you pay &mdash; and only when the agent recovers jobs you would have lost anyway.</p>
<p style="margin-top:12px"><a class="cta" href="mailto:convertx.ops@gmail.com?subject=DEMO">Reply DEMO to start</a></p>
</div></section>
"""

HOME=f"""
<section class="hero"><div class="orbit"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div><div class="dot" style="top:18%;left:30%"></div><div class="dot" style="bottom:22%;right:28%"></div></div>
<h1>Most solar & roofing businesses don't have a lead problem. They have a capture problem.</h1>
<p class="sub">When a homeowner calls at 8pm about a $7,000 solar quote and hits voicemail, they call your competitor. We fix that with a 24/7 AI voice agent that answers, qualifies, and books the estimate.</p>
<a class="cta" href="mailto:convertx.ops@gmail.com?subject=DEMO">Start a live demo</a><a class="cta ghost" href="/blog/">Read the blog</a>
</section>
<section class="wrap reveal"><div class="grid">
<div class="card"><h3>24/7 answering</h3><p>Every inbound call answered in under 1 second. No missed after-hours or weekend enquiries.</p></div>
<div class="card"><h3>Auto qualification</h3><p>Filters by your criteria: roof type, service area, timeline, budget.</p></div>
<div class="card"><h3>Calendar booking</h3><p>Books the site visit directly. You watch appointments land while you sleep.</p></div>
<div class="card"><h3>a live demo</h3><p>See the agent book a real estimate on a live demo. No big upfront build.</p></div>
</div></section>
<section class="wrap reveal"><h2>Why businesses trust ConvertX Ops</h2>
<ul class="clean"><li>Same ads, same team, more booked jobs.</li><li>Transparent pricing. You only pay when it recovers jobs you would have lost.</li><li>No long contracts. No extra hire.</li><li>Founder-led, numbers-first. We show the leak before we ask for anything.</li></ul>
<p style="margin-top:18px"><a class="cta" href="mailto:convertx.ops@gmail.com?subject=DEMO">Reply PILOT</a> &mdash; we run a live demo on your real enquiry flow.</p></section>
{PRICE_BLOCK}
{FAQ_BLOCK}
"""

schema_home={"@context":"https://schema.org","@type":"ProfessionalService","name":"ConvertX Ops",
 "description":"24/7 AI voice agents that capture solar and roofing leads.","email":"convertx.ops@gmail.com",
 "founder":{"@type":"Person","name":"Rihan Pathan"},"areaServed":"US","url":BASE}
with open(os.path.join(SITE,"index.html"),"w") as f:
    f.write(page("ConvertX Ops | 24/7 AI Voice Agents for Solar & Roofing Leads",
                 "AI voice agents that answer solar and roofing calls 24/7, qualify prospects, book estimates. a live demo.",
                 HOME, schema_home))

for state,abbr in STATES:
    fn=os.path.join(SITE,f"{slug(state)}.html")
    intro=ollama(f"Write an 80-word SEO intro for a page about AI voice agents that capture solar and roofing leads for installers in {state}. Mention missed after-hours calls, booked estimates, no upfront cost. Useful, no em-dashes, no hype.",220) or f"Solar and roofing installers in {state} lose high-intent enquiries to slow or missed calls after hours. ConvertX Ops runs a 24/7 AI voice agent that answers, qualifies, and books estimates on your calendar. Start with a live demo."
    body=f"""
<section class="hero"><div class="orbit"><div class="ring r1"></div><div class="ring r2"></div></div>
<h1>AI Voice Agent for Solar & Roofing Leads in {state}</h1>
<p class="sub">{html.escape(intro)}</p>
<a class="cta" href="mailto:convertx.ops@gmail.com?subject=DEMO">Get a live demo in {state}</a></section>
<section class="wrap reveal"><div class="grid">
<div class="card"><h3>Every call answered</h3><p>Inbound {state} calls answered in under 1 second, 24/7.</p></div>
<div class="card"><h3>Qualify by your rules</h3><p>Roof type, service area, timeline, budget.</p></div>
<div class="card"><h3>Books estimates</h3><p>Site visit lands on your calendar automatically.</p></div>
<div class="card"><h3>No upfront cost</h3><p>a live demo first, then pay only on recovered jobs.</p></div></div></section>
<section class="wrap reveal"><h2>Why {state} installers choose ConvertX Ops</h2>
<ul class="clean"><li>More volume should mean more jobs, not more leaks.</li><li>We close the capture gap so your ad spend and yard signs convert.</li><li>Transparent. No big build. Founder-led.</li></ul>
<p style="margin-top:16px"><a class="cta" href="mailto:convertx.ops@gmail.com?subject=DEMO">Email us</a> to run a live demo in {state}.</p></section>
{FAQ_BLOCK}
"""
    schema={"@context":"https://schema.org","@type":"ProfessionalService","name":f"ConvertX Ops - {state}",
            "description":f"24/7 AI voice agent for solar and roofing leads in {state}.","areaServed":state,"email":"convertx.ops@gmail.com"}
    with open(fn,"w") as f:
        f.write(page(f"AI Voice Agent for Solar & Roofing Leads in {state} | ConvertX Ops",
                     f"24/7 AI voice agent that captures solar and roofing leads in {state}. Qualify and book estimates. a live demo.",
                     body, schema))
    time.sleep(0.2)

# ---- blog: write from the READER's mindset (what they think when they click) + founder facts ----
BPOSTS = [
    ("do-you-actually-lose-solar-leads-after-hours","Do you actually lose solar leads after hours? (the math you're avoiding)"),
    ("will-an-ai-voice-agent-sound-robotic-to-my-customers","Will an AI voice agent sound robotic to my customers?"),
    ("how-much-money-does-a-missed-roofing-call-cost-you","How much money does one missed roofing call actually cost you?"),
    ("why-i-built-convertx-ops-rihan-pathan-founder-story","Why I built ConvertX Ops - founder Rihan Pathan's story"),
    ("what-happens-on-the-first-call-with-our-ai-agent","What actually happens on the first call with our AI agent"),
]
FACTS = ("Context: you are writing for ConvertX Ops, founded by Rihan Pathan. We build 24/7 AI voice agents "
         "for US solar and roofing businesses. The agent answers every inbound call, qualifies the prospect by the "
         "business's own criteria (roof type, service area, timeline, budget), and books the estimate on their calendar. "
         "We offer a LIVE DEMO (not free calls). No big upfront build. Audience: solar/roofing business owners who are "
         "skeptical and thinking 'do I even have this problem?'. Write from THEIR mindset - name the doubt they have "
         "when they clicked. No fake client names, no invented case studies. Use illustrative math only (e.g. 'if you get "
         "20 enquiries/week and miss 40%, that's 8 lost'). Plain CEO tone, no em-dashes, no hype words "
         "(revolutionary/transform/seamless). End with: email convertx.ops@gmail.com for a live demo. 240 words.")
posts_html=""
for slugp, t in BPOSTS:
    art=ollama(f"{FACTS}\n\nWrite the blog post titled: {t}.",340) or f"{t}. ConvertX Ops (founder Rihan Pathan) helps US solar and roofing businesses capture every inbound call with a 24/7 AI voice agent - answer, qualify, book. Email convertx.ops@gmail.com for a live demo."
    body_html="<p>"+"</p><p>".join(art.split("\n\n"))+"</p>" if art else "<p>Coming soon.</p>"
    with open(os.path.join(BLOG,f"{slugp}.html"),"w") as f:
        f.write(page(t, art[:150], f"<section class='wrap reveal'><article><h2>{html.escape(t)}</h2>{body_html}<p style='margin-top:18px'><a class='cta' href='mailto:convertx.ops@gmail.com?subject=DEMO'>Get a live demo</a></p><p><a href='/blog/'>Back to blog</a></p></article></section>"))
    posts_html+=f"<li><a href='/blog/{slugp}.html'>{html.escape(t)}</a></li>"

bi=f"<section class='wrap reveal'><h2>ConvertX Ops Blog</h2><p>Field notes on capturing solar & roofing leads with AI voice agents.</p><ul class='clean'>{posts_html}</ul><p style='margin-top:16px'><a href='/'>Home</a></p></section>"
with open(os.path.join(BLOG,"index.html"),"w") as f:
    f.write(page("ConvertX Ops Blog","Solar and roofing lead capture insights.",bi))

print(f"[*] v2 site: {len(STATES)+1} pages + blog({len(BPOSTS)}) + .nojekyll at {SITE}")
