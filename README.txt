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
