#!/bin/bash
# send_pitch.sh — guarded evolution pitch send for the-beat-district E2 (t_36b96016)
# Ports pz-painting proven kit tip e8fc692 2026-11-22. Recipient tz America/New_York (Petersburg VA).
# Gates: registry dedupe guard -> live-preview gate -> word/shape/pixel assert -> recipient-window gate -> send -> IMAP read-back -> registry append + recount.
# NEVER re-run after a confirmed send (guard exits ALREADY_SENT). NEVER blind-resend: msg_id recovered from IMAP if envelope JSON fails.
set -uo pipefail
cd "$(dirname "$0")"
DEMO=https://the-beat-district-demo.up.railway.app
RECIPIENT="info@thebeatdistrict.co"     # site-published mailto (verified, evidence.json)
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
HOME_CODE=$(curl -s -o /tmp/tbd_home.html -w "%{http_code}" -m 15 "$DEMO/")
grep -qi "The Beat District" /tmp/tbd_home.html || HOME_CODE=BADBODY
grep -qi "noindex" /tmp/tbd_home.html || HOME_CODE=NOIDXMISSING
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

echo "== reply check (never pitch into an owner reply — INBOX FROM recipient domain)"
python3 - <<'PYEOF' || exit 7
import imaplib, re, sys
conf={}
for line in open("/Users/rleon/.hermes/config/jarvis-email.conf"):
    m=re.match(r'\s*([A-Z_]+)\s*=\s*"?([^"\s]+)"?', line)
    if m: conf[m.group(1)]=m.group(2)
M=imaplib.IMAP4_SSL(conf["IMAP_SERVER"]); M.login(conf["EMAIL"],conf["APP_PASSWORD"]); M.select('INBOX')
typ,res=M.uid('search',None,'FROM','thebeatdistrict.co')
uids=[i.decode() for i in res[0].split()] if res and res[0] else []
print("INBOX FROM thebeatdistrict.co uids:", uids)
sys.exit(2 if uids else 0)
PYEOF

echo "== recipient-window gate (America/New_York = recipient tz (Petersburg VA); 07:00-17:00)"
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
# dig message_id wherever it lives
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
# Feedback-ID may ride its own header; check raw
if not ogf:
    ogf = 'Feedback-ID: websites:pitch' in (msg.get_all('Feedback-ID') and msg['Feedback-ID'] or '')
match_claim = (msg_id_claim=='__NONE__') or (mid.strip('<>').lower()==msg_id_claim.strip('<>').lower())
print("READBACK:", "SENTCOPY_MATCH" if ok_sentcopy else "SENTCOPY_DIFF", "| MID:", mid, "| REPLYTO:", rt, "| OGF:", "ok" if ogf else "check-raw", "| CLAIM_MATCH:", "ok" if match_claim else "MISMATCH", "| uid:", uid)
if not ok_sentcopy or not match_claim: sys.exit(2)
print(mid)
PYEOF
RB=$?
[ $RB -eq 0 ] || { echo "READBACK_PROBLEM exit=$RB — do NOT re-send; investigate"; exit 5; }
# capture true mid from last line of readback: re-run cheap by parsing file? simpler: use MSGID unless __NONE__, else re-derive:
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

python3 - <<'PYEOF' || true
import datetime, json
today = datetime.date.today()
fu = (today + datetime.timedelta(days=10)).isoformat()
sw = ("render-sweep: 18/18 PASS 2026-11-21/22 (9 pages x 2 viewports; DOM metrics clean; "
      "vision: gemini-2.5-flash OpenRouter battery 5 calls 2026-11-23 — 46 claims adjudicated "
      "against live DOM measurements, 0 real, 0 fixes). Live: https://the-beat-district-demo.up.railway.app "
      "(Railway shell project honeyspell-cafe, service 8d350110; teardown = serviceDelete, never project delete). "
      "Before-shots: projects/websites/evolutions/shots-2026-11-21/thebeatdistrict_co-*.")
try:
    with open("DEPLOY.md") as f: dep = f.read()
    if "render-sweep" not in dep:
        with open("DEPLOY.md", "a") as f: f.write("\n" + sw + "\n")
        print("DEPLOY_MD: sweep line appended")
    else:
        print("DEPLOY_MD: sweep line already banked")
