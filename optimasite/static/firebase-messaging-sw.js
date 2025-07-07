/* service-worker FCM */
importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-messaging-compat.js');

firebase.initializeApp({
    apiKey: "AIzaSyDRdh7NOorxSHvf0hPEuglOOZu2Lj4KEg0",
    authDomain: "instafret-django.firebaseapp.com",
    projectId: "instafret-django",
    storageBucket: "instafret-django.firebasestorage.app",
    messagingSenderId: "805066432902",
    appId: "1:805066432902:web:b4e23e578c0f62e3478c07",
    measurementId: "G-V6ZH65PJYC"
});

const messaging = firebase.messaging();

/* Affiche une notif native quand l’admin est fermé */
messaging.onBackgroundMessage(payload => {
    self.registration.showNotification(payload.notification.title, {
        body : payload.notification.body,
        data : payload.data,
        icon : '/static/img/bell.png'
    });
});
