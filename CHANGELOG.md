# Changelog: Interactive Universe Map

Versions follow `vMAJOR.MINOR`. From now on, the monthly "living universe" data updates (new survey releases and refreshed catalogues) will each bump the minor version, and the changes will be listed here and in the map's **What's new** page.
Dates are in Perth time (AWST, UTC+8).

## Release workflow (beta first)
Every change goes to the **beta** copy first: https://johnrichardszpe-dot.github.io/universe-map/beta/ (folder `beta/` on `main`; it shares the stable `assets/` data files via `../assets/`). Beta shows an orange "BETA vX.Y-beta" badge with a link back to stable.
The stable map (`index.html` at the site root) is only updated after the owner OKs the beta. To promote: copy `beta/index.html` to `index.html`, change `../assets/` back to `assets/`, remove the BETA badge/title, set the version, keep the GoatCounter `<script data-goatcounter=...>` snippet just before `</body>` (both pages), tag `vX.Y`, publish a GitHub release.
(`tools/make_beta.py` builds the v1.4 beta page from the stable page.)

## v2.2 - 24 Oct 2026 (stable)
- Promoted v2.1-beta-2 (Voyager 1 and 2) to stable, approved by the owner.

## v2.1-beta-2 - 24 Oct 2026 (beta only, not yet in stable)
- Added Voyager 1 (172 AU) and Voyager 2 (144 AU) to the Solar System view at their real directions (JPL Horizons, 14 Oct 2026), on the same squeezed distance scale as the planets, with a dashed line from the Sun and an info card. Chip's Voyager answer now flies to Voyager 1.

## v2.1 - 23 Oct 2026 (stable)
Promoted from beta (v2.0-beta-2 to beta-4), approved by the owner after testing on his Galaxy S9.
- Fixed the oversized map canvas on high-resolution phones, which put labels, the Chip ring and taps away from their targets.
- Solar System labels sit beside bodies; the Sun glows; the target is lifted above the info panel on phones.
- Chip fact corrections, GJ 411 distance fix, wrong Milky Way toast removed, Install button moved clear of the Time-travel panel, one tap on Chip opens the menu.
- New: if the map is installed or already open when an update arrives, it now shows "Universe Map was just updated. Tap to reload."

## v2.0-beta-4 - 23 Oct 2026 (beta only, not yet in stable)
- Fixed a display bug on high-resolution phones: the map canvas was drawn about 1.5 times bigger than the screen and cropped, so labels, the Chip ring and tap targets sat away from their stars and planets. The canvas now fills the screen exactly. (The same bug is in the stable map until this is promoted.)

## v2.0-beta-3 - 23 Oct 2026 (beta only, not yet in stable)
- Chip facts corrected: Lalande 21185 and M32 distances, Voyager, Io, Kepler, Polaris wording; Jupiter, Saturn and Uranus moon counts now say "at least N" until checked against NASA.
- GJ 411 exoplanet distance fixed (was a bad catalogue value of 5.68 pc, now 2.55 pc).
- Removed a wrong "You're at the Milky Way" toast that could appear while flying to Andromeda.
- Install-app button no longer covers the Names / Time-travel panel on phones.
- One tap on Chip now always opens its menu (previously needed a second tap after a tour or answer).

## v2.0-beta-2 - 23 Oct 2026 (beta only, not yet in stable)
- Solar System labels now sit beside each body instead of on top of it, and the selected body shows a single target label (no more doubled "Sun" text over the Sun).
- The Sun has a soft glow so Chip's ring and beam clearly point at the real Sun, not the word.
- On phones, when Chip or a tap flies to a planet or star and the info panel opens, the target is parked in the free area above the panel so it is never hidden behind it.

