// Service worker : garde l'application en cache pour qu'elle s'ouvre sans connexion.
// Pour publier une nouvelle version, changer VERSION.
const VERSION = 'correcteur-v3';
const POLICES = 'correcteur-polices';
const COQUILLE = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(VERSION).then((c) => c.addAll(COQUILLE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((cles) => Promise.all(cles.filter((k) => k !== VERSION && k !== POLICES).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Polices Google : cache d'abord, mise à jour en arrière-plan.
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(
      caches.open(POLICES).then(async (c) => {
        const enCache = await c.match(req);
        const reseau = fetch(req)
          .then((rep) => { if (rep.ok || rep.type === 'opaque') c.put(req, rep.clone()); return rep; })
          .catch(() => enCache);
        return enCache || reseau;
      })
    );
    return;
  }

  if (url.origin !== self.location.origin) return;

  // Application : la version en cache s'affiche tout de suite, la version en ligne la remplace pour le lancement suivant.
  const cle = req.mode === 'navigate' ? './index.html' : req;
  e.respondWith(
    caches.open(VERSION).then(async (c) => {
      const enCache = await c.match(cle, { ignoreSearch: true });
      const reseau = fetch(req)
        .then((rep) => { if (rep.ok) c.put(cle, rep.clone()); return rep; })
        .catch(() => enCache);
      return enCache || reseau;
    })
  );
});
