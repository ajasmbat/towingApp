// self.addEventListener('push', function(event) {
//   const eventInfo = event.data.text();
//   const data = JSON.parse(eventInfo);
//   const head = data.head || 'New Notification 🕺🕺';
//   const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';
//   const url = data.url;

//   event.waitUntil(
//     self.registration.showNotification(head, {
//       body: body,
//       icon: 'https://i.imgur.com/MZM3K5w.png'
//     })
//   );
// });

// // Add listener for notificationclick event
// self.addEventListener('notificationclick', function(event) {
//     event.notification.close(); // Close the notification
    
    
    
//     event.notification.data.url = "google.com";


//   // Perform the desired action when the notification is clicked
//   const clickedNotification = event.notification;
//   const url = clickedNotification.data.url;

//   // Open the URL in a new window or tab
//   if (url) {
//     clients.openWindow(url);
//   }
// });

self.addEventListener('push', function(event) {
  const eventInfo = event.data.text();
  const data = JSON.parse(eventInfo);
  const head = data.head || 'New Notification 🕺🕺';
  const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';
  const url = data.url;

  event.waitUntil(
    self.registration.showNotification(head, {
      body: body,
      icon: 'https://i.imgur.com/MZM3K5w.png',
      data: { url: url } // Pass the URL in the data object
    })
  );
});

// Add listener for notificationclick event
self.addEventListener('notificationclick', function(event) {
  event.notification.close(); // Close the notification

  const url = event.notification.data.url;

  // Open the URL in a new window or tab
  if (url) {
    event.waitUntil(clients.openWindow(url));
  }
});
