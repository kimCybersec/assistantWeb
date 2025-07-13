const CACHE_NAME = "assistant-cache-v1";
const ASSETS_TO_CACHE = [
  "/",
  "/templates/index.html",
  "/templates/summary.html",
  "/templates/base.html"
  "/static/style.css",
  "/static/script.js",
  "/manifest.json",
  "/public/logo.jpg",
  "/templates/generate.html"
];

self.addEventListener("install", event => {
  console.log("[ServiceWorker] Install");
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  console.log("[ServiceWorker] Activate");
  event.waitUntil(
    caches.keys().then(keyList =>
      Promise.all(
        keyList.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
