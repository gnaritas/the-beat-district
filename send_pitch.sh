#!/bin/bash
# send_pitch.sh — guarded evolution pitch send for the-beat-district (t_36b96016)
# Gates: registry dedupe guard -> live-preview gate -> word/shape/pixel assert -> recipient-window gate -> send -> IMAP read-back -> registry append + recount.
# NEVER re-run after a confirmed send (guard exits ALREADY_SENT). NEVER blind-resend: msg_id recovered from IMAP if envelope JSON fails.
# Recipient tz = Eastern (Petersburg VA) — window gate uses America/New_York.
set -uo pipefail
cd "$(dirname "$0")"
DEMO=https://the-beat-district-demo.up.railway.app
RECIPIENT="info@thebeatdistrict.co"     # site-published, 2 hits in home HTML (evidence.json)
SLUG=$(grep -oE 'https://[a-z0-9-]+-demo\.up\.railway\.app' pitch-draft.md | head -1 | sed -E 's|https://([a-z0-9-]+)-demo\..*|\1|')
TOKEN=$(python3 -c "import re;d=open('pitch-draft.md').read();m=re.search(r'utm_content=([A-Za-z0-9-]+)',d);print(m.group(1))")
echo "slug=$SLUG token=$TOKEN"
[ "$SLUG" = "the-beat-district" ] || { echo "SLUG_DERIVE_FAIL"; exit 1; }
[ "$TOKEN" = "the-beat-district-t1" ] || { echo "TOKEN_DERIVE_FAIL"; exit 1; }

