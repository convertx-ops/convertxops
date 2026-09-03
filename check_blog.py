import subprocess, json, os
tok = [l.split('=', 1)[1].strip() for l in open(r'C:\Users\inaya\AppData\Local\hermes\.env') if l.startswith('GITHUB_TOKEN=')][0]
H = {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"}
def get(u):
    r = subprocess.run(["curl", "-s", "-m", "25", "-H", f"Authorization: Bearer {tok}", "-H", "Accept: application/vnd.github+json", u], capture_output=True, text=True, timeout=30)
    try: return json.loads(r.stdout)
    except: return r.stdout
root = get("https://api.github.com/repos/convertx-ops/convertxops/contents/")
print("ROOT:", sorted(x['name'] for x in root)[:50])
blog = get("https://api.github.com/repos/convertx-ops/convertxops/contents/blog")
print("BLOG:", sorted(x['name'] for x in blog) if isinstance(blog, list) else blog)
for u in ["/blog/", "/blog", "/blog/index.html"]:
    rc = subprocess.run(["curl", "-s", "-m", "20", "-o", "/dev/null", "-w", "%{http_code}", f"https://convertx-ops.github.io/convertxops{u}"], capture_output=True, text=True, timeout=25).stdout
    print(u, "->", rc)