## v2.0 - 16 Oct 2026: Chip the alien guide + installable app
Promoted from v1.9-beta (+ suggestion box) after owner approval. Built with `tools/make_root20.py` (beta -> root: `../assets/` -> `assets/`, no BETA badge/title, own manifest and SW).
- Chip the alien guide: draggable UFO helper; Quick (6) and Full (14) tours; Ask Chip (185 sourced facts in `chip_facts.json`, offline fuzzy matching in `chip_match.js`); highlight ring, tractor beam and edge arrow for on-map targets.
- Suggest something (Chip's menu and the ? help screen): opens a prefilled GitHub issue (template `.github/ISSUE_TEMPLATE/suggestion.md`, label `suggestion`) or an email to the owner. No backend, no secrets.
- Installable PWA: root manifest id/start_url/scope `/universe-map/`, service worker cache `umap-v2.0-1`. The root SW ignores `/universe-map/beta/`; beta keeps its own manifest (`/universe-map/beta/`) and SW cache (`umap-beta-...`), so the two apps install and update separately.
- Beta is now identical to stable plus the BETA badge (v2.0-beta).

## v1.5.1 - 15 Oct 2026
- Added privacy-friendly GoatCounter visit counting (no cookies, no personal tracking) to stable and beta. Stats-only change, pushed straight to stable at the owner's request.

## v1.5 - 14 Oct 2026
Promoted from v1.5-beta after owner approval (live beta re-tested desktop + phone, zero JS errors, ~60 fps). Also: compact 2-row phone bar; star taps near the Sun pick whichever target is closest on screen.
Rule: only real, known data; sources cited in About/README.
- Tap any galaxy dot (tap vs drag threshold, so rotating still works): highlight, smooth fly-to, info box with survey, redshift, comoving distance (Mpc + light-years), lookback time, RA/Dec, and the closest named index object. Redshift/lookback are worked back from the stored position with Planck 2018; catalogue IDs are not stored in the compressed data, so none is shown.
- Enter the Milky Way (button, Milky Way info box, or a prompt when zoomed right in): Sun, 8 planets, Pluto and Ceres at real heliocentric positions for 14 Oct 2026 (JPL Horizons), facts from the NASA Planetary Fact Sheet (NSSDCA, updated 18 Mar 2025) and per-planet sheets; Earth: life, ~8.7 million estimated eukaryote species (Mora et al. 2011, PLoS Biol 9(8):e1001127). 4,814 exoplanet host stars / 6,417 confirmed planets with known distance from the NASA Exoplanet Archive pscomppars table (TAP, 14 Oct 2026; 6,445 planets total), at true RA/Dec/distance, coloured by size class; missing values shown as 'unknown'. Solar System drawn enlarged (not to scale), labelled. Back to universe button. Data lazy-loaded (beta/solar.js, beta/exoplanets.js).
- Measure / waypoints: tap points in order; legs + total in Mpc/light-years (AU/light-years in the Milky Way view, using true positions); undo, clear, save routes (this device), fly the route.

## v1.4 - 14 Oct 2026
Promoted from v1.4-beta after owner approval (beta tested live, desktop + phone, zero JS errors).

- Simple mode (default): clean screen with Fly to, Find, zoom +/-, Home, help, a big Names on/off button and a Time-travel slider. "Advanced" reveals the full panel (colours, surveys, lookback range, 724k points, dot size, filament/predicted/conceptual layers). Choice remembered.
- Home glides smoothly (ease in/out, 1.5 s) back to the default Milky Way-centred view; zoom buttons, Fly-to and search also glide; touching the map cancels a glide.
- Smoothness: render on demand (only when the camera or settings change), label decluttering throttled to every 120 ms while moving (cheap re-positioning in between), cached UI rectangles (no per-frame layout reads), scale bar only updates the DOM when it changes, no per-frame vector allocations, pixel ratio capped at 1.5 on phones, time sweep animated per-frame instead of 120 ms steps.
- Fixes: zoom buttons did nothing when very close (Local Group close-ups); keyboard fly keys could stick after the window lost focus; Ctrl/Cmd shortcuts triggered fly keys.

## v1.3 (2026-10-14)
- **Galaxy name index + search:** 4,326 named objects. Tap 🔍 Find (top bar or panel) to search by name with autocomplete (Andromeda, M87, Whirlpool, Centaurus A, NGC 253, Abell 3558...) or browse by group: Local Group, Messier & famous galaxies, Nearby galaxies (Local Volume), Bright NGC/IC galaxies, Galaxy clusters, Superclusters, Walls & voids.
- Picking an entry flies the camera there, adds a gold marker and label, and shows an info box (type, group, distance in Mpc/kpc and light-years, distance method, redshift, aliases).
- Very close Local Group galaxies get a close-up fly-in. The Milky Way marker and camera clipping now scale with zoom.
- Sources: Updated Nearby Galaxy Catalog (Karachentsev+ 2013, VizieR J/AJ/145/101) and SIMBAD (CDS). See README.
- Versioning: a version tag in the corner, a **What's new** page, a one-time "New in v1.3" message, this changelog, and git tags with GitHub releases.
- The scale bar now switches to kpc and thousands of light-years when zoomed right in.

## v1.2 (2026-10-13 20:45)
- Structure labels no longer stack on phones: they avoid each other on screen (with leader lines), lower-priority names hide until you zoom in, and the font is smaller on mobile.

## v1.1 (2026-10-13 20:24)
- Easier navigation: collapsible side panel (☰/✕, remembered, collapsed by default on phones); on-screen zoom in/out, reset and help buttons; a "Fly to" menu for labelled structures; touch, pinch and drag; a first-visit help screen.
- Plain-English "?" tooltips for Mpc, redshift, comoving distance and lookback time; distances shown in both Mpc and light-years.
- Lighter default of 100,000 galaxies (all ~724,000 optional).

## v1.0 (2026-10-13 20:15)
- First public release: about 724,000 real galaxies from 2MRS, SDSS DR17 and DESI DR1 in 3D (comoving distance, Planck18), with a lookback-time (4D) slider and colouring, named structures, and optional filament web, predicted (model) and conceptual-lattice layers. Includes the About panel with sources, licences and accuracy notes.
