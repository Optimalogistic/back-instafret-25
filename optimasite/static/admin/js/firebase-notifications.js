class AdminNotificationManager {
    constructor() {
        this.firebaseApp = null;
        this.messaging = null;
        this.notificationBell = document.getElementById('notification-bell');
        this.notificationCount = document.getElementById('notification-count');
        this.notificationDropdown = document.getElementById('notification-dropdown');
        this.notificationList = document.getElementById('notification-list');
        this.markAllReadBtn = document.getElementById('mark-all-read');
        
        this.unreadCount = 0;
        this.notifications = [];
        
        this.initializeFirebase();
        this.setupEventListeners();
        this.loadExistingNotifications();
    }
    
    async initializeFirebase() {
        try {
            // Initialiser Firebase
            this.firebaseApp = firebase.initializeApp(window.FIREBASE_CONFIG);
            this.messaging = firebase.messaging();
            
            // Demander permission
            await this.requestNotificationPermission();
            
            // Configurer les listeners
            this.setupFirebaseListeners();
            
            console.log('Firebase initialisé avec succès');
        } catch (error) {
            console.error('Erreur initialisation Firebase:', error);
        }
    }
    
    async requestNotificationPermission() {
        try {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                console.log('Permission accordée');
                await this.getAndSaveToken();
            } else {
                console.log('Permission refusée');
            }
        } catch (error) {
            console.error('Erreur permission:', error);
        }
    }
    
    async getAndSaveToken() {
        try {
            const token = await this.messaging.getToken({
                vapidKey: window.VAPID_KEY
            });
            
            if (token) {
                console.log('Token FCM obtenu:', token);
                await this.saveTokenToServer(token);
            }
        } catch (error) {
            console.error('Erreur récupération token:', error);
        }
    }
    
    async saveTokenToServer(token) {
        try {
            const response = await fetch('/api/device-tokens/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.CSRF_TOKEN,
                },
                body: JSON.stringify({
                    token: token,
                    user_agent: navigator.userAgent,
                    user_id: window.USER_ID
                })
            });
            
            if (response.ok) {
                console.log('Token sauvegardé sur le serveur');
            }
        } catch (error) {
            console.error('Erreur sauvegarde token:', error);
        }
    }
    
    setupFirebaseListeners() {
        // Messages en premier plan
        this.messaging.onMessage((payload) => {
            console.log('Message reçu en premier plan:', payload);
            this.handleIncomingNotification(payload);
        });
    }
    
    setupEventListeners() {
        // Clic sur la cloche
        this.notificationBell.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown();
        });
        
        // Fermer dropdown en cliquant ailleurs
        document.addEventListener('click', (e) => {
            if (!this.notificationBell.contains(e.target) && 
                !this.notificationDropdown.contains(e.target)) {
                this.hideDropdown();
            }
        });
        
        // Marquer tout comme lu
        this.markAllReadBtn.addEventListener('click', () => {
            this.markAllAsRead();
        });
    }
    
    handleIncomingNotification(payload) {
        const notification = {
            id: Date.now(),
            title: payload.notification.title,
            body: payload.notification.body,
            type: payload.data.type || 'general',
            url: payload.data.url || '#',
            sound: payload.data.sound || 'notification.mp3',
            timestamp: new Date(),
            read: false
        };
        
        // Ajouter à la liste
        this.addNotification(notification);
        
        // Jouer le son
        this.playNotificationSound(notification.sound);
        
        // Animer la cloche
        this.animateBell();
        
        // Afficher notification navigateur si en arrière-plan
        if (document.hidden) {
            this.showBrowserNotification(notification);
        }
    }
    
    addNotification(notification) {
        this.notifications.unshift(notification);
        this.renderNotifications();
        this.updateNotificationCount();
        
        // Limiter à 50 notifications
        if (this.notifications.length > 50) {
            this.notifications = this.notifications.slice(0, 50);
        }
        
        // Sauvegarder dans localStorage
        this.saveNotificationsToStorage();
    }
    
    renderNotifications() {
        if (this.notifications.length === 0) {
            this.notificationList.innerHTML = '<div class="no-notifications">Aucune notification</div>';
            return;
        }
        
        const notificationsHTML = this.notifications.map(notification => `
            <div class="notification-item ${notification.read ? '' : 'unread'}" 
                 data-id="${notification.id}" 
                 data-url="${notification.url}">
                <div class="notification-content">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-body">${notification.body}</div>
                    <div class="notification-meta">
                        <span class="notification-time">${this.formatTime(notification.timestamp)}</span>
                        <span class="notification-type ${notification.type}">${this.getTypeLabel(notification.type)}</span>
                    </div>
                </div>
            </div>
        `).join('');
        
        this.notificationList.innerHTML = notificationsHTML;
        
        // Ajouter les event listeners
        this.notificationList.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const id = parseInt(item.dataset.id);
                const url = item.dataset.url;
                
                this.markAsRead(id);
                
                if (url && url !== '#') {
                    window.open(url, '_blank');
                }
            });
        });
    }
    
    updateNotificationCount() {
        this.unreadCount = this.notifications.filter(n => !n.read).length;
        
        if (this.unreadCount > 0) {
            this.notificationCount.textContent = this.unreadCount > 99 ? '99+' : this.unreadCount;
            this.notificationCount.classList.remove('hidden');
        } else {
            this.notificationCount.classList.add('hidden');
        }
    }
    
    markAsRead(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
            this.renderNotifications();
            this.updateNotificationCount();
            this.saveNotificationsToStorage();
        }
    }
    
    markAllAsRead() {
        this.notifications.forEach(n => n.read = true);
        this.renderNotifications();
        this.updateNotificationCount();
        this.saveNotificationsToStorage();
    }
    
    playNotificationSound(soundFile) {
        const soundType = soundFile.replace('.mp3', '').replace('.wav', '');
        const audioElement = document.getElementById(`${soundType}-sound`);
        
        if (audioElement) {
            audioElement.currentTime = 0;
            audioElement.play().catch(e => {
                console.log('Impossible de jouer le son:', e);
            });
        }
    }
    
    animateBell() {
        this.notificationBell.classList.add('shake');
        setTimeout(() => {
            this.notificationBell.classList.remove('shake');
        }, 600);
    }
    
    showBrowserNotification(notification) {
        if (Notification.permission === 'granted') {
            const browserNotif = new Notification(notification.title, {
                body: notification.body,
                icon: '/static/admin/img/notification-icon.png',
                badge: '/static/admin/img/badge-icon.png',
                tag: `admin-notification-${notification.id}`,
                requireInteraction: true
            });
            
            browserNotif.onclick = () => {
                window.focus();
                if (notification.url && notification.url !== '#') {
                    window.open(notification.url, '_blank');
                }
                browserNotif.close();
            };
            
            // Fermer automatiquement après 10 secondes
            setTimeout(() => {
                browserNotif.close();
            }, 10000);
        }
    }
    
    toggleDropdown() {
        const isHidden = this.notificationDropdown.classList.contains('hidden');
        if (isHidden) {
            this.showDropdown();
        } else {
            this.hideDropdown();
        }
    }
    
    showDropdown() {
        this.notificationDropdown.classList.remove('hidden');
        this.renderNotifications();
    }
    
    hideDropdown() {
        this.notificationDropdown.classList.add('hidden');
    }
    
    formatTime(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        
        if (minutes < 1) return 'À l\'instant';
        if (minutes < 60) return `Il y a ${minutes}min`;
        if (hours < 24) return `Il y a ${hours}h`;
        if (days < 7) return `Il y a ${days}j`;
        
        return timestamp.toLocaleDateString('fr-FR');
    }
    
    getTypeLabel(type) {
        const labels = {
            'new_user': 'Utilisateur',
            'new_request': 'Demande',
            'status_update': 'Statut',
            'new_offer': 'Offre'
        };
        return labels[type] || 'Général';
    }
    
    saveNotificationsToStorage() {
        try {
            localStorage.setItem('admin_notifications', JSON.stringify(this.notifications));
        } catch (error) {
            console.error('Erreur sauvegarde notifications:', error);
        }
    }
    
    loadExistingNotifications() {
        try {
            const saved = localStorage.getItem('admin_notifications');
            if (saved) {
                this.notifications = JSON.parse(saved).map(n => ({
                    ...n,
                    timestamp: new Date(n.timestamp)
                }));
                this.renderNotifications();
                this.updateNotificationCount();
            }
        } catch (error) {
            console.error('Erreur chargement notifications:', error);
        }
    }
}

// Initialiser le gestionnaire quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    if (window.USER_ID && window.FIREBASE_CONFIG) {
        new AdminNotificationManager();
    }
});
