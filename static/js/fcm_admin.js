import { initializeApp }    from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getMessaging, getToken, onMessage }
                             from "https://www.gstatic.com/firebasejs/9.23.0/firebase-messaging.js";

const firebaseConfig = {

  apiKey: "AIzaSyDRdh7NOorxSHvf0hPEuglOOZu2Lj4KEg0",
    authDomain: "instafret-django.firebaseapp.com",
    projectId: "instafret-django",
    storageBucket: "instafret-django.firebasestorage.app",
    messagingSenderId: "805066432902",
    appId: "1:805066432902:web:b4e23e578c0f62e3478c07",
    measurementId: "G-V6ZH65PJYC"
};
const vapidKey = "BLAyZhnpG7UT8wgYMK4X0NNSyQxdJKJuBrVDicielUmiZhtKoZMvXuubUhrXeACZrWsBhANrD7gDmMV3iL-zwEw";

const app       = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

/* ---- enregistrement SW + token ---- */
navigator.serviceWorker.register("/firebase-messaging-sw.js").then(reg => {
    return getToken(messaging, { vapidKey, serviceWorkerRegistration: reg });
}).then(tok => {
    if (tok)
        fetch("/api/device-tokens/", {
            method : "POST",
            headers: {
                "Content-Type":"application/json",
                "X-CSRFToken" : Cookies.get("csrftoken")
            },
            body   : JSON.stringify({ token: tok, user_agent: navigator.userAgent })
        });
}).catch(err => console.warn("FCM token error", err));

/* ---- réception temps-réel ---- */
onMessage(messaging, payload => {
    const badge = document.getElementById("notif-badge");
    const menu  = document.getElementById("notif-menu");
    const beep  = document.getElementById("notif-sound");

    badge.textContent = parseInt(badge.textContent || 0) + 1;
    badge.style.display = "inline-block";

    menu.querySelector(".small")?.remove();  // retire “Aucune notification”
    const link = document.createElement("a");
    link.href        = payload.data?.url || "#";
    link.className   = "dropdown-item";
    link.innerHTML   =
        `<strong>${payload.notification.title}</strong><br>
         <small>${payload.notification.body}</small>`;
    menu.prepend(link);

    beep.currentTime = 0;
    beep.play();
});
