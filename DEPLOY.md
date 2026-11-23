# DEPLOY — The Beat District (t_36b96016, E2 evolutions rebuild)

Rebuild of thebeatdistrict.co (Wix, junk-confirmed 2026-11-21 vision pass: dated early-2010s fixed-width template; live recheck found responsive viewport but ~10-11px phone type — pitch angle = dated/hard-to-read on phone, NEVER "broken mobile"). Target market: Petersburg VA record store. Recipient: info@thebeatdistrict.co (site-published).

render-sweep line: render-sweep: 18/18 PASS 2026-11-21/22 — 9 pages × 2 viewports (1280/390), DOM metrics clean: zero h-scroll, zero block-clip, zero zero-width, zero sibling-overlap. Montages + vision adjudication in workspace shots (attempt 1 budget-exhausted run banked 6ed100e).

## Stack
- Static node server (server.js + deploy.sh template-v2 pattern), port 8080, pixel GIF at /open, Brevo form relay.
- Git: github.com/gnaritas/the-beat-district (public, main). Work dir: /Users/rleon/sites/the-beat-district.
- Pages: index / records-and-gifts / visit / preorders / contact / privacy / thanks / 404. No store page — full catalog + pre-orders stay at thebeatdistrict.co (provenance line on home + preorders page; SHOP nav links out).

## Deploy — DONE 2026-11-23 (run 125 window)
- Railway: ws "Ramon Leon's Projects" · project **honeyspell-cafe `5be9a2cb-4597-48ed-9368-e8fb587aa71b`** (multi-service shell — account at the 58-project cap; same pattern as E1 pz-painting) · service **the-beat-district id `8d350110-70a5-494c-9094-2e386ae901c8`** · env production · domain id `321a65c0-5262-4e10-856d-9b403c069350` → **https://the-beat-district-demo.up.railway.app** (200-verified; canonical/og:url/sitemap/robots/pixel already pinned to this host from build — no re-pin).
- **Teardown here = GraphQL serviceDelete on 8d350110 — NEVER project delete** (shared shell; siblings live in same project).
- BREVO_API_KEY set at service var step (sliced at "xkeysib" from ~/.hermes/secrets/brevo_smtp_key.txt).
- deploy.sh patched to ride the shell: python block links this dir to shell project+env in ~/.railway/config.json instead of new-project create; vars/domain steps target -s the-beat-district -e production. After auto-create: `railway domain update 321a65c0-5262-4e10-856d-9b403c069350 --domain the-beat-district-demo`.
- **Live render-sweep 2026-11-23 ~07:1x UTC: PASS, 0 fixes.** 16 shots (8 routes × {1280 dsf2, 390 dsf2-mobile}, raw + montages; ~/.hermes/profiles/websites/cache/scratch/tbd-live-shots/). Lane vision timed out twice → OpenRouter gemini-2.5-flash battery (5 calls) verdict 'DEFECTS' = 46 candidate claims, ALL adjudicated false/intentional by live DOM measurement battery: contrast 4.4–16.8:1 vs AA 4.5 (worst real items: rust-button 4.42 large-text, footline 4.54 AA pass, placeholders browser-default ~4.6 vs labels, openstrip grad-min 14.4); zero scroll-clips (12 cards scrollHeight==clientHeight, gap≥3px above padding line); flex row-tops equal everywhere (header/chips/footer wrap naturally); RECORDS = intentional SVG crate art (glyphs y272–294 sit between shelf lines 252/316); footline bottom 6024 < doc 6064. Tree == 6ed100e == live.
- lane.db deploys + services rows booked via sites_agency_state.py (see commands below); verify export after.

## Deploy commands (proven this run)
- `railway up -s 8d350110` (dir linked; multi-service project → always -s) — poll `railway service status --json` (railway status --json can hang on build events).
- vars/domain scoped: `railway variable set -s the-beat-district -e production -v KEY=VAL`; `railway domain list --json`; `railway domain update <id> --domain <name>`.
- Post-deploy verify: _verify.py vs live origin (0 fail/0 warn), 200-walk + OPEN pixel + FORM POST 303 + PARITY (style.css/og.png/pixel/sitemap byte-identical local==live), send_pitch.sh live-gate rehearsal prints home=200 open=200 image/gif.

## Lane bookkeeping after deploy/send
- lane.db deploys + services rows booked via `python3 /Users/rleon/.hermes/profiles/websites/skills/websites-build/scripts/sites_agency_state.py` (import/export/verify); export is a generated mirror, never hand-edited.
- Ladder note: followup_due = send_date + 10 days on the registry/lane.db events row drives the follow-up waves (t2 followup / t3 offer / t4 invoice; teardown recheck >= t2+20d). send_pitch.sh prints t2/t3 candidate counts after send; waves themselves run on their own cards — never invent followup dates here.

## Facts discipline
Every on-site claim in evidence.json (repo root): site copy harvest, GBP/press captures, registry check. Unknowns omitted. Owner Demetrius Frazier (per 11-21 mining evidence); hours Wed–Sun 12–6 from site-published copy + GBP. Do NOT claim "broken mobile" in any copy — recheck found responsive viewport; copy says dated / hard-to-read on phone. Old-site before-shots: ~/.hermes/projects/websites/evolutions/shots-2026-11-21/ (thebeatdistrict_co-*). Pitch angle: dated template + tiny phone type.
