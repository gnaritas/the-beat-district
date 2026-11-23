#!/bin/bash
# deploy.sh — The Beat District E2 deploy to Railway + live verification (t_36b96016)
# Adapted from the pz-painting guarded runbook (t_811cd84b). Slot-full exits 2 (park, do not force).
# Idempotent-ish: re-running after partial success is safe (up re-creates nothing that exists; domain rename is set-based).
set -uo pipefail
cd /Users/rleon/sites/the-beat-district
DEMO=https://the-beat-district-demo.up.railway.app

echo "== 0. link dir to honeyspell-cafe shell project (58-project cap house pattern, E1 t_811cd84b / terra-house etc)"
python3 - <<'CFGEOF'
import json
CFG="/Users/rleon/.railway/config.json"
c=json.load(open(CFG))
key="/Users/rleon/sites/the-beat-district"
c["projects"].setdefault(key, {
    "environment": "f96cf84f-dc58-422f-af76-fa6d5e9e79e1",
    "environmentName": "production",
    "name": "honeyspell-cafe",
    "project": "5be9a2cb-4597-48ed-9368-e8fb587aa71b",
    "projectPath": key,
    "service": None,
})
json.dump(c, open(CFG, "w"))
print("linked:", key, "-> honeyspell-cafe 5be9a2cb")
CFGEOF

echo "== 1. service create + deploy inside shell"
ADD_OUT=$(railway add -s the-beat-district </dev/null 2>&1 | tail -8)
echo "$ADD_OUT"
if echo "$ADD_OUT" | grep -qi "project limit"; then echo "SLOT_FULL"; exit 2; fi
UP_OUT=$(railway up -d -y -s the-beat-district -e production </dev/null 2>&1 | tail -12)
echo "$UP_OUT"
if echo "$UP_OUT" | grep -qi "project limit"; then echo "SLOT_FULL"; exit 2; fi

echo "== 2. domain"
DOM=$(railway domain list --json -s the-beat-district 2>/dev/null || true)
if [ -z "$DOM" ] || [ "$DOM" = "[]" ] || [ "$DOM" = "null" ]; then
  DOM=$(railway domain -s the-beat-district </dev/null 2>&1); echo "$DOM" | head -3
  DOM=$(railway domain list --json -s the-beat-district 2>/dev/null)
fi
echo "$DOM" | python3 -c "import sys,json;d=json.load(sys.stdin);[print(x.get('id'),x.get('domain') or x.get('hostname') or x.get('url')) for x in (d if isinstance(d,list) else d.get('domains',[]))]"
CUR=$(echo "$DOM" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if isinstance(d,dict): d=d.get('domains',d.get('data',[]))
for x in d:
    dom=x.get('domain') or x.get('hostname') or x.get('url') or ''
    if 'up.railway.app' in str(dom):
        print(x.get('id') or dom); break")
if [ -n "$CUR" ]; then
  echo "current domain record: $CUR"
  railway domain update "$CUR" --domain the-beat-district-demo --json | head -5 || echo "DOMAIN_RENAME_MAYBE_ALREADY_DONE"
fi

echo "== 3. brevo variable"
awk '/xkeysib/{i=index($0,"xkeysib");print substr($0,i)}' /Users/rleon/.hermes/secrets/brevo_smtp_key.txt | railway variable set BREVO_API_KEY --stdin -s the-beat-district -e production 2>&1 | tail -2

echo "== 4. redeploy with vars"
railway up -d -y -s the-beat-district -e production </dev/null 2>&1 | tail -3

echo "== 5. wait for live"
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 10 "$DEMO/" || true)
  [ "$code" = "200" ] && break
  sleep 20
done
echo "home http: $code"
[ "$code" = "200" ] || { echo "NOT_LIVE_YET"; exit 3; }

echo "== 6. live verification walk"
python3 - <<'PYEOF'
import subprocess, hashlib, sys, os
DEMO="https://the-beat-district-demo.up.railway.app"
def get(p, method="GET", data=None):
    cmd=["curl","-s","-m","25","-X",method,"-w","\n%{http_code}"]
    if data: cmd+=["--data",data]
    cmd.append(DEMO+p)
    r=subprocess.run(cmd,capture_output=True,text=True,errors="ignore")
    body,code=r.stdout.rsplit("\n",1)
    return int(code),body
routes=["/","/records-and-gifts","/visit","/preorders","/contact","/privacy","/thanks","/sitemap.xml","/robots.txt","/favicon.svg","/style.css","/pixel.gif","/og.png","/nope"]
fail=0
for r in routes:
    code,body=get(r)
    want=404 if r=="/nope" else 200
    ok=(code==want)
    if want==200 and r.endswith(".html") or r in ("/","/records-and-gifts","/visit","/preorders","/contact","/privacy","/thanks"):
        ok = ok and "The Beat District" in body
    if r=="/nope": ok = (code==404) and ("The Beat District" in body)
    if r in ("/sitemap.xml","/robots.txt","/style.css","/pixel.gif","/og.png","/favicon.svg"):
        ok = (code==200)
    print(("OK " if ok else "FAIL"), code, r)
    if not ok: fail+=1
# pixel endpoint self-test with reserved probe token
code,body=get("/open?t=the-beat-district-t9")
h=subprocess.run(["curl","-s","-m","20","-o","/dev/null","-w","%{http_code} %{content_type}","-I",DEMO+"/open?t=the-beat-district-t9"],capture_output=True,text=True).stdout
print("OPEN probe:",h.strip(), "(expect 200 image/gif)")
if not (code==200 and "200 image/gif" in h): fail+=1
# form relay probe (real mail lands in lane inbox; identity-clean)
code,body=get("/contact","POST","name=Sweep+Probe&phone=&email=jarvis%2Bprobe%40onsmalltalk.com&message=deploy+relay+probe&callback=")
print("FORM POST:",code,"(expect 303; 502/503 = mail send failed - check BREVO var)", body[:120].replace(chr(10)," "))
if code not in (303,): fail+=1
# byte parity local==live (binary-safe: fetch to file)
import tempfile
for f in ["style.css","og.png","pixel.gif","sitemap.xml","robots.txt","favicon.svg"]:
    subprocess.run(["curl","-s","-m","25","-o","/tmp/live_"+f,DEMO+"/"+f])
    live=open("/tmp/live_"+f,"rb").read()
    loc=open(os.path.join("public",f),"rb").read()
    print(("PARITY-OK " if live==loc else "PARITY-FAIL "), f, len(loc), len(live))
    if live!=loc: fail+=1
# headers: noindex
hdr=subprocess.run(["curl","-s","-m","20","-I",DEMO+"/"],capture_output=True,text=True).stdout.lower()
print("X-ROBOTS:", [l for l in hdr.split("\n") if "robots" in l] or "meta-noindex-in-html-only")
print("TOTAL FAILS:", fail)
sys.exit(1 if fail else 0)
PYEOF
VEXIT=$?
echo "live verify exit: $VEXIT"
exit $VEXIT
