document.addEventListener('DOMContentLoaded', function() {
    // Obsługa stanu ładowania
    const setLoadingState = (isLoading) => {
        const loader = document.getElementById('global-loader');
        if (loader) {
            loader.style.display = isLoading ? 'block' : 'none';
        }
    };

    // Obsługa błędów
    const showErrorToast = (message) => {
        const toast = document.createElement('div');
        toast.className = 'error-toast';
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fa-solid fa-circle-exclamation"></i>
                <span>${message}</span>
            </div>
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 5000);
    };

    // Weryfikacja sesji
    const checkAuth = async () => {
        try {
            const response = await fetch('/api/check-auth', {
                credentials: 'include'
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    };

    // Obsługa kliknięć w nawigację
    const handleNavigation = async (event) => {
        const link = event.currentTarget;
        const path = link.getAttribute('href');

        // Tymczasowa obsługa nieistniejących stron
        const existingPaths = ['/admin/questions', '/admin/surveys'];
        if (!existingPaths.includes(path)) {
            event.preventDefault();
            showErrorToast('Ta funkcja jest w trakcie implementacji');
            return;
        }

        event.preventDefault();
        setLoadingState(true);

        if (!(await checkAuth())) {
            window.location.href = '/login';
            return;
        }

        try {
            const response = await fetch(path, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                window.location.href = path;
            }
        } catch (error) {
            showErrorToast('Błąd połączenia z serwerem');
        } finally {
            setLoadingState(false);
        }
    };

    // Inicjalizacja
    const init = () => {
        // Podpięcie event listenerów
        document.querySelectorAll('.dashboard-btn').forEach(link => {
            link.addEventListener('click', handleNavigation);
        });

        // Aktualny aktywny link
        const currentPath = window.location.pathname;
        document.querySelectorAll(`a[href="${currentPath}"]`).forEach(link => {
            link.classList.add('active');
        });

        // Symulacja live danych
        setInterval(() => {
            document.querySelectorAll('.notification-badge').forEach(badge => {
                badge.textContent = Math.floor(Math.random() * 20);
            });
        }, 10000);
    };

    // Logout handler
    document.getElementById('logout-btn')?.addEventListener('click', async (e) => {
        e.preventDefault();
        if (confirm('Czy na pewno chcesz się wylogować?')) {
            await fetch('/logout', { method: 'POST' });
            window.location.href = '/login';
        }
    });

    // Inicjalizacja
    init();
});