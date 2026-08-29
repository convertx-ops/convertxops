#!/usr/bin/env python3
"""
ConvertX Ops INBOUND site generator (FREE, open-source stack).
- Generates static SEO site: homepage + 50 US-state landing pages + blog.
- Content via local Ollama (qwen2.5:3b) -> $0.
- Output to inbound/site/  (deploy to GitHub Pages / Vercel / Netlify free).
Usage: python3 sitegen.py
"""
import os, json, subprocess, time, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
BLOG = os.path.join(SITE, "blog")
os.makedirs(BLOG, exist_ok=True)

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

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def ollama(prompt, maxtok=400):
    try:
        r = subprocess.run(["curl","-s","-m","90","-X","POST",OLLAMA,
            "-H","Content-Type: application/json",
            "-d", json.dumps({"model":MODEL,"prompt":prompt,"stream":False,"options":{"num_predict":maxtok}})],
            capture_output=True, text=True, timeout=100)
        out = json.loads(r.stdout).get("response","").strip()
        return out
    except Exception as e:
        return ""

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def gen_state_intro(state, abbr):
    p = (f"Write a 90-word SEO intro for a page about AI voice agents that capture solar and "
         f"roofing leads for installers in {state}. Mention missed after-hours calls, booked estimates, "
         f"no upfront cost. Useful tone, no em-dashes, no hype words like 'revolutionary'.")
    return ollama(p, 250)

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
</head>
<body style="font-family:system-ui,Arial,sans-serif;max-width:760px;margin:auto;padding:24px;color:#111;line-height:1.6">
<header style="border-bottom:2px solid #0a7;padding-bottom:10px;margin-bottom:20px">
<h1 style="margin:0;color:#0a7">ConvertX Ops</h1>
<p style="margin:4px 0 0;color:#555">AI voice agents that book solar & roofing estimates 24/7</p>
</header>
<main>
{body}
</main>
<footer style="border-top:1px solid #ccc;margin-top:30px;padding-top:12px;color:#777;font-size:13px">
<p>ConvertX Ops &mdash; Founder Rihan Pathan. <a href="mailto:convertx.ops@gmail.com">convertx.ops@gmail.com</a> | +91-8055317114</p>
<p><a href="/">Home</a> &middot; <a href="/blog/">Blog</a></p>
</footer>
</body>
</html>"""

def page(title, desc, body_inner):
    return TPL.format(title=html.escape(title), desc=html.escape(desc), body=body_inner)

# ---------- Homepage ----------
home_body = """
<h2>Most solar & roofing businesses don't have a lead problem. They have a capture problem.</h2>
<p>When a homeowner calls at 8pm about a $7,000 solar quote and hits voicemail, they don't wait. They call your competitor who answers. ConvertX Ops fixes that with a 24/7 AI voice agent that answers every call, qualifies the prospect, and books the estimate on your calendar.</p>
<h3>What you get</h3>
<ul>
<li>24/7 call answering &mdash; no missed after-hours or weekend enquiries</li>
<li>Automatic qualification by your criteria (roof type, suburb, timeline, budget)</li>
<li>Direct calendar booking &mdash; watch appointments land while you sleep</li>
<li>100 free test calls first &mdash; see real booked estimates before spending a dollar</li>
</ul>
<h3>Why businesses trust us</h3>
<p>We show the numbers. Same ads, same team, more booked jobs. No long contracts, no big upfront build. You only pay when it recovers jobs you would have lost.</p>
<h3>Start</h3>
<p>Reply <b>PILOT</b> or email <a href="mailto:convertx.ops@gmail.com">convertx.ops@gmail.com</a>. We run 100 free test calls on your real enquiry flow.</p>
"""
with open(os.path.join(SITE,"index.html"),"w") as f:
    f.write(page("ConvertX Ops | 24/7 AI Voice Agents for Solar & Roofing Leads",
                 "AI voice agents that answer solar and roofing calls 24/7, qualify prospects, and book estimates. 100 free test calls.",
                 home_body))

# ---------- State pages ----------
for state, abbr in STATES:
    fn = os.path.join(SITE, f"{slug(state)}.html")
    if os.path.exists(fn):
        continue  # cache; don't re-call ollama every run
    intro = gen_state_intro(state, abbr) or (
        f"Solar and roofing installers in {state} lose high-intent enquiries to slow or missed "
        f"calls after hours. ConvertX Ops runs a 24/7 AI voice agent that answers, qualifies, "
        f"and books estimates on your calendar. Start with 100 free test calls.")
    body = f"""
<h2>AI Voice Agent for Solar & Roofing Leads in {state}</h2>
<p>{html.escape(intro)}</p>
<h3>How it works for {state} installers</h3>
<ul>
<li>Every inbound call answered in under 1 second, 24/7</li>
<li>Qualifies by your criteria (roof type, service area, timeline)</li>
<li>Books the site visit directly into your calendar</li>
<li>100 free test calls &mdash; you see booked {state} estimates before paying</li>
</ul>
<h3>Why {state} businesses choose ConvertX Ops</h3>
<p>More volume should mean more jobs, not more leaks. We close the capture gap so your ad spend and yard signs actually convert. Transparent, no big upfront cost.</p>
<p>Email <a href="mailto:convertx.ops@gmail.com">convertx.ops@gmail.com</a> or reply PILOT to run 100 free test calls in {state}.</p>
"""
    with open(fn,"w") as f:
        f.write(page(f"AI Voice Agent for Solar & Roofing Leads in {state} | ConvertX Ops",
                     f"24/7 AI voice agent that captures solar and roofing leads in {state}. Qualify and book estimates. 100 free test calls.",
                     body))
    time.sleep(0.3)

# ---------- Blog index ----------
blog_index = "<h2>ConvertX Ops Blog</h2><p>Field notes on capturing solar & roofing leads with AI voice agents.</p><ul>"
if os.path.exists(BLOG):
    for fn in sorted(os.listdir(BLOG)):
        if fn.endswith(".html"):
            t = fn[:-5].replace("-"," ").title()
            blog_index += f'<li><a href="/blog/{fn}">{html.escape(t)}</a></li>'
blog_index += "</ul>"
with open(os.path.join(BLOG,"index.html"),"w") as f:
    f.write(page("ConvertX Ops Blog","Solar and roofing lead capture insights.",blog_index))

print(f"[*] site generated: {len(STATES)+1} pages + blog index at {SITE}")