except FileNotFoundError:
    print("DEPLOY_MD: missing")
REG = "/Users/rleon/.hermes/projects/websites/pitch_registry.jsonl"
rows = [json.loads(l) for l in open(REG) if l.strip()]
def t1_done(r): return (r.get("msg_id") or "").strip() not in ("", "__NONE__")
existing = {r.get("slug") for r in rows if r.get("type") in ("t2", "t3")}
t1 = [r for r in rows if r.get("type") == "pitch" and t1_done(r) and r.get("slug") not in existing]
print("t1 skip (unanswered):", ", ".join(sorted(r.get("slug", "?") for r in t1 if str(r.get("followup_due", "")) > fu)) or "none")
for kind, due_s in (("t2", fu), ("t3", None)):
    due = due_s or (datetime.date.fromisoformat(fu) + datetime.timedelta(days=7)).isoformat()
    hits = [r.get("slug", "?") for r in t1 if r.get("followup_due") == due]
    print(kind, "candidates (due", due + "):", ", ".join(sorted(set(hits))) or "none")
PYEOF

echo "== registry append + recount (jsonl + lane.db events mirror)"
python3 - "$MSGID" <<'PYEOF'
import json, sys, datetime, time, sqlite3
msg_id=sys.argv[1]
REG="/Users/rleon/.hermes/projects/websites/pitch_registry.jsonl"
LANEDB="/Users/rleon/.hermes/projects/websites/lane.db"
today=datetime.date.today()
fu=(today+datetime.timedelta(days=10)).isoformat()
row={"id": None, "slug": "the-beat-district", "type": "pitch", "feed_id": "exp-evolutions",
     "shop_id": "thebeatdistrict.co",
     "aliases": ["thebeatdistrict.co","The Beat District","info@thebeatdistrict.co"],
     "business": "The Beat District (Petersburg VA)",
     "email": "info@thebeatdistrict.co",
     "subject": "Your new website is live \u2014 The Beat District",
     "subject_arm": "v6", "cohort": "evolutions",
     "preview": "https://the-beat-district-demo.up.railway.app",
     "card": "t_36b96016",
     "utm_content": "the-beat-district-t1",
     "pixel": True, "shot": False,
     "date": today.isoformat(),
     "followup_due": fu,
     "ladder": "t2 "+fu+" / t3 t2+7d / t4 t2+14d (weekday ladder, US-holiday shift); teardown recheck >= t2+20d",
     "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
     "msg_id": msg_id,
     "note": "E2 evolutions rebuild pitch (junk-confirmed dated 2010s Wix template with tiny phone type per 11-21 vision pass; live recheck found responsive viewport — copy says dated/hard-to-read, never broken); phone-friendly demo; founder bundle $249+$39/mo 31d trial; read-back SENTCOPY_MATCH proof via send_pitch.sh"}
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
# lane.db events mirror row (canonical store per DATA RULE 2026-11-21)
db=sqlite3.connect(LANEDB)
have=db.execute("SELECT COUNT(*) FROM events WHERE type='pitch' AND slug='the-beat-district'").fetchone()[0]
if have:
    print("EVENTS_GUARD_RACE: events pitch row already present"); sys.exit(1)
line=db.execute("SELECT COALESCE(MAX(line),0)+1 FROM events").fetchone()[0]
db.execute("INSERT INTO events (line,type,feed_id,shop_id,slug,business,email,msg_id,followup_due,date_txt,ts,note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
  (line,"pitch","exp-evolutions","thebeatdistrict.co","the-beat-district","The Beat District (Petersburg VA)","info@thebeatdistrict.co",msg_id,fu,today.isoformat(),int(time.time()),
   "E2 evolutions rebuild pitch; junk-confirmed dated 2010s template, phone-unfriendly type; demo https://the-beat-district-demo.up.railway.app; founder bundle $249+$39/mo 31d trial; v6 subject arm"))
db.commit()
npitch=db.execute("SELECT COUNT(*) FROM events WHERE type='pitch'").fetchone()[0]
print("EVENT_ROW_OK line=", line, "| events pitch total:", npitch)
print("SENT_OK msg_id="+msg_id)
PYEOF
[ $? -eq 0 ] || exit 6
echo "SEND_COMPLETE slug=$SLUG token=$TOKEN recipient=$RECIPIENT"
