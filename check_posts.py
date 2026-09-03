import subprocess
base="https://convertx-ops.github.io/convertxops/blog/"
posts=[
 "do-you-actually-lose-solar-leads-after-hours.html",
 "will-an-ai-voice-agent-sound-robotic-to-my-customers.html",
 "how-much-money-does-a-missed-roofing-call-cost-you.html",
 "why-i-built-convertx-ops-rihan-pathan-founder-story.html",
 "what-happens-on-the-first-call-with-our-ai-agent.html",
 # OLD names (should 404 now):
 "why-solar-installers-lose-leads-after-hours.html",
 "cost-of-missed-calls-for-roofing-businesses.html",
]
for p in posts:
    rc=subprocess.run(["curl","-s","-m","20","-o","/dev/null","-w","%{http_code}",base+p],capture_output=True,text=True,timeout=25).stdout
    print(rc, p)