REG=/Users/rleon/.hermes/projects/websites/pitch_registry.jsonl
GUARD=$(python3 -c "
import json
n=0
for l in open('$REG'):
    l=l.strip()
    if not l: continue
    try: r=json.loads(l)
    except Exception: continue
    if r.get('slug')=='$SLUG' and r.get('type')=='pitch': n+=1
print(n)")
[ "$GUARD" = "0" ] || { echo "ALREADY_SENT (registry pitch rows: $GUARD)"; exit 0; }

echo "== live preview gate"
HOME_CODE=$(curl -s -o /tmp/beat_home.html -w "%{http_code}" -m 15 "$DEMO/")
grep -qi "The Beat District" /tmp/beat_home.html || HOME_CODE=BADBODY
grep -qi "noindex" /tmp/beat_home.html || HOME_CODE=NOIDXMISSING
PIX_HDR=$(curl -s -m 15 -o /dev/null -w "%{http_code} %{content_type}" -I "$DEMO/open?t=${SLUG}-t9")
echo "home=$HOME_CODE open=$PIX_HDR"
[ "$HOME_CODE" = "200" ] || { echo "PREVIEW_NOT_LIVE"; exit 3; }
echo "$PIX_HDR" | grep -q "200 image/gif" || { echo "PIXEL_ENDPOINT_DEAD"; exit 3; }

echo "== shape assert (derive tokens from draft on disk)"
python3 - <<'PYEOF' || exit 1
import re, sys
d=open("pitch-draft.md").read()
core=[]
for L in d.split("\n"):
    s=L.strip()
    if not s: continue
    if s.startswith("**"): core.append(re.sub(r"\*\*","",s)); continue
    if s.startswith("Hi ") or s.startswith("— Jarvis") or s.startswith("OnSmalltalk Media ·") or s.startswith("<img"): continue
    core.append(s)
core=re.sub(r"\[([^\]]+)\]\(https?://[^)]+\)", r"\1", "\n".join(core))
wc=len(core.split())
links=d.count("](http")
imgs=d.count("<img")
demo=re.search(r"\[[^\]]+\]\((https://the-beat-district-demo\.up\.railway\.app/[^)]+)\)", d).group(1)
pay=re.search(r"\[[^\]]+\]\((https://buy\.stripe\.com/[^)]+)\)", d).group(1)
pix=re.search(r'src="(https://the-beat-district-demo\.up\.railway\.app/open\?t=[^"]+)"', d).group(1)
tok="the-beat-district-t1"
errs=[]
if wc>110: errs.append(f"core words {wc}>110")
if links!=2: errs.append(f"links {links}!=2")
if imgs!=1: errs.append(f"imgs {imgs}!=1")
for name,u in (("preview",demo),("pay",pay)):
    for param in ("utm_medium=email","utm_campaign=websites",f"utm_content={tok}"):
        if param not in u: errs.append(f"{name} missing {param}")
if "client_reference_id="+tok not in pay: errs.append("pay missing client_reference_id")
if pix!=f"https://the-beat-district-demo.up.railway.app/open?t={tok}": errs.append("pixel token mismatch")
if errs:
    print("ASSERT_FAIL:", errs); sys.exit(1)
print(f"ASSERT PASS: core_words={wc} links=2 pixel-gates=ok")
PYEOF

echo "== recipient-window gate (Eastern = recipient tz; 07:00-17:00)"
HR=$(TZ=America/New_York date +%H)
[ "$HR" -ge 7 ] && [ "$HR" -lt 17 ] || { echo "OUTSIDE_WINDOW hr=$HR — do NOT send; re-park"; exit 4; }

SUBJ=$(python3 -c "print('Your new website is live \u2014 The Beat District')")
echo "== send"
~/bin/email send --account jarvis --as websites --to "$RECIPIENT" --subject "$SUBJ" --json < pitch-draft.md > send-envelope.json 2>send-err.txt
cat send-envelope.json | head -30
MSGID=$(python3 -c "
import json
try:
    d=json.load(open('send-envelope.json'))
except Exception as e:
    print(''); raise SystemExit
import re
s=json.dumps(d)
m=re.search(r'[\"'']message_id[\"'']:\s*[\"'']([^\"'']+)[\"'']', s)
print(m.group(1) if m else '')")
[ -n "$MSGID" ] || MSGID="__NONE__"
echo "MSGID=$MSGID"
if [ "$MSGID" = "__NONE__" ]; then
  echo "envelope did not surface msg_id — read back from IMAP before deciding"
fi

echo "== IMAP read-back (never blind-resend)"
python3 - "$MSGID" "$SUBJ" <<'PYEOF'
import imaplib, re, sys
from email import message_from_bytes
from email.policy import default
msg_id_claim, subj = sys.argv[1], sys.argv[2]
conf={}
for line in open("/Users/rleon/.hermes/config/jarvis-email.conf"):
    m=re.match(r'\s*([A-Z_]+)\s*=\s*"?([^"\s]+)"?', line)
    if m: conf[m.group(1)]=m.group(2)
M=imaplib.IMAP4_SSL(conf["IMAP_SERVER"]); M.login(conf["EMAIL"],conf["APP_PASSWORD"]); M.select('"[Gmail]/Sent Mail"')
typ,res=M.uid('search',None,'SUBJECT','"The Beat District"')
uids=[i.decode() for i in res[0].split()] if res and res[0] else []
found=None
for uid in reversed(uids):
    t,data=M.uid('fetch',uid,'BODY.PEEK[]')
    raw=None
    for item in data:
        if isinstance(item,tuple): raw=item[1]
    msg=message_from_bytes(raw,policy=default)
    if subj in (msg['subject'] or ''):
        found=(uid,msg); break
if not found:
    print("READBACK_FAIL: no sent copy"); sys.exit(2)
uid,msg=found
plain=msg.get_body(preferencelist=('plain',)).get_content()
draft=open("pitch-draft.md").read()
norm=lambda s: "\n".join(l.rstrip() for l in s.replace("\r\n","\n").strip().split("\n"))
mid=msg['Message-ID'] or ''
rt=msg['Reply-To'] or ''
ok_sentcopy = norm(plain)==norm(draft)
ogf = ('Feedback-ID: websites:pitch' in (msg.as_string() or '')) or ('Feedback-ID: websites:pitch' in str(msg.get('References','')))
if not ogf:
    ogf = 'Feedback-ID: websites:pitch' in (msg.get_all('Feedback-ID') and msg['Feedback-ID'] or '')
match_claim = (msg_id_claim=='__NONE__') or (mid.strip('<>').lower()==msg_id_claim.strip('<>').lower())
print("READBACK:", "SENTCOPY_MATCH" if ok_sentcopy else "SENTCOPY_DIFF", "| MID:", mid, "| REPLYTO:", rt, "| OGF:", "ok" if ogf else "check-raw", "| CLAIM_MATCH:", "ok" if match_claim else "MISMATCH", "| uid:", uid)
if not ok_sentcopy or not match_claim: sys.exit(2)
print(mid)
PYEOF
RB=$?
[ $RB -eq 0 ] || { echo "READBACK_PROBLEM exit=$RB — do NOT re-send; investigate"; exit 5; }
if [ "$MSGID" = "__NONE__" ]; then
  MSGID=$(python3 - <<'PYEOF'
import imaplib, re
from email import message_from_bytes
from email.policy import default
conf={}
for line in open("/Users/rleon/.hermes/config/jarvis-email.conf"):
    m=re.match(r'\s*([A-Z_]+)\s*=\s*"?([^"\s]+)"?', line)
    if m: conf[m.group(1)]=m.group(2)
M=imaplib.IMAP4_SSL(conf["IMAP_SERVER"]); M.login(conf["EMAIL"],conf["APP_PASSWORD"]); M.select('"[Gmail]/Sent Mail"')
typ,res=M.uid('search',None,'SUBJECT','"The Beat District"')
uids=[i.decode() for i in res[0].split()] if res and res[0] else []
uid=uids[-1]
t,data=M.uid('fetch',uid,'BODY.PEEK[HEADER]')
raw=None
for item in data:
    if isinstance(item,tuple): raw=item[1]
msg=message_from_bytes(raw,policy=default)
print(msg['Message-ID'] or '')
M.logout()
PYEOF
)
fi

echo "== registry append + recount"
python3 - "$MSGID" <<'PYEOF'
import json, sys, datetime, os
msg_id=sys.argv[1]
REG="/Users/rleon/.hermes/projects/websites/pitch_registry.jsonl"
def plus5bd(d):
    hol={datetime.date(2026,11,26), datetime.date(2026,12,25)}  # Thanksgiving, Christmas
    n=0
    while n<5:
        d+=datetime.timedelta(days=1)
        if d.weekday()>=5 or d in hol: continue
        n+=1
    return d
row={"id": None, "slug": "the-beat-district", "type": "pitch", "feed_id": "exp-evolutions",
     "aliases": ["thebeatdistrict.co", "thebeatdistrict.com", "The Beat District", "info@thebeatdistrict.co"],
     "email": "info@thebeatdistrict.co",
     "subject": "Your new website is live \u2014 The Beat District",
     "subject_arm": "v6", "cohort": "evolutions",
     "utm_content": "the-beat-district-t1",
     "pixel": True, "shot": False,
     "followup_due": plus5bd(datetime.date.today()).isoformat(),
     "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
     "msg_id": msg_id}
import uuid
row["id"]="pk-"+uuid.uuid4().hex[:12]
with open(REG,"r") as f: existing=[json.loads(l) for l in f if l.strip()]
for r in existing:
    if r.get("type")=="pitch" and r.get("slug")=="the-beat-district":
        print("GUARD_RACE: pitch row already present"); sys.exit(1)
with open(REG,"a") as f: f.write(json.dumps(row, ensure_ascii=False)+"\n")
after=[json.loads(l) for l in open(REG) if l.strip()]
n=sum(1 for r in after if r.get("slug")=="the-beat-district" and r.get("type")=="pitch")
print("RECONCILE: pitch rows for slug:", n, "| registry total rows:", len(after))
print("SENT_OK msg_id="+msg_id)
PYEOF
[ $? -eq 0 ] || exit 6
echo "SEND_COMPLETE slug=$SLUG token=$TOKEN recipient=$RECIPIENT"
