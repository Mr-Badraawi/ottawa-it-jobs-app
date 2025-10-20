self.addEventListener('push', function(event) {
  let data = 'New notification';
  try {
    data = event.data.text();
  } catch(e) {}
  const title = 'Ottawa IT Jobs';
  const options = {
    body: data,
    icon: '/static/icon-192.png'
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

// basic fetch handler (cache omitted for simplicity)
self.addEventListener('install', function(e){ self.skipWaiting(); });
self.addEventListener('activate', function(e){ self.clients.claim(); });