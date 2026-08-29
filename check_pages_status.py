import subprocess, json
tok=[l.split('=',1)[1].strip() for l in open(r'C:\Users\inaya\AppData\Local\hermes\.env') if l.startswith('GITHUB_TOKEN=')][0]
REPO="convertx-ops/convertxops"
def req(method,url,data=None):
    cmd=["curl","-s","-m","25","-X",method,"-H",f"Authorization: Bearer {tok}","-H","Accept: application/vnd.github+json"]
    if data: cmd+=["-d",json.dumps(data)]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    return r.returncode, r.stdout
rc,out=req("GET",f"https://api.github.com/repos/{REPO}/pages")
d=json.loads(out) if out.strip().startswith('{') else {}
print("PAGES status:", d.get("status"), "| html_url:", d.get("html_url"), "| build:", d.get("build",{}).get("status") if isinstance(d.get("build"),dict) else None)
# check if GitHub error text appears on live
r=subprocess.run(["curl","-s","-m","20","https://convertx-ops.github.io/convertxops/"],capture_output=True,text=True,timeout=25)
print("LIVE has GitHub 404 banner?:", "There isn't a GitHub Pages site" in r.stdout)
print("LIVE has real content?:", "ConvertX Ops" in r.stdout)
