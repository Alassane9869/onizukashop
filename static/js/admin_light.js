// ONIZOUKA SHOP - Forçage du Mode Clair Lumineux pour l'Administration Unfold
(function() {
    function enforceLightMode() {
        try {
            // Réinitialiser les clés de persistance d'Alpine / Unfold vers le mode clair
            localStorage.setItem('adminTheme', JSON.stringify('light'));
            localStorage.setItem('_x_adminTheme', JSON.stringify('light'));
            
            // Retirer immédiatement toute classe sombre sur le document
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
            }
            document.documentElement.classList.add('light');
            
            // Si Alpine.js a déjà initialisé un store ou des données
            if (window.Alpine && window.Alpine.store) {
                const store = window.Alpine.store('unfold');
                if (store && store.theme) {
                    store.theme = 'light';
                }
            }
        } catch (e) {
            console.error('Erreur forcage light mode unfold:', e);
        }
    }

    // Exécution immédiate avant le rendu
    enforceLightMode();

    // Ré-exécution au chargement du DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enforceLightMode);
    } else {
        enforceLightMode();
    }

    // Observer pour empêcher la ré-injection de la classe dark
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                    document.documentElement.classList.add('light');
                }
            }
        });
    });
    observer.observe(document.documentElement, { attributes: true });
})();
