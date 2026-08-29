#!/usr/bin/env python3
"""
Deploy ConvertX Ops static site to GitHub Pages (FREE).
Requires a GitHub Personal Access Token (classic, with repo scope) in env GITHUB_TOKEN.
Creates repo 'convertxops' (if not exists via API) and pushes site/ as Pages root.
Usage: GITHUB_TOKEN=xxx python3 deploy_ghpages.py
"""
import os, subprocess, sys, json

TOKEN = os.environ.get("GITHUB_TOKEN")
USER = "rihanpathan2425"   # your git user (set in git config)
REPO = "convertxops"
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

if not TOKEN:
    print("ERROR: set GITHUB_TOKEN env var (GitHub PAT, repo scope)"); sys.exit(1)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

# 1) create repo (ignore if exists)
run(f'curl -s -m 20 -X POST -H "Authorization: Bearer {TOKEN}" '
    f'-H "Accept: application/vnd.github+json" '
    f'-d \'{{"name":"{REPO}","description":"ConvertX Ops - 24/7 AI voice agents for solar & roofing leads","homepage":"https://{USER}.github.io/{REPO}","public":true}}\' '
    f'https://api.github.com/user/repos')

# 2) copy site into repo root, commit, push
run(f'robocopy "{SITE}" . /E' if os.name=="nt" else f'cp -r "{SITE}/." .')
run('git add -A')
run('git commit -q -m "deploy inbound site" ')
rc,out,err = run(f'git push -f https://{TOKEN}@github.com/{USER}/{REPO}.git HEAD:main')
print("push rc=", rc, err[:200])
print(f"LIVE at https://{USER}.github.io/{REPO}")
