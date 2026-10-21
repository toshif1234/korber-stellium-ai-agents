# Körber Stellium – AI Agents pages (preview build)

Static HTML preview of the proposed AI Agents section for koerber-stellium.com.
Open `index.html` in a browser to view it locally.

## Contents
| File | Page | Proposed live URL |
|---|---|---|
| index.html | AI Agents hub | /our-services/innovation/ai-agents/ |
| ewm-outbound-supervisor-agent.html | SAP EWM Outbound Supervisor | /our-services/innovation/ai-agents/sap-ewm-outbound-supervisor-agent/ |
| tm-invoice-dispute-agent.html | SAP TM Freight Invoice Dispute | /our-services/innovation/ai-agents/sap-tm-freight-invoice-dispute-agent/ |
| dm-order-release-agent.html | SAP DM Order Release | /our-services/innovation/ai-agents/sap-dm-order-release-agent/ |
| placement-plan.html | Placement & SEO plan (internal, not for publishing) | – |
| styles.css | Shared styles (brand palette, Arial) | – |
| logo-black.png, logo-white.png | Körber Stellium logos from the 2026 template | – |
| media/*.mp4, media/*.jpg | Agent videos and poster / share images | /wp-content/uploads/ai-agents/ |
| source/build.py | Python script that generates the HTML pages | – |

## Go-live checklist
1. Rebuild the pages in Elementor (or import the HTML) using this layout and copy.
2. Upload `media/` files to `/wp-content/uploads/ai-agents/` (the VideoObject and og:image tags point there).
3. Copy each page's title, meta description and canonical into the SEO plugin; keep the JSON-LD blocks.
4. Change `<meta name="robots" content="noindex, nofollow">` to `index, follow` on the four public pages.
5. Remove the black "Preview for review" bar at the top of each page.
6. Add the pages to the XML sitemap and submit in Google Search Console.
7. Add internal links from the existing pages listed in placement-plan.html.

## Regenerating
`python3 source/build.py` writes the pages to the folder set in `OUT` at the top of the script
(set it to this folder first). The hub is written without a doctype in the script; the copy in this
zip has been wrapped as a full HTML document.
