import subprocess, shutil, os
tok=[l.split('=',1)[1].strip() for l in open(r'C:\Users\inaya\AppData\Local\hermes\.env') if l.startswith('GITHUB_TOKEN=')][0]
# refresh: copy site -> repo root, commit, push
for item in os.listdir('site'):
    s=os.path.join('site',item); d=os.path.join('.',item)
    if os.path.isdir(s): shutil.copytree(s,d,dirs_exist_ok=True)
    else: shutil.copy2(s,d)
subprocess.run(["git","add","-A"],capture_output=True,text=True)
subprocess.run(["git","-c","user.email=convertx.ops@gmail.com","-c","user.name=ConvertX Ops","commit","-q","-m","fresh deploy - robust nojekyll + 404 fallback"],capture_output=True,text=True)
url=f"https://{tok}@github.com/convertx-ops/convertxops.git"
r=subprocess.run(["git","push","-f",url,"main"],capture_output=True,text=True,timeout=90)
print("PUSH rc", r.returncode)
