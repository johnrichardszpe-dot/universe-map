// Universe Map BETA service worker. Bump VERSION on every release so old caches are dropped.
const VERSION = "v1.9-beta-1";
const CACHE = "umap-beta-" + VERSION;
const SHELL = [
  "./", "./index.html", "./manifest.webmanifest", "./solar.js", "./exoplanets.js",
  "./icons/icon-192.png", "./icons/icon-512.png", "./icons/maskable-512.png", "./icons/apple-touch-icon.png", "./icons/alien.png", "./chip_match.js", "./chip_facts.json",
  "../assets/three.min.js", "../assets/OrbitControls.js", "../assets/data_core.js",
  "../assets/layers.js", "../assets/structures.js"
];
// Large optional files (data_more.js, galaxy_index.js) are cached on first use.
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL.map(u => new Request(u, {cache: "reload"})))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("umap-beta-") && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return; // GoatCounter etc. go straight to network
  if (req.mode === "navigate" || url.pathname.endsWith(".html") || url.pathname.endsWith("/beta/")) {
    // Network first for the page, so a new release shows up immediately when online.
    e.respondWith(fetch(req).then(r => { const c = r.clone(); caches.open(CACHE).then(ca => ca.put(req, c)); return r; })
      .catch(() => caches.match(req, {ignoreSearch: true}).then(r => r || caches.match("./index.html"))));
    return;
  }
  // Stale-while-revalidate for scripts/data/icons: fast from cache, refreshed in the background.
  e.respondWith(caches.open(CACHE).then(ca => ca.match(req, {ignoreSearch: true}).then(hit => {
    const net = fetch(req).then(r => { if (r.ok) ca.put(req, r.clone()); return r; });
    if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
    return net;
  })));
});
