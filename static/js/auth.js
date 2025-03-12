// Obsługa rejestracji
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (data.success) {
            showMessage('success', data.message);
            // Możesz automatycznie zalogować użytkownika po rejestracji
        } else {
            showMessage('error', data.message);
        }
    } catch (error) {
        showMessage('error', 'Błąd połączenia z serwerem');
    }
});

// Obsługa logowania
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (data.success) {
            showMessage('success', data.message);
           if (data.redirect) {
              window.location.href = data.redirect;  // Przekierowanie
         }
        } else {
            showMessage('error', data.message);
        }
    } catch (error) {
        showMessage('error', 'Błąd połączenia z serwerem');
    }
});

// Funkcja pomocnicza do wyświetlania komunikatów
function showMessage(type, text) {
    const messagesDiv = document.getElementById('messages');
    const message = document.createElement('div');
    message.className = `alert alert-${type}`;
    message.textContent = text;
    messagesDiv.appendChild(message);
    
    // Autoukrywanie po 5 sekundach
    setTimeout(() => {
        message.remove();
    }, 5000);
}