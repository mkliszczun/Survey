document.addEventListener('DOMContentLoaded', function() {
    const questionTypeSelect = document.getElementById('question_type');
    const answersSection = document.getElementById('answers-section');
    const answersContainer = document.getElementById('answers-container');
    const addAnswerBtn = document.getElementById('add-answer-btn');
    const form = document.getElementById('add-question-form');
    const messageArea = document.getElementById('message-area');

    // Pokaż/ukryj sekcję odpowiedzi w zależności od typu pytania
    questionTypeSelect.addEventListener('change', function() {
        if (this.value === 'choice') {
            answersSection.style.display = 'block';
            // Upewnij się, że jest przynajmniej jedno pole odpowiedzi, jeśli go nie ma
            if (answersContainer.children.length === 0) {
                 addAnswerField();
            }
        } else {
            answersSection.style.display = 'none';
        }
    });

    // Dodaj nowe pole odpowiedzi
    function addAnswerField() {
        const div = document.createElement('div');
        div.classList.add('answer-input-group');

        const input = document.createElement('input');
        input.type = 'text';
        input.name = 'choices[]'; // Nazwa zgodna z oczekiwaniem (lub do zmiany)
        input.classList.add('answer-input');
        input.placeholder = 'Treść odpowiedzi';

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('remove-answer-btn');
        removeBtn.innerHTML = '&times;'; // Krzyżyk jako ikona usunięcia
        removeBtn.title = 'Usuń odpowiedź';
        removeBtn.addEventListener('click', function() {
            // Nie usuwaj ostatniego pola odpowiedzi
            if (answersContainer.children.length > 1) {
                 div.remove();
            } else {
                // Możesz dać komunikat lub po prostu nic nie robić
                alert('Musi pozostać przynajmniej jedno pole odpowiedzi.');
            }
        });

        div.appendChild(input);
        div.appendChild(removeBtn);
        answersContainer.appendChild(div);
    }

    addAnswerBtn.addEventListener('click', addAnswerField);

    // Obsługa wysyłania formularza
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Zatrzymaj domyślne wysyłanie formularza
        messageArea.style.display = 'none'; // Ukryj poprzednie komunikaty
        messageArea.className = 'message-area'; // Resetuj klasy

        const questionContent = document.getElementById('question_content').value.trim();
        const questionType = questionTypeSelect.value;
        let choices = [];

        // Podstawowa walidacja po stronie klienta
        if (!questionContent || !questionType) {
            showMessage('Wypełnij treść pytania i wybierz typ.', 'error');
            return;
        }

        if (questionType === 'choice') {
            const answerInputs = answersContainer.querySelectorAll('.answer-input');
             choices = Array.from(answerInputs)
                           .map(input => input.value.trim())
                           .filter(value => value !== ''); // Zbierz tylko niepuste odpowiedzi

            if (choices.length === 0) {
                showMessage('Dodaj przynajmniej jedną odpowiedź dla pytania typu "choice".', 'error');
                return;
            }
        }

        // Przygotuj dane JSON
        const dataToSend = {
            question_content: questionContent,
            question_type: questionType,
        };
        // Dodaj odpowiedzi tylko jeśli typ to 'choice' (Backend tego oczekuje)
        if (questionType === 'choice') {
            dataToSend.choices = choices;
        }

        // Wyślij dane do backendu
        fetch(form.action || window.location.pathname, { // Użyj akcji formularza lub bieżącego URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Możesz potrzebować dodać nagłówek CSRF, jeśli używasz Flask-WTF/CSRFProtect
                // 'X-CSRFToken': '{{ csrf_token() }}' // Przykład dla Jinja2 z CSRF
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data }))) // Przekaż status i dane JSON
        .then(({ status, body }) => {
            if (body.success) {
                showMessage(body.message || 'Pytanie dodane pomyślnie!', 'success');
                form.reset(); // Wyczyść formularz
                answersContainer.innerHTML = ''; // Wyczyść dynamiczne odpowiedzi
                 addAnswerField(); // Dodaj jedno puste pole z powrotem
                answersSection.style.display = 'none'; // Ukryj sekcję odpowiedzi
            } else {
                showMessage(body.message || 'Wystąpił błąd.', 'error');
            }
        })
        .catch(error => {
            console.error('Błąd podczas wysyłania:', error);
            showMessage('Błąd komunikacji z serwerem.', 'error');
        });
    });

    // Funkcja do wyświetlania komunikatów
    function showMessage(message, type) {
        messageArea.textContent = message;
        messageArea.classList.add(type); // 'success' lub 'error'
        messageArea.style.display = 'block';
    }

    // Inicjalizacja: Dodaj jedno pole odpowiedzi, jeśli typ 'choice' jest wybrany domyślnie (choć nie jest)
    // if (questionTypeSelect.value === 'choice') {
    //    addAnswerField();
    //}

});