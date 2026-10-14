# Changelog: Interactive Universe Map

Versions follow `vMAJOR.MINOR`. From now on, the monthly "living universe" data updates (new survey releases and refreshed catalogues) will each bump the minor version, and the changes will be listed here and in the map's **What's new** page.
Dates are in Perth time (AWST, UTC+8).

## Release workflow (beta first)
Every change goes to the **beta** copy first: https://johnrichardszpe-dot.github.io/universe-map/beta/ (folder `beta/` on `main`; it shares the stable `assets/` data files via `../assets/`). Beta shows an orange "BETA vX.Y-beta" badge with a link back to stable.
The stable map (`index.html` at the site root) is only updated after the owner OKs the beta. To promote: copy `beta/index.html` to `index.html`, change `../assets/` back to `assets/`, remove the BETA badge/title, set the version, tag `vX.Y`, publish a GitHub release.
(`tools/make_beta.py` builds the v1.4 beta page from the stable page.)

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
