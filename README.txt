Interactive Universe Map - by John Richards, Manjimup WA ()
Open index.html in any modern browser (Chrome, Edge, Firefox, Safari). It works offline; keep the "assets" folder next to index.html.
Real galaxy data: 2MRS (Huchra et al. 2012), SDSS DR17, DESI DR1 (CC BY 4.0). See "About this map" inside for credits and accuracy notes.
tools/build_data.py rebuilds the data files; tools/verification.json lists the coordinate and structure checks.

Version: v1.3 (see CHANGELOG.md, the in-map "What's new" page, and GitHub releases/tags v1.0 to v1.3).
Monthly "living universe" data updates will bump the version going forward.

Galaxy name index (v1.3, assets/galaxy_index.js, 4,326 entries):
- Updated Nearby Galaxy Catalog, Karachentsev, Makarov & Kaisina 2013, AJ 145, 101 (VizieR J/AJ/145/101): Local Group and Local Volume galaxies with measured distances.
- SIMBAD astronomical database (CDS, Strasbourg; Wenger et al. 2000, A&AS 143, 9), queried October 2026 via TAP: common names, Messier and bright (B<13) NGC/IC galaxies, Abell and named clusters and groups, and published distance measurements (median of non-redshift distances, used when cz < 3000 km/s).
- Beyond that, distances come from redshift (Planck18 comoving). Several superclusters, walls and voids use approximate literature positions (marked "approx.").
- Built by tools/build_index.py. Positions use the same conversion as the map; checked: Virgo, Coma, Perseus, Shapley and the Great Walls match the existing labels to within 0.01 Mpc.


BETA WORKFLOW
All changes are published first at https://johnrichardszpe-dot.github.io/universe-map/beta/ (folder beta/, shares ../assets/). The stable map at the site root is only updated after the owner approves the beta. See CHANGELOG.md for the promotion steps.

v1.5-beta MILKY WAY VIEW SOURCES
NASA Planetary Fact Sheet (nssdc.gsfc.nasa.gov/planetary/factsheet/); JPL Horizons (ssd.jpl.nasa.gov/horizons) planet positions for 2026-10-14; Ceres: NASA Dawn / JPL Horizons; Mora et al. 2011 PLoS Biology 9(8): e1001127 (8.7 million species); NASA Exoplanet Archive pscomppars (exoplanetarchive.ipac.caltech.edu), 6,445 planets / 6,417 with distance / 4,814 hosts, downloaded 2026-10-14. This research has made use of the NASA Exoplanet Archive, operated by Caltech under contract with NASA under the Exoplanet Exploration Program.

VISIT COUNTING
The site uses GoatCounter (https://www.goatcounter.com), a privacy-friendly open-source visit counter: no cookies, no personal tracking. Dashboard: https://universemap.goatcounter.com
