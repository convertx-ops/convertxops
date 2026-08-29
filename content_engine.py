#!/usr/bin/env python3
"""
ConvertX Ops DAILY CONTENT engine (FREE, local Ollama).
- Writes 1 SEO blog post (solar/roofing lead capture) -> inbound/site/blog/
- Prints 1 LinkedIn post + 1 Reddit (r/solar, r/Roofing) + 1 Quora answer draft
  (you paste into LinkedIn/Reddit/Quora free accounts; or future auto-post).
Usage: python3 content_engine.py
"""
import os, json, subprocess, time, re, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BLOG = os.path.join(HERE, "site", "blog")
os.makedirs(BLOG, exist_ok=True)
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"
TOPICS = [
    "why solar installers lose leads after hours","cost of missed calls for roofing businesses",
    "how AI voice agents qualify solar leads","24/7 call answering for roofing estimates",
    "lead capture vs lead generation for solar","booking solar site visits automatically",
    "reducing response time in home services","voice AI for solar appointments",
]

def ollama(prompt, maxtok=500):
    try:
        r = subprocess.run(["curl","-s","-m","120","-X","POST",OLLAMA,
            "-H","Content-Type: application/json",
            "-d", json.dumps({"model":MODEL,"prompt":prompt,"stream":False,"options":{"num_predict":maxtok}})],
            capture_output=True, text=True, timeout=130)
        return json.loads(r.stdout).get("response","").strip()
    except Exception:
        return ""

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def make_post(topic):
    body = ollama(
        f"Write a 280-word useful blog post titled about: {topic}. Audience: US solar and roofing "
        f"business owners. No em-dashes. No hype words. Include one real-sounding number example. "
        f"End with a plain CTA to email convertx.ops@gmail.com for a live demo.", 600)
    return body

def linkedin_post():
    return ollama(
        "Write a 110-word LinkedIn text post for the founder of ConvertX Ops, a company that sells "
        "24/7 AI voice agents to solar and roofing businesses. Hook about missed after-hours calls. "
        "One plain insight with a real number. CTA: reply DEMO. FORBIDDEN words: revolutionary, "
        "game-changing, transform, seamless, unparalleled, excited to introduce, leverage. Plain CEO tone. "
        "No em-dashes. No hashtags in body.", 280)

def reddit_post():
    return ollama(
        "Write a helpful Reddit comment (r/solar or r/Roofing) answering 'how do you handle after-hours "
        "lead calls?' Be genuine, mention 24/7 voice agents briefly, no spam. 120 words, no em-dashes.", 300)

def quora_post():
    return ollama(
        "Write a Quora answer to 'What is the best way to capture solar leads?' Useful, mention 24/7 "
        "answering + qualification, no promo spam. 140 words, no em-dashes.", 300)

def main():
    topic = TOPICS[datetime.date.today().toordinal() % len(TOPICS)]
    # blog
    fn = os.path.join(BLOG, slug(topic)+".html")
    title = topic.title()
    art = make_post(topic)
    tpl = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | ConvertX Ops</title>
<meta name="description" content="{desc}"></head>
<body style="font-family:system-ui,Arial;max-width:720px;margin:auto;padding:24px;line-height:1.6;color:#111">
<header style="border-bottom:2px solid #0a7;padding-bottom:8px"><h1 style="margin:0;color:#0a7">ConvertX Ops</h1></header>
<article><h2>{title}</h2>{body}
<p style="margin-top:20px"><a href="/">Home</a> &middot; <a href="/blog/">Blog</a></p></article>
<footer style="border-top:1px solid #ccc;margin-top:24px;color:#777;font-size:13px">
ConvertX Ops &mdash; convertx.ops@gmail.com | +91-8055317114</footer></body></html>"""
    body_html = "<p>" + "</p><p>".join(art.split("\n\n")) + "</p>" if art else "<p>Coming soon.</p>"
    with open(fn,"w") as f:
        f.write(tpl.format(title=html.escape(title), desc=html.escape(art[:150]), body=body_html))
    print("BLOG:", fn)
    print("\n--- LINKEDIN ---\n", linkedin_post())
    print("\n--- REDDIT ---\n", reddit_post())
    print("\n--- QUORA ---\n", quora_post())

if __name__=="__main__":
    main()
