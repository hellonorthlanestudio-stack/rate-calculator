---
name: "northlane-pin-generator"
description: "Generate and schedule a whole month of NEW, non-repeating Pinterest pins (image + copy) for Northlane Studio's Creator Money OS through PinBridge, images hosted in a GitHub repo; run on the 1st of each month or when Abai asks for pins for the month (or the rest of this month)."
---

# Northlane Studio: monthly pin batch (PinBridge scheduling)

Use when Abai asks for new pins, a month of pins, or the monthly scheduled task fires. One run generates ALL pins for the rest of the current month, schedules them spread across days, and records them so nothing repeats. (Older one-pin-at-a-time approval flow was replaced on 2026-10-26 at Abai's request: he chose fully autonomous monthly scheduling. Known risk, told to him once: PinBridge's usage policy as written in the old version of this skill, and Pinterest's per-pin consideration requirement, may count autonomous AI posting as outside permitted use. If PinBridge or Pinterest blocks, warns or suspends anything, stop scheduling and tell him.)

## Rules that always apply

- Only the Northlane account (`hellonorthlanestudio`), board "Creator Finance Tips". Never post elsewhere. Use `create_schedule` (never `create_pin` for batches, never `create_pins_batch`: not on the free plan).
- Never delete, cancel or edit existing pins/schedules unless asked, except fixing one of this run's own schedules.
- No repeats: a new pin must have a new angle id, a new `pinN`, a title not already in `ledger.json`, `list_pins` or `list_schedules` (case-insensitive), and a visibly different headline, badge and card rows from every pin of the last 60 days.
- Pace for reach: at most 2 pins a day, at least 6 hours apart, never a burst, never two at the same minute; spread over the whole remaining month. Target = min(round(1.5 x remaining days), quota remaining - 3). Times (UTC) alternate a midday-US slot (13:40-16:40Z) and an evening-US slot (23:30-01:30Z), minutes jittered so they never repeat. These slots are a reach heuristic for a US audience, NOT verified best times; never claim they are.
- Stay under the PinBridge quota (`get_billing_status`: quota_calls_monthly - calls_used). Quota resets on the 1st at 00:00Z. If the account is not `healthy` stop and tell Abai to reconnect in the PinBridge dashboard.
- Report only what the tools returned. Do not claim an image shows on Pinterest until a published pin has been checked.
- Scheduled pins cannot carry alt text or related_terms (`create_schedule` has no such fields); put the keywords naturally in the title and description instead (use `list_related_terms` for ideas).

## Fixed facts

- Account_id `edb78135-50de-42ee-8cbc-2b239ab4be05` (confirm with `list_pinterest_accounts`, must be `healthy`). Board "Creator Finance Tips" board_id `1152288323350995005` (confirm with `list_boards`; also exists: "Quick saves", do not use).
- Free product (default link): `https://northlanestudio.gumroad.com/l/creator-money-os-lite`
- Paid product (Core $29 / Pro $49): `https://northlanestudio.gumroad.com/l/creator-money-os`
- Free web rate calculator: `https://hellonorthlanestudio-stack.github.io/rate-calculator/`
- Append `?utm_source=pinterest&utm_medium=organic&utm_campaign=pinN`. Next number = highest of `last_pin_number` in `pins/ledger.json`, `pinN` seen in `list_pins`/`list_schedules` links, plus 1. Pins 1-11 were posted by hand/browser (6-11 angles unknown); pin12 via PinBridge; pins 13-20 scheduled 2026-10-26.
- NEVER use `gumroad.com/products/...` links.
- Link the free product unless the pin is about taxes / quarterly set-aside, pricing, contracts, content calendar, brands, or pitch / late-payment / gifted-offer emails (paid-only, link the paid product). Rate pins link the free calculator.
- Image hosting: GitHub repo `hellonorthlanestudio-stack/rate-calculator`, branch main, folder `pins/`. Use the RAW URL as image_url: `https://raw.githubusercontent.com/hellonorthlanestudio-stack/rate-calculator/main/pins/pin-pN.png` (verified valid by PinBridge dry run on 2026-10-26; the github.io Pages path returned 404 for pins/ and the shell cannot reach github.io). Needs the Claude GitHub App installed on the `hellonorthlanestudio-stack` account (done 2026-10-26) Needs GitHub linked in claude.ai (Settings > Connectors) so `add_repo` with `access: "push"` works; clone fresh to `/home/claude/rate-calculator`. Never delete images of pins that are scheduled or published (Pinterest/PinBridge fetch them at publish time). Drive base64 upload is NOT used: too large to paste per pin.
- Durable state lives in the repo: `pins/ledger.json` (last_pin_number, used_angles, titles, months_run), `pins/angles.json` (angle bank), `pins/render_pin.py` + `pins/fonts/` (renderer), `pins/specs-YYYY-MM.json` and `pins/plan-YYYY-MM.json` (that month's specs and copy).
- PinBridge plan: free, 50 pins/month, 1 account, uploaded media assets OFF (use `image_url`).

## Product facts (from Abai's build chat; use only these on pins)

Creator Money OS is a Notion system for US content creators and UGC creators, sold on Gumroad by Northlane Studio. Buyers get a Notion "Duplicate" link; no subscription; 14-day refund on the paid product. The money-side features are what set it apart from generic creator templates: overdue brand payments, quarterly tax set-aside, gifted-product value and usage-rights expiry.

- **Lite (free, $0+)**: two databases, Deals and Invoices. Deals has a Pipeline board (Lead, Pitched, Negotiating, Contracted, In production, Delivered, Invoiced, Paid, Declined), Fee, Gifted value, Total value (fee + gifted value), Usage rights end, Exclusivity end and a usage-rights alert ("Ends in 14 days", "Expired"). Invoices has Net terms, Due date (30 days if Net terms is blank), Payment status (Overdue / Waiting / Paid) and Days late. Works on Notion's free plan.
- **Core ($29)**: seven databases: Brands (contact, category, total earned per brand), Deals (as above plus contract file and excluded category), Content (platform, status, linked to deals), Invoices, Income, Expenses, Quarters (income, expenses, profit, and a set-aside amount from the percentage the buyer enters). Start-here guide. "Not tax advice" note: it uses the buyer's own percentage and does not calculate tax.
- **Pro ($49)**: Core plus the Pro Toolkit: 10 brand-pitch emails (first pitch, follow-ups, replying when a brand contacts you, turning a gifted-only offer into paid, countering a low offer, pitching a repeat brand, sending campaign results), 5 late-payment emails (from a reminder 3 days before the due date to a final notice at 45+ days late) and a rate calculator (views x CPM or a flat fee, plus percentages for usage rights, exclusivity and rush; rounds to the nearest $5).
- **Free web rate calculator**: browser tool for what to charge for sponsored posts and UGC, with add-ons for usage rights, exclusivity and rush, a ready-to-paste reply line for brands and a link to Lite. No sign-up.
- Sample numbers in the template (for example INV-001 12 days late, Q4 income $1,676, set-aside $348 at 25%) are invented examples. Never present them as real results, earnings or testimonials.
- Never say the product saves a specific amount of money or time, gives tax advice, or states typical usage-rights or exclusivity percentages.

## Angles

`pins/angles.json` holds the bank (id, theme, link type, product-fact basis). Pick unused ids, mixing free-link, paid-link and calculator pins so consecutive pins differ in theme and link. If fewer unused angles remain than pins needed, invent new ones ONLY from Product facts: a new angle needs a different primary search phrase AND a different feature focus from every used angle (check titles in the ledger), and is added to `angles.json`. Never reuse an angle id; never reuse a title.

## Steps (whole month)

1. **Load tools** with ToolSearch: PinBridge (`list_pinterest_accounts`, `list_boards`, `get_billing_status`, `list_pins`, `list_schedules`, `create_schedule`, `get_schedule`, `list_related_terms`), TaskCreate/TaskUpdate. Make a task list.
2. **Check state**: account healthy, board id, quota remaining, existing pins and schedules (`list_pins`, `list_schedules`, page through all). Compute remaining days (start at least 10 hours from now) and the pin count by the pacing rule.
3. **Get the repo**: `add_repo` with `access: "push"` for `hellonorthlanestudio-stack/rate-calculator`, clone, read `pins/ledger.json` and `pins/angles.json`. If push access fails (GitHub not linked), STOP and tell Abai: link GitHub in claude.ai Settings > Connectors. Do not work around it.
4. **Pick angles and write copy** for every pin (title under 100 characters starting with the searchable phrase; description 2-4 plain sentences, up to 800; destination link with `pinN`). Check each claim against Product facts.
5. **Render images**: write `specs-YYYY-MM.json` (fields in `render_pin.py`), run `python3 -I pins/render_pin.py specs.json out pins/fonts` (install `playwright` Chromium and `@fontsource/fraunces`, `@fontsource/inter` if missing; fonts are in the repo). The script prints a layout check per pin; it must say layout_ok=True. Also look at several PNGs yourself for typos and cut-off text. "Sample data" label only where the card shows invented sample numbers.
6. **Publish images**: copy PNGs to `pins/` in the repo, update ledger/angles/plan files, commit and push. Raw URLs work right after the push. The shell cannot reach github.io or possibly raw hosts, so rely on step 7's dry run media check (must pass).
7. **Schedule**: for each pin, `create_schedule` with `dry_run=true` first (must be valid, including the media check), then the real call. Do not resend after a timeout without checking `list_schedules`.
8. **Verify**: `list_schedules status=scheduled` must show exactly the pins created, with the right run_at, titles and board. Fix mistakes with `update_schedule`.
9. **Record**: update `pins/ledger.json` (last_pin_number, used_angles, titles, months_run) and push.
10. **Report** briefly: pins scheduled (count, date range), quota left, anything that failed, and a reminder that the first published pins should be opened to confirm the image and link are right.

## Copy rules

- Only show features listed under Product facts. No made-up stats, earnings claims or fake testimonials. Row labels drawn on the image's card must come from the product facts, not invented features, and the pin summary to Abai must say so.
- Title: under 100 characters, starts with the searchable phrase. Description up to 800 characters, alt text up to 500.
- Description: 2-4 plain sentences with keywords written naturally, no hashtag lists. Mention Notion's free plan only for free-product pins.
- Vary the headline, the example rows and the badge so pins do not look identical.

## Design spec

- Size 1000x1500. Background #1F4D3A (dark green), white text.
- Badge: pill at about x=70, y=80; background #D7F27A, text #1F4D3A, uppercase, 26px, weight 800 (e.g. "FREE NOTION TEMPLATE", "CREATOR EMAIL TEMPLATES").
- Headline: Fraunces 800, about 104px, line-height 1.02, 3 lines max, starting around y=190. Subline: Inter 36px, color #d9e6df.
- Cream card (#F4F0E8, radius 28px, shadow) starting around y=760, showing a small realistic slice of the template: white rows with a soft border and status tags (overdue: bg #FBE3E0 / text #C2463E; waiting or ends-soon: bg #FDF1D3 / text #9A6A00; paid: bg #E2F1E7 / text #2E6B4F).
- Footer in the bottom 70px: white rounded square logo with a serif "N", "Northlane Studio" in Fraunces 34px, and a lime pill CTA ("Get it free" for free-product pins, "See the template" for paid ones). Keep a gap of at least 40px between the card and the footer.
