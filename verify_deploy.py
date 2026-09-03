import subprocess, json
tok=[l.split('=',1)[1].strip() for l in open(r'C:\Users\inaya\AppData\Local\hermes\.env') if l.startswith('GITHUB_TOKEN=')][0]
H={"Authorization":f"Bearer {tok}","Accept":"application/vnd.github+json"}
def get(u):
    r=subprocess.run(["curl","-s","-m","25","-H",f"Authorization: Bearer {tok}","-H","Accept: application/vnd.github+json",u],capture_output=True,text=True,timeout=30)
    return json.loads(r.stdout) if r.stdout.strip().startswith(('{','[')) else r.stdout
root=get("https://api.github.com/repos/convertx-ops/convertxops/contents/")
names=sorted(x['name'] for x in root)
print("404.html in repo:", "404.html" in names)
print("nojekyll in repo:", ".nojekyll" in names)
# check live 404 behavior
for u in ["/404.html","/blog/do-you-actually-lose-solar-leads-after-hours.html","/blog/"]:
    rc=subprocess.run(["curl","-s","-m","20","-o","/dev/null","-w","%{http_code}",f"https://convertx-ops.github.io/convertxops{u}"],capture_output=True,text=True,timeout=25).stdout
    print(u,"->",rc)
