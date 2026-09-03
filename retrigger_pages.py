import subprocess, json, time, os
tok=[l.split('=',1)[1].strip() for l in open(r'C:\Users\inaya\AppData\Local\hermes\.env') if l.startswith('GITHUB_TOKEN=')][0]
REPO="convertx-ops/convertxops"
BASE="https://api.github.com/repos/"+REPO
def req(method,url,data=None):
    cmd=["curl","-s","-m","25","-X",method,"-H",f"Authorization: Bearer {tok}","-H","Accept: application/vnd.github+json"]
    if data: cmd+=["-d",json.dumps(data)]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    return r.returncode, r.stdout
# 1) turn Pages OFF
req("DELETE", BASE+"/pages")
time.sleep(3)
# 2) turn Pages ON (main branch, root)
rc,out=req("POST", BASE+"/pages", {"source":{"branch":"main","path":"/"}})
print("PAGES_ON:", rc, out[:120])
time.sleep(5)
# 3) also disable Jekyll properly via API? Pages already serves static. re-push to trigger build
import shutil
for item in os.listdir('site'):
    s=os.path.join('site',item); d=os.path.join('.',item)
    if os.path.isdir(s): shutil.copytree(s,d,dirs_exist_ok=True)
    else: shutil.copy2(s,d)
subprocess.run(["git","add","-A"],capture_output=True,text=True)
subprocess.run(["git","-c","user.email=convertx.ops@gmail.com","-c","user.name=ConvertX Ops","commit","-q","-m","re-trigger pages build"],capture_output=True,text=True)
url=f"https://{tok}@github.com/{REPO}.git"
r=subprocess.run(["git","push","-f",url,"main"],capture_output=True,text=True,timeout=90)
print("PUSH:", r.returncode)
time.sleep(40)
# 4) verify
for u in ["/","/blog/","/blog/do-you-actually-lose-solar-leads-after-hours.html"]:
    rc=subprocess.run(["curl","-s","-m","20","-o","/dev/null","-w","%{http_code}",f"https://convertx-ops.github.io/convertxops{u}"],capture_output=True,text=True,timeout=25).stdout
    print(u,"->",rc)
